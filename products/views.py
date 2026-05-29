from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

PRODUCT_LIST_CACHE_KEY = 'product_list'

class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            cache_data = cache.get(PRODUCT_LIST_CACHE_KEY)
            if cache_data:
                return Response(cache_data, status=status.HTTP_200_OK)
            else:
                queryset = Product.objects.select_related('warehouse', 'inventory').all()
                serializer = ProductSerializer(queryset, many=True)
                cache.set(PRODUCT_LIST_CACHE_KEY, serializer.data, timeout=300)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response()

class ProductDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            cache_key = f"product_{pk}"
            cache_data = cache.get(cache_key)
            if cache_data:
                return Response(cached_data, status=status.HTTP_200_OK)
            else:
                product = Product.objects.select_related('warehouse', 'inventory').filter(pk=pk).first()
                if not product:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                serializer = ProductSerializer(product)
                cache.set(cache_key, serializer.data, timeout=300)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response()