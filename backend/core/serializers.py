from rest_framework import serializers
from . import models

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductMedia
        fields = ["id","image","video"]

class ProductSerializer(serializers.ModelSerializer):
    media = ProductMediaSerializer(many=True, read_only=True)
    is_available = serializers.ReadOnlyField()
    display_price = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ["id","name","category","unit","price_per_unit","currency","display_price",
                  "available_from","available_to","verified","supplier","is_available","media"]

    def get_display_price(self, obj): return obj.display_price()

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ["id","product","quantity","unit_price_snapshot"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = models.Order
        fields = ["id","restaurant","delivery_date","status","created_at","items"]
    def create(self, validated_data):
        items = validated_data.pop("items", [])
        order = models.Order.objects.create(**validated_data)
        for item in items: models.OrderItem.objects.create(order=order, **item)
        return order

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer
        fields = ["id","order","supplier","price","delivery_eta","created_at"]

class PreOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PreOrder
        fields = ["id","restaurant","supplier","product","quantity","delivery_date","status","created_at"]

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalendarEvent
        fields = ["id","date","restaurant","supplier","order","preorder","event_type","status"]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ["id","reviewer","target","rating","comment","image","created_at"]

class ProductWaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductWaitlist
        fields = ["id","product","restaurant","desired_quantity","notified","created_at"]

class FavoritePartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FavoritePartner
        fields = ["id","restaurant","partner_user","created_at"]
