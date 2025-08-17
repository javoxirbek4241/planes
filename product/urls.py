from django.urls import path
from .views import *
urlpatterns = [
    path('', ProductListCreate.as_view()),
    path('rud/<int:pk>/', ProductRud.as_view())
]