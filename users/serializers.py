# users/serializers.py

from rest_framework import serializers
from .models import User, Role, Category, SubCategory, Product, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item_id', 'product', 'quantity', 'subtotal', 'order']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['order_id', 'total_price', 'order_date', 'customer', 'employee_id', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()

        keep_items = []
        for item_data in items_data:
            if 'item_id' in item_data:
                item = OrderItem.objects.get(id=item_data['item_id'])
                item.quantity = item_data.get('quantity', item.quantity)
                item.subtotal = item_data.get('subtotal', item.subtotal)
                item.save()
                keep_items.append(item.id)
            else:
                new_item = OrderItem.objects.create(order=instance, **item_data)
                keep_items.append(new_item.id)

        instance.items.exclude(id__in=keep_items).delete()
        return instance
