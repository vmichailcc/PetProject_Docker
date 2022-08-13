from datetime import datetime, timedelta

from django.contrib import admin
from django.db.models import Sum, Count
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe

from accounts.models import CustomUser
from .models import Product, Pictures, ProductComment, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ("get_image", "name", "vendor_code", "brand",  "price", "old_price", "availability", "is_published")
    list_filter = ("brand", "price", "availability", "is_published", "card_views")
    list_editable = ("is_published", )
    search_fields = ["name", "description", "brand", "id"]

    def get_image(self, obj):
        if obj.main_picture:
            return mark_safe(f"<img src='{obj.main_picture_url}' width='75'>")
        else:
            return "Без фото"
    get_image.short_description = "Фото"


class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "status", "created_at", "owner", )
    list_filter = ("status", )
    search_fields = ["order_number"]

    fields = ("order_number", ("product", "quantity"), "owner_comment", "status", "admin_comment", "owner")
    readonly_fields = ("owner", "order_number")


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ("text_product", "text_author", "text", "text_created_at", )


class MyAdminSite(admin.AdminSite):
    site_title = "STORE Адмін панель"
    site_header = "STORE Адмін панель"

    def index(self, request, extra_context=None):
        app_list = self.get_app_list(request)
        user_count = CustomUser.objects.count()
        user_count_last_week = CustomUser.objects.filter(
            date_joined__range=[datetime.now() - timedelta(weeks=1), datetime.now()]
        ).count()
        orders_count = Order.objects.count()
        orders_count_last_week = Order.objects.filter(
            created_at__range=[datetime.now() - timedelta(weeks=1), datetime.now()]
        ).count()
        products_count = Product.objects.count()
        likes = Product.objects.aggregate(Sum('like'))
        comments = len(ProductComment.objects.annotate(Count('text')))
        context = {
            **self.each_context(request),
            "title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            **(extra_context or {}),
            "user_count": user_count,
            "user_count_last_week": user_count_last_week,
            "orders_count": orders_count,
            "orders_count_last_week": orders_count_last_week,
            "products_count": products_count,
            "likes": likes['like__sum'],
            "comments": comments,
        }

        request.current_app = self.name

        return TemplateResponse(
            request, self.index_template or "admin/index.html", context
        )


admin.site = MyAdminSite()
admin.site.register(Product, ProductAdmin)
admin.site.register(Pictures)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(Order, OrderAdmin)
