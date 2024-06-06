from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller_login, name='seller_login'),
    path('aromat_sold/', views.aromat_sold, name='aromat_sold'),
    path('aromat_sold_list/', views.aromat_sold_list, name='aromat_sold_list'),
    path('aromat_list_seller/', views.aromat_list_seller, name='aromat_list_seller'),
    path('seller_logout/', views.seller_logout, name='seller_logout'),
]
