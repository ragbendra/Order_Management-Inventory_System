from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import CreateOrderSerializer, OrderSerializer
from .services import create_order, cancel_order

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = create_order(
            user=request.user,
            items=serializer.validated_data['items'],
            idempotency_key=serializer.validated_data['idempotency_key']
        )

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        cancel_order(order_id=pk)
        return Response({'message': 'Order cancelled successfully.'}, status=status.HTTP_200_OK)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.prefetch_related('items__product').filter(pk=pk, user=request.user).first()
        if not order:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
