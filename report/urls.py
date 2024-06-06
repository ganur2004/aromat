from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('aromat_add', views.aromat_add, name='aromat_add'),
    path('aromat_add/<int:branch_id>/', views.aromat_add, name='aromat_add_by_branch'),
    path('logout/', views.logout_view, name='logout'),
    path('aromat_list/', views.aromat_list, name="aromat_list"),
    path('aromat_list/<int:branch_id>/', views.aromat_list, name="aromat_list_by_branch"),
    path('seller_register/', views.seller_register, name="seller_register"),
    path('seller_register/<int:branch_id>/', views.seller_register, name="seller_register_by_branch"),
    path('seller_report/', views.seller_report, name="seller_report"),
    path('seller_report/<int:branch_id>/', views.seller_report, name="seller_report_by_branch"),
    path('aromats/edit/<int:pk>/', views.edit_aromat, name='edit_aromat'),
    path('aromats/delete/<int:pk>/', views.delete_aromat, name='delete_aromat'),
    path('aromat_sold_list_admin/', views.aromat_sold_list_admin, name='aromat_sold_list_admin'),
    path('aromat_sold_list_admin/<int:branch_id>/', views.aromat_sold_list_admin, name='aromat_sold_list_admin_by_branch'),
    path('seller_report/seller/<int:pk>/', views.seller_report_page, name='seller_report_page'),
    path('<int:branch_id>/', views.purchases_by_branch, name='purchases_by_branch'),
]
