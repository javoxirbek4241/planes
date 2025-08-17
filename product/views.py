from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Products
from .serializers import ProductSerializer

class ProductListCreate(APIView):
    def get(self, request):
        product = Products.objects.all()
        category = request.GET.get('category')
        price = request.GET.get('price')
        if category:
            product = product.filter(category=category)
        if price:
            product = product.filter(price=price)
        search = request.GET.get('search')
        if search:
            product = product.filter(Q(name__icontains=search) | Q(description__icontains=search))
        ordering = request.GET.get('ordering')
        if ordering:
            product = product.order_by(ordering)

        serializer = ProductSerializer(product, many=True)
        return Response({'data':serializer.data, "status":status.HTTP_200_OK})
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'status':status.HTTP_201_CREATED})
        return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

class ProductRud(APIView):
    def get(self, request, pk):
        try:
            product = Products.objects.get(id=pk)
        except Products.DoesNotExist:
            return Response({'message':'product topilmadi', 'status':status.HTTP_400_BAD_REQUEST})
        serializer = ProductSerializer(product)
        return Response({'data': serializer.data, "status": status.HTTP_200_OK})

    def put(self, request, pk):
        try:
            product = Products.objects.get(id=pk)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found', 'status':status.HTTP_404_NOT_FOUND})
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK, 'updated_data':serializer.data})
        return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

    def patch(self, request, pk):
        try:
            product = Products.objects.get(id=pk)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found', 'status':status.HTTP_404_NOT_FOUND})
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK, 'updated_data':serializer.data})
        return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

    def delete(self,request, pk):
        try:
            product = Products.objects.get(id=pk)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found', 'status':status.HTTP_404_NOT_FOUND})
        product.delete()
        return Response({'status':status.HTTP_200_OK, 'message':'product deleted'})
