from rest_framework import serializers
from .models import Category, Product, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name',
                                          read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name',
                  'price', 'stock', 'description', 'image_url']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name',
                                         read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name',
                  'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email',
                  'customer_phone', 
                  'customer_address', 'created_at',
                  'status', 'total_amount', 'items']

class OrderCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=100)
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField(max_length=20)
    customer_address = serializers.CharField()
    items = serializers.ListField(child=serializers.DictField())
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Корзина не может быть пустой")
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Неверный формат товара")
            if item['quantity'] < 1:
                raise serializers.ValidationError("Количество должно быть больше 0")
        return value