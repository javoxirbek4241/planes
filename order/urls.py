from django.urls import path
from .views import CreateOrder, UserOrders, OrderDetail, UpdateOrderStatus, CancelOrder

urlpatterns = [
    path('create/', CreateOrder.as_view()),
    path('orders/', UserOrders.as_view()),
    path('order_detail/<int:pk>/', OrderDetail.as_view()),
    path('status/<int:pk>/', UpdateOrderStatus.as_view()),
    path('cancel/<int:pk>/', CancelOrder.as_view()),
]