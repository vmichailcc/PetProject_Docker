from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import CustomUser
from .utils import send_verify_email


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Ім'я", widget=forms.TextInput(attrs={'class': 'form-control'}), )
    last_name = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label="Місто", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Електрона пошта", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Повторити пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "city", "password1", "password2")


class UserLoginForm(AuthenticationForm):

    def confirm_login_allowed(self, user):

        if user.block:
            raise ValidationError(
                "Аккаунт заблоковано!"
            )

        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

        if not user.email_verify:
            send_verify_email(self.request, user)
            raise ValidationError(
                "Електронна пошта не веріфікована. Будь ласка, перевірте пошту!",
                code='invalid_login'
            )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        print("username =", username)
        print("password =", password)
        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
