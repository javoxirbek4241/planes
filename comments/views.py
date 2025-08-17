from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer
from product.models import Products


class ProductCommentListCreateAPIView(APIView):

    def get(self, request, pk):
        product = Products.objects.filter(id=pk).first()
        if not product:
            return Response({'error': 'Product not found', 'status': status.HTTP_404_NOT_FOUND})

        if request.user.is_staff:
            comments = Comment.objects.filter(product=product)
        else:
            comments = Comment.objects.filter(product=product, user=request.user)

        serializer = CommentSerializer(comments, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})

    def post(self, request, pk):
        product = Products.objects.filter(id=pk).first()
        if not product:
            return Response({'error': 'Product not found', 'status': status.HTTP_404_NOT_FOUND})

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response({'data': serializer.data, 'status': status.HTTP_201_CREATED})
        return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})


class CommentUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        comment = Comment.objects.filter(id=pk, user=request.user).first()
        if not comment:
            return Response({'error': 'Comment not found', 'status': status.HTTP_404_NOT_FOUND})

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': status.HTTP_200_OK})
        return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})

    def delete(self, request, pk):
        comment = Comment.objects.filter(id=pk, user=request.user).first()
        if not comment:
            return Response({'error': 'Comment not found', 'status': status.HTTP_404_NOT_FOUND})

        comment.delete()
        return Response({'message': 'Comment deleted', 'status': status.HTTP_204_NO_CONTENT})


class AllCommentsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_staff:
            comments = Comment.objects.all()
        else:
            comments = Comment.objects.filter(user=request.user)

        serializer = CommentSerializer(comments, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})




