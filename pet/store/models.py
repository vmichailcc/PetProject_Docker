from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.conf import settings
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from .utils import create_new_ref_number


class Product(models.Model):
    id = models.CharField(verbose_name="ID", primary_key=True, max_length=100)
    name = models.CharField(verbose_name="Назва", max_length=200)
    category = models.CharField(max_length=200, verbose_name="Категорія")
    vendor_code = models.CharField(verbose_name="Код товара", max_length=200)
    price = models.PositiveIntegerField(verbose_name="Ціна")
    old_price = models.IntegerField(default=0, verbose_name="Стара ціна")
    availability = models.BooleanField("Наявність", default=1)
    is_published = models.BooleanField("Публікація", default=1)
    moderated_at = models.DateTimeField(verbose_name="Час оновленя", auto_now=True)
    description = models.TextField(verbose_name="Опис", max_length=5000)
    brand = models.CharField(verbose_name="Бренд", max_length=150)
    main_picture = models.ImageField(
        verbose_name="Головне зображення",
        blank=True,
        upload_to="uploadphoto/main_picture/"
    )
    main_picture_url = models.URLField()
    options = models.JSONField(verbose_name="Опції", blank=True, null=True)
    attributes = models.JSONField(verbose_name="Атрибути", blank=True, null=True)
    card_views = models.IntegerField(verbose_name="Перегляди", default=0)
    like = models.IntegerField(verbose_name="Лайк", default=0)

    def save(self, *args, **kwargs):
        if self.main_picture_url and not self.main_picture:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.main_picture_url).read())
            img_temp.flush()
            self.main_picture.save(f"image_{self.pk}.jpg", File(img_temp))
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def get_absolute_url(self):
        return reverse("view_card", kwargs={"pk": self.pk})


class Pictures(models.Model):
    pictures_point = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name="Назва товару що зображен",
        related_name="pictures",
    )
    pictures = models.ImageField(blank=True, upload_to="uploadphoto/%d%m%Y/", verbose_name="Назва зображення")

    def get_absolute_url(self):
        return reverse("pictures", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Зображення"
        verbose_name_plural = "Зображення"

    def __str__(self):
        return self.pictures


class ProductComment(models.Model):
    text_product = models.ForeignKey(Product,
                                     on_delete=models.CASCADE,
                                     verbose_name="Продукт",
                                     related_name='text_product'
                                     )
    text_author = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    verbose_name="Автор",
                                    related_name='text_author'
                                    )
    text = models.TextField(verbose_name="Комментар", max_length=1000)
    text_created_at = models.DateTimeField(verbose_name="Час створення", auto_now_add=True)

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"


class Order(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
        related_name='product'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Покупець",
        related_name='owner',
    )
    order_number = models.CharField(
        verbose_name="Номер замовлення",
        max_length=10,
        blank=True,
        editable=False,
        unique=True,
        default=create_new_ref_number)
    quantity = models.PositiveIntegerField(
        verbose_name="Кількість",
        default=1,
        validators=[
            MaxValueValidator(99),
            MinValueValidator(1)
        ])
    status = models.CharField(
        choices=(
            ("new", "Новий"),
            ("in progress", "В роботі"),
            ("sent", "Відправлено"),
            ("canceled", "Відмінено"),
            ("completed", "Завершено"),
        ),
        max_length=11,
        default="new",
        verbose_name="Статус"
    )
    owner_comment = models.CharField(verbose_name="Коментар покупця", max_length=500, blank=True)
    admin_comment = models.CharField(verbose_name="Коментар від адміна", max_length=500, blank=True)
    created_at = models.DateTimeField(verbose_name="Дата створення", auto_now_add=True)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def __str__(self):
        return self.order_number
