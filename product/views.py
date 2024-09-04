from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import ProductFilter
from drf_yasg.utils import swagger_auto_schema
from .pagination import CustomPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from product.serializers import *
from django.db.models import Count, Avg
from product.models import *


class HomepageView(APIView):
    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт возвращает данные для главной страницы, "
                              "включая баннер, товар дня, новые товары, "
                              "товары со скидками и популярные товары."
                              "Для выбора товрав дня, надо найти товар который "
                              "мы хотим сделать товаром дня, и надо обновить "
                              "как product_of_the_day = True, после этого, "
                              "этот товар будет товаром дня "
    )
    def get(self, request, *args, **kwargs):
        banner = Banner.objects.filter(id=1).first()
        product_of_the_day = Product.objects.filter(is_product_of_the_day=True, is_active=True).first()
        new_products = Product.objects.filter(is_active=True).order_by('-id')[:4]
        promotion_products = Product.objects.filter(promotion__isnull=False, is_active=True)[:4]
        popular_products = Product.objects.filter(is_active=True).annotate(
            review_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')
        ).filter(
            review_count__gt=0
        ).order_by('-avg_rating')[:8]

        response_data = {
            "homepage": {
                "banner": self.serialize_banner(banner),
                "product_of_the_day": self.serialize_product(product_of_the_day),
                "promotion": self.serialize_products(promotion_products),
                "popular": self.serialize_products(popular_products),
                "new": self.serialize_products(new_products),
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def serialize_banner(self, banner):
        if banner:
            # Предположим, у вас есть сериализатор для модели Banner
            serializer = BannerSerializer(banner)
            return serializer.data
        return None

    def serialize_product(self, product):
        if product:
            serializer = ProductShortSerializer(product)
            return serializer.data
        return None

    def serialize_products(self, products):
        serializer = ProductShortSerializer(products, many=True)
        return serializer.data


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Этот эндпоинт позволяет получить список "
                              "всех категорий и создать новую категорию."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Этот эндпоинт позволяет создать новую категорию."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Этот эндпоинт позволяет получить, "
                              "обновить или удалить категорию по ID."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Этот эндпоинт позволяет обновить категорию по ID."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['category'],
        operation_description="Этот эндпоинт позволяет удалить категорию по ID."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    @swagger_auto_schema(
        tags=['brand'],
        operation_description="Этот эндпоинт позволяет получить список всех брендов и создать новый бренд."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['brand'],
        operation_description="Этот эндпоинт позволяет создать новый бренд."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    @swagger_auto_schema(
        tags=['brand'],
        operation_description="Этот эндпоинт позволяет получить, обновить или удалить бренд по ID."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['brand'],
        operation_description="Этот эндпоинт позволяет обновить бренд по ID."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['brand'],
        operation_description="Этот эндпоинт позволяет удалить бренд по ID."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ColorListCreateView(generics.ListCreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет получить список всех цветов и создать новый цвет."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет создать новый цвет."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ColorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет получить, обновить или удалить цвет по ID."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет обновить цвет по ID."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['color'],
        operation_description="Этот эндпоинт позволяет удалить цвет по ID."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductShortSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'price', 'promotion', 'description']

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить список всех товаров."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет создать новый продукт."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        product = super().get_object()
        product.similar_products = self.get_similar_products(product)
        return product

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет посмотреть похожие товары, "
                              "на товар который мы выбрали через ID, "
                              "схожость выбирается по категории и по цене товара."
    )
    def get_similar_products(self, product):
            # Convert price to Decimal for accurate arithmetic operations
        price = Decimal(product.price)
        price_range = Decimal('0.2') * price

            # Query for similar products
        similar_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id).filter(
            price__gte=price - price_range,
            price__lte=price + price_range
        ).distinct()

            # Serialize similar products
        serializer = ProductShortSerializer(similar_products, many=True, context=self.get_serializer_context())
        return serializer.data

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить, обновить или удалить продукт по ID."
    )
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        data = response.data
        data['similar_products'] = self.get_object().similar_products
        return Response(data)

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет обновить продукт по ID."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет удалить продукт по ID."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductNewView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductShortSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'price', 'promotion', 'description']

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить список новинок товаров."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.all().order_by('-id')


class ProductPromotionView(generics.ListAPIView):
    queryset = Product.objects.filter(promotion__isnull=False, is_active=True)
    serializer_class = ProductShortSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'price', 'promotion', 'description']

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить список товаров с акциями."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить список продуктов c акциями."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductPopularView(generics.ListAPIView):
    serializer_class = ProductShortSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'price', 'promotion', 'description']

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет получить список популярных продуктов "
                              "(только те, у которых есть отзывы)."
    )
    def get_queryset(self):
        # Получаем популярные продукты с аннотациями
        return Product.objects.annotate(
            review_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')  # Средний рейтинг
        ).filter(
            review_count__gt=0,
            is_active=True
        ).order_by('-avg_rating')  # Сортируем только по avg_rating

    def get(self, request, *args, **kwargs):
        # Используем `get_queryset` для получения данных
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.filter(id=1)
    serializer_class = ProductCreateSerializer

    @swagger_auto_schema(
        tags=['product'],
        operation_description="Этот эндпоинт позволяет создать новый продукт."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @swagger_auto_schema(
        tags=['review'],
        operation_description="Этот эндпоинт позволяет создать комментарий и оставить рейтинг."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @swagger_auto_schema(
        tags=['review'],
        operation_description="Этот эндпоинт позволяет получить определенный комменарий по id."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Review.objects.filter(id=self.kwargs.get('pk'))


class BannerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    @swagger_auto_schema(
        tags=['banner'],
        operation_description="Этот эндпоинт позволяет получить, обновить или удалить баннер для главное страницы."
    )
    def get_object(self):
        # Получаем первый объект, либо создаем его, если он не существует
        obj, created = Banner.objects.get_or_create(id=1)
        return obj