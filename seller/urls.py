from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller_login, name='seller_login'),
    path('aromat_sold/', views.aromat_sold, name='aromat_sold'),
    path('seller_logout/', views.seller_logout, name='seller_logout'),
    # другие пути
]
