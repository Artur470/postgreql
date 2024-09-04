from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
import pytz
import uuid

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('product.Product', related_name='cartitems', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"CartItem {self.id} for Cart {self.cart.id}"

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id} for Cart {self.cart.id}"
class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)  # Например: "Card", "Cash", "Bank Transfer"
    description = models.TextField(blank=True, null=True)  # Дополнительное описание (по желанию)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, null=True, blank=True, on_delete=models.SET_NULL)
    total_price = models.FloatField()
    address = models.CharField(max_length=255)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

    def clear_user_cart(self):
        # Очистите корзину пользователя
        self.cart.cartitem_set.all().delete()
        self.cart.total_price = 0
        self.cart.save()

    def send_order_email(self):
        order_time_utc = self.ordered_at
        timezone_bishkek = pytz.timezone('Asia/Bishkek')  # Избегаем конфликта с модулем `timezone`
        order_time_local = order_time_utc.astimezone(timezone_bishkek)
        order_time_str = order_time_local.strftime('%Y-%m-%d %H:%M:%S')

        subject = 'Новый заказ!'
        message = f'Номер заказа: {self.id}\n' \
                  f'Email Пользователя: {self.user.email}\n' \
                  f'Имя пользователя: {self.user.first_name} {self.user.last_name}\n' \
                  f'Номер телефона пользователя: {self.user.number}\n' \
                  f'Адрес: {self.address}\n' \
                  f'Способ оплаты: {self.payment_method.name if self.payment_method else "Не указан"}\n' \
                  f'Окончательная цена: {self.total_price}\n' \
                  f'Время заказа: {order_time_str}\n\n'

        if self.user.wholesaler:
            message += "Покупатель является оптовиком.\n\n"

        items = self.cart.cartitem_set.all()
        if items.exists():
            message += "\nТовары в заказе:\n\n"
            for item in items:
                message += f'ID продукта: {item.product.id}\n' \
                           f'Продукт: {item.product.title}\n' \
                           f'Категория: {item.product.category}\n' \
                           f'Цвет: {item.product.color}\n' \
                           f'Бренд: {item.product.brand}\n' \
                           f'Количество: {item.quantity}\n' \
                           f'Цена за 1 товар: {item.price / item.quantity}\n' \
                           f'Цена за все товары: {item.price}\n\n'

        admin_email = 'homelife.site.kg@gmail.com'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])
