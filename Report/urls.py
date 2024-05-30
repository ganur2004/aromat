from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('aromat_add', views.aromat_add, name='aromat_add'),
    path('logout/', views.logout_view, name='logout'),
    path('aromat_list/', views.aromat_list, name="aromat_list"),
    path('seller_register/', views.seller_register, name="seller_register"),
    path('seller_report/', views.seller_report, name="seller_report")
    # другие пути
]
