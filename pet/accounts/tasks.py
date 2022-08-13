import os

from celery import shared_task
from django.core.mail import EmailMessage

from store.models import Order

domain = os.environ.get("LOCAL_DOMAIN")


@shared_task
def send_status_email_celery(pk, order_status):
    order = Order.objects.get(pk=pk)
    if order.owner.send_status_email == 1:
        welcome_message = f"Статус замовлення № {order.order_number}"
        email_message = f"Вітаю, {order.owner}! " \
                        f"Ваше замовлення № {order.order_number} отримало статус - {order_status}. " \
                        f"Дякуємо!" \
                        f"Ссилка на замовлення: http://{ domain }/orders/{order.owner.pk}"

        mail_recipient = order.owner.email

        email = EmailMessage(
            welcome_message,
            email_message,
            to=[mail_recipient]
        )
        print(email)
        email.send()
