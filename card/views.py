
from .serializers import CardSerializer, CardItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Card, CardItem
from product.models import Products
from .serializers import CardSerializer

class CardCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        card, created = Card.objects.get_or_create(user=request.user)
        serializer = CardSerializer(card)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )




class AddToCard(APIView):
    permission_classes = [IsAuthenticated]  # faqat login qilgan user qo‘sha oladi

    def post(self, request):
        product_id = request.data.get("product_id")
        amount = request.data.get("amount", 1)

        product = Products.objects.filter(id=product_id).first()
        if not product:
            return Response(
                {"error": "Bunday mahsulot topilmadi"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if amount<=0 or amount>100:
            return Response(
                {"error": "hato malumot kiritdingiz"},
                status=status.HTTP_400_BAD_REQUEST
            )
        card, _ = Card.objects.get_or_create(user=request.user)

        card_item, created = CardItem.objects.get_or_create(
            card=card,
            product=product,
            amount=amount
        )
        if not created:
            card_item.amount += amount
            card_item.save()

        serializer = CardItemSerializer(card_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Product_update(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        count = request.data.get('count', None)
        mtd = request.data.get('mtd', None)
        product = CardItem.objects.get(card__user = request.user, id=pk)
        if count:
            product.amount = count
            product.save()

        elif mtd:
            if mtd == '+':
                product.amount += 1
            elif mtd == "-":
                if product.amount==1:
                    product.delete()
                else:
                    product.amount -= 1
                    product.save()
        else:
            return Response({'error':'error'})
        serializer = CardItemSerializer(product)
        return Response({'data':serializer.data})

class ClearCard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            card = Card.objects.get(user=request.user)
            card.items.all().delete()
            return Response({'message': 'savat tozalandi'}, status=status.HTTP_200_OK)
        except Card.DoesNotExist:
            return Response({'message': 'savat bo‘sh'}, status=status.HTTP_200_OK)










