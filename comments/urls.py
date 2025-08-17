from django.urls import path
from .views import ProductCommentListCreateAPIView, CommentUpdateDeleteAPIView, AllCommentsAPIView
urlpatterns = [
    path('leave_comment/<int:pk>', ProductCommentListCreateAPIView.as_view()),
    path('update_comment/<int:pk>', CommentUpdateDeleteAPIView.as_view()),
    path('all_comments/', AllCommentsAPIView.as_view()),
]