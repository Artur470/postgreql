from rest_framework import serializers
from django.db.models import Avg
from .models import Product, Category, Color, Brand, Review, Banner
from .utils import round_to_nearest_half


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title"]


class ColorSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    class Meta:
        model = Color
        fields = ['title', 'key']

    def get_key(self, obj):
        translation = {
            'белый': 'white',
            'черный': 'black',
            'красный': 'red',
            'синий': 'blue',
            'зеленый': 'green',
            'желтый': 'yellow',
            'оранжевый': 'orange',
            'пурпурный': 'purple',
            'розовый': 'pink',
            'серый': 'gray',
            'коричневый': 'brown',
            'бежевая': 'beige',
            'фиолетовый': 'violet',
            'голубой': 'light blue',
            'бирюзовый': 'turquoise',
            'мятный': 'mint',
            'лавандовый': 'lavender',
            'гранатовый': 'pomegranate',
            'песочный': 'sand',
            'оливковый': 'olive',
            'малахитовый': 'malachite',
            'медный': 'copper',
            'слоновая кость': 'ivory',
            'медный': 'copper'
        }


        if obj.key:
            return translation.get(obj.key,
                                   obj.key)

        return translation.get(obj.title.lower(), obj.title.lower())


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["title"]


class ReviewSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comments']


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = [
#             'image1',
#             'image2',
#             'image3'
#         ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    reviews = ReviewSummarySerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'color',
            'images',
            'price',
            'promotion',
            'brand',
            'quantity',
            'description',
            'is_product_of_the_day',
            'reviews',
            'avg_rating',
            'is_active',
        ]

    def get_avg_rating(self, obj):
        if obj.reviews.exists():
            avg_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round_to_nearest_half(avg_rating)
        return 0

    def get_images(self, obj):
        request = self.context.get('request')
        images = [
            obj.image1.url if obj.image1 else None,
            obj.image2.url if obj.image2 else None,
            obj.image3.url if obj.image3 else None,
        ]
        if request:
            return [request.build_absolute_uri(image) for image in images if image]
        return [image for image in images if image]


class ProductShortSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'images',
            'avg_rating',
            'title',
            'price',
            'promotion',
        ]

    def get_avg_rating(self, obj):
        if obj.reviews.exists():
            avg_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round_to_nearest_half(avg_rating)
        return 0

    def get_images(self, obj):
        request = self.context.get('request')
        images = [
            obj.image1.url if obj.image1 else None,
            obj.image2.url if obj.image2 else None,
            obj.image3.url if obj.image3 else None,
        ]
        if request:
            return [request.build_absolute_uri(image) for image in images if image]
        return [image for image in images if image]


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'color',
            'image1',
            'image2',
            'image3',
            'price',
            'promotion',
            'brand',
            'quantity',
            'description',
            'is_product_of_the_day',
            'is_active'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            images = [
                request.build_absolute_uri(instance.image1.url) if instance.image1 else None,
                request.build_absolute_uri(instance.image2.url) if instance.image2 else None,
                request.build_absolute_uri(instance.image3.url) if instance.image3 else None,
            ]
            representation['images'] = [image for image in images if image]
        if not instance.reviews.exists():
            representation.pop('reviews', None)
        return representation


class ReviewSerializer(serializers.ModelSerializer):

    product_title = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'product',
            'product_title',
            'user',
            'user_name',
            'comments',
            'rating',
            'created',
            'updated'
        ]

    def get_product_title(self, obj):
        return obj.product.title if obj.product else 'unknown'

    def get_user_name(self, obj):
        return obj.user.first_name if obj.user else 'unknown'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('product', None)
        representation.pop('user', None)
        return representation


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'