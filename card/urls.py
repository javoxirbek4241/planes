from django.urls import path
from .views import *
urlpatterns = [
    path('create_card/', CardCreate.as_view()),
    path('add/', AddToCard.as_view()),
    path('pr_amount_add/<int:pk>/', Product_update.as_view()),
    path('clear_card/', ClearCard.as_view())
]