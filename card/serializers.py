from .models import Card, CardItem
from rest_framework import serializers

class CardItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CardItem
        fields=['id', 'card', 'product', 'amount', 'created_at', 'updated_at', 'total_price']


class CardSerializer(serializers.ModelSerializer):
    items = CardItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Card
        fields = ['id', 'user', 'created_at', 'total_price', 'items']