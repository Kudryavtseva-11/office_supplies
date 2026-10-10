from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock']
    list_filter = ['category']
    search_fields = ['name']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'created_at', 'total_amount', 'status']
    list_filter = ['status', 'created_at']
    list_editable = ('status',)
    search_fields = ['customer_name', 'customer_email']
    inlines = [OrderItemInline]

    actions = ['make_confirmed', 'make_shipped', 'make_delivered', 'make_cancelled']
    
    def make_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'✅ Подтверждено заказов: {updated}')
    make_confirmed.short_description = 'Подтвердить выбранные заказы'
    
    def make_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'📦 Отправлено заказов: {updated}')
    make_shipped.short_description = 'Отправить выбранные заказы'
    
    def make_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'🏠 Доставлено заказов: {updated}')
    make_delivered.short_description = 'Отметить как доставленные'
    
    def make_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'❌ Отменено заказов: {updated}')
    make_cancelled.short_description = 'Отменить выбранные заказы'