from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('aromat_add', views.aromat_add, name='aromat_add'),
    path('logout/', views.logout_view, name='logout'),
    path('aromat_list/', views.aromat_list, name="aromat_list"),
    path('seller_register/', views.seller_register, name="seller_register"),
    path('seller_report/', views.seller_report, name="seller_report"),
    path('aromats/edit/<int:pk>/', views.edit_aromat, name='edit_aromat'),
    path('aromats/delete/<int:pk>/', views.delete_aromat, name='delete_aromat'),
    path('aromat_sold_list_admin/', views.aromat_sold_list_admin, name='aromat_sold_list_admin'),
    path('seller_report/seller/<int:pk>/', views.seller_report_page, name='seller_report_page'),
]
