from django.urls import path

from menu import views

urlpatterns = [
    path('menu/', views.get_menu),
    path('menu/<str:slug>/', views.get_menu),
]