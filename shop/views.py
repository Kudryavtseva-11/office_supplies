from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderCreateSerializer
import json

# HTML страницы
def index(request):
    return render(request, 'shop/index.html')

def cart_page(request):
    return render(request, 'shop/cart.html')

def profile_page(request):
    return render(request, 'shop/profile.html')

def order_success(request, order_id):
    return render(request, 'shop/order_success.html', {'order_id': order_id})

# API endpoints (остаются без изменений)
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_order(request):
    serializer = OrderCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.validated_data
        
        # Создаем заказ
        order = Order.objects.create(
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            customer_phone=data['customer_phone'],
            customer_address=data['customer_address']
        )
        
        total = 0
        
        # Добавляем товары в заказ
        for item in data['items']:
            try:
                product = Product.objects.get(id=item['product_id'])
                
                if product.stock < item['quantity']:
                    order.delete()
                    return Response({
                        'error': f'Недостаточно товара: {product.name}'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Уменьшаем количество на складе
                product.stock -= item['quantity']
                product.save()
                
                item_total = product.price * item['quantity']
                total += item_total
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )
                
            except Product.DoesNotExist:
                order.delete()
                return Response({
                    'error': f'Товар с id {item["product_id"]} не найден'
                }, status=status.HTTP_404_NOT_FOUND)
        
        order.total_amount = total
        order.save()
        
        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_order(request, id):
    try:
        order = Order.objects.get(id=id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)