from rest_framework import serializers
from .models import Product, Supplier, Inventory

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only=True


class ProductSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'supplier']

    def create(self, validated_data):
        supplier_data = validated_data.pop('supplier')
        supplier, created = Supplier.objects.get_or_create(**supplier_data)
        product = Product.objects.create(supplier=supplier, **validated_data)
        return product
    
    def update(self, instance, validated_data):
        supplier_data=validated_data.pop('supplier', None)

        if supplier_data:

            supplier, created = Supplier.objects.get_or_create(**supplier_data)
            instance.supplier=supplier
        instance.name=validated_data.get('name',instance.name)
        instance.description=validated_data.get('description', instance.description)
        instance.price=validated_data.get('price', instance.price)
        instance.save

        return instance



class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Inventory
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        # Create or update the product instance (including supplier)
        product_serializer = ProductSerializer()
        product = product_serializer.create(product_data)
        # Create the inventory instance
        inventory = Inventory.objects.create(product=product, **validated_data)
        return inventory

    def update(self, instance, validated_data):
        product_data = validated_data.pop('product', None)  # Extract product data if provided
        if product_data:
            # Update the product instance (including supplier)
            product_serializer = ProductSerializer(instance=instance.product)
            product_serializer.update(instance.product, product_data)

        # Update the inventory quantity
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()

        return instance

