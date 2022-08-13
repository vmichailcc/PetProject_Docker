from django.contrib import admin

from store.models import Order
from .models import CustomUser, MailingList


class OrderInline(admin.TabularInline):
    model = Order
    readonly_fields = ("order_number", "status",)
    fields = ("order_number", "status", )
    extra = 0


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name",  "city", "order_count")
    search_fields = ["first_name", "last_name"]
    fields = ("first_name", "last_name", "city", "block")
    readonly_fields = ("first_name", "last_name",  "city", "order_count")
    inlines = [
        OrderInline
    ]

    def order_count(self, obj):
        count = Order.objects.filter(owner=obj)
        return len(count)

    order_count.short_description = "Кількість замовлень"


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MailingList)
