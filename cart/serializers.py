from rest_framework import serializers
from .models import Cart, CartItem, Order, PaymentMethod
from product.serializers import ProductSerializer

class CartItemsSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(source='cart.id', read_only=True)
    product = ProductSerializer(read_only=True)  # Используем ProductSerializer для вложенного продукта

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'product', 'quantity', 'price']

    def create(self, validated_data):
        cart = validated_data.get('cart')
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        user = self.context['request'].user

        if product.quantity < quantity:
            raise serializers.ValidationError('Not enough stock available.')

        price = product.promotion if product.promotion else product.price
        total_price = price * quantity

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity, 'price': total_price, 'user': user}
        )

        if not created:
            if product.quantity < quantity:
                raise serializers.ValidationError('Not enough stock available.')

            product.quantity -= (quantity - cart_item.quantity)
            cart_item.quantity = quantity
            cart_item.price = price * quantity
            product.save()
            cart_item.save()
        else:
            product.quantity -= quantity
            product.save()

        cart.update_total_price()

        return cart_item

    def update(self, instance, validated_data):
        new_quantity = validated_data.get('quantity', instance.quantity)
        product = instance.product

        if new_quantity != instance.quantity:
            if product.quantity + instance.quantity < new_quantity:
                raise serializers.ValidationError('Not enough stock available.')

            product.quantity += instance.quantity - new_quantity
            price = product.promotion if product.promotion else product.price
            instance.price = price * new_quantity
            instance.quantity = new_quantity
            product.save()
            instance.save()

            cart = instance.cart
            cart.update_total_price()

        return instance
class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    items = CartItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'ordered', 'user', 'items']

    def get_total_price(self, obj):
        return sum(item.price for item in obj.items.all())
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name']

class OrderSerializer(serializers.ModelSerializer):
    payment_method = serializers.PrimaryKeyRelatedField(queryset=PaymentMethod.objects.all())

    class Meta:
        model = Order
        fields = ['user', 'cart', 'total_price', 'address', 'payment_method']
