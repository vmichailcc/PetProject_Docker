from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Product, ProductComment, Pictures, Order
from .serializers import StoreSerializer, ProductCommentSerializer, OrderSerializer, ProductDetailSerializer, \
    OrderDetailSerializer


class ProductView(ListView):
    model = Product
    template_name = "store/index.html"
    context_object_name = "products"
    paginate_by = 20


class ProductDetailView(View):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        pictures = Pictures.objects.filter(pictures_point=pk)
        comments = ProductComment.objects.filter(text_product=pk)
        context = {
            "product": product,
            "pictures": pictures,
            "comments": comments,
        }
        return render(request, "store/product.html", context)


class StoreApiView(ListModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand', 'price']
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(comments=Count('text_product'))
        return queryset


class ProductDetailApiView(RetrieveModelMixin, GenericViewSet):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(comments_count=Count('text_product'))
        return queryset

    @action(detail=True, methods=['post'])
    def add_like(self, request, pk=None):
        prod = self.get_object()
        prod.like += 1
        prod.save()
        serializer = self.get_serializer(prod)
        return Response(serializer.data)


class CommentApiView(CreateModelMixin, GenericViewSet):
    serializer_class = ProductCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(**{'text_author': self.request.user})

    def get_queryset(self):
        user = self.request.user
        return ProductComment.objects.filter(text_author=user)


class OrderApiView(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            user = self.request.user
            serializer.save(**{'owner': user})

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(owner=user.pk)


class OrderDetailApiView(RetrieveModelMixin, GenericViewSet):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()


class OrderView(View):
    def get(self, request, pk):
        orders = Order.objects.filter(pk=pk)
        context = {"orders": orders}
        return render(request, "store/orders.html", context)
