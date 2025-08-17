from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Order, OrderItem
from .serializers import OrderSerializer
from card.models import Card, CardItem

class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            card = Card.objects.get(user=request.user)
            if not card.items.exists():
                return Response({'error': 'Savat bo‘sh'}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.create(user=request.user, total_price=card.total_price)

            for item in card.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    amount=item.amount,
                    price=item.total_price
                )

            card.items.all().delete()

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Card.DoesNotExist:
            return Response({'error': 'Savat topilmadi'}, status=status.HTTP_404_NOT_FOUND)


class UserOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Buyurtma topilmadi'}, status=status.HTTP_404_NOT_FOUND)


class UpdateOrderStatus(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        status_new = request.data.get('status')
        if status_new not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Notog‘ri status'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=pk)
            order.status = status_new
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Buyurtma topilmadi'}, status=status.HTTP_404_NOT_FOUND)


class CancelOrder(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
            if order.status in ['completed', 'canceled']:
                return Response({'error': 'Buyurtmani bekor qilib bo‘lmaydi'}, status=status.HTTP_400_BAD_REQUEST)
            order.status = 'canceled'
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Buyurtma topilmadi'}, status=status.HTTP_404_NOT_FOUND)
