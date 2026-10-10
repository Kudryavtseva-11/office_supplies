from django.urls import path
from . import views

urlpatterns = [
    # HTML страницы
    path('', views.index, name='index'),
    path('cart/', views.cart_page, name='cart'),
    path('profile/', views.profile_page, name='profile'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    
    # API endpoints
    path('api/products/', views.product_list, name='product_list'),
    path('api/products/<int:id>/', views.product_detail, name='product_detail'),
    path('api/orders/', views.create_order, name='create_order'),
    path('api/orders/<int:id>/', views.get_order, name='get_order'),
]