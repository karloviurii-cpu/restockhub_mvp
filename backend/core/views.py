from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from . import models, serializers

class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    pass

class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all().select_related("supplier").prefetch_related("media")
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category","supplier__verified","supplier__is_farmer"]
    search_fields = ["name","category","supplier__company_name"]
    ordering_fields = ["price_per_unit","available_from"]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all().select_related("restaurant")
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OfferViewSet(viewsets.ModelViewSet):
    queryset = models.Offer.objects.all().select_related("order","supplier")
    serializer_class = serializers.OfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["order","supplier"]
    ordering_fields = ["price","delivery_eta"]

class PreOrderViewSet(viewsets.ModelViewSet):
    queryset = models.PreOrder.objects.all().select_related("restaurant","supplier","product")
    serializer_class = serializers.PreOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = models.CalendarEvent.objects.all()
    serializer_class = serializers.CalendarEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["restaurant","supplier","event_type","status","date"]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all().select_related("reviewer","target")
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["target"]
    ordering_fields = ["created_at"]

class ProductWaitlistViewSet(viewsets.ModelViewSet):
    queryset = models.ProductWaitlist.objects.all().select_related("product","restaurant")
    serializer_class = serializers.ProductWaitlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product","restaurant","notified"]

class FavoritePartnerViewSet(viewsets.ModelViewSet):
    queryset = models.FavoritePartner.objects.all().select_related("restaurant","partner_user")
    serializer_class = serializers.FavoritePartnerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["restaurant","partner_user"]
