from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, UpdateView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .forms import UserRegisterForm, UserLoginForm
from .models import CustomUser
from .serializers import CustomUserSerializer, MailingListSerializer
from .utils import send_verify_email


class Register(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        context = {
            "form": UserRegisterForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_verify_email(request, user)
            return redirect("confirm_email")
        context = {
            "form": form
        }
        return render(request, self.template_name, context)


class LoginUserView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class ConfirmView(TemplateView):
    template_name = 'accounts/confirm_email.html'


class InvalidVerifyView(TemplateView):
    template_name = 'accounts/invalid_verify.html'


class VerifyEmail(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verify = 1
            user.save()
            login(request, user)
            return redirect('index')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                CustomUser.DoesNotExist, ValidationError):
            user = None
        return user


class UpdateProfileView(UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'city']
    template_name = 'accounts/update_profile.html'
    template_name_suffix = '_update_profile'


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class CustomUserApiView(ModelViewSet):
    serializer = CustomUserSerializer
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(**{'email': self.request.user.email})

    def get_queryset(self):
        email = self.request.user.email
        return CustomUser.objects.filter(email=email)

    @action(detail=True, methods=['post'])
    def mark_status_email(self, request, pk=None):
        mark = self.get_object()
        mark.send_status_email = 1
        mark.save()
        serializer = self.get_serializer(mark)
        return Response(serializer.data)


class MailingListApiView(CreateModelMixin, GenericViewSet):
    serializer_class = MailingListSerializer
