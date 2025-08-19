from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ---------- Users & Profiles ----------
class CustomUser(AbstractUser):
    is_restaurant = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    kyc = models.BooleanField(default=False)
    attestation = models.BooleanField(default=False)
    def __str__(self): return self.username

class RestaurantProfile(models.Model):
    CURRENCY_CHOICES = [("EUR","EUR"),("USD","USD"),("RUB","RUB")]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="restaurant_profile")
    company_name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255, blank=True, default="")
    preferred_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="EUR")
    def __str__(self): return self.company_name

class SupplierProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="supplier_profile")
    company_name = models.CharField(max_length=255)
    categories = models.TextField(blank=True, default="")
    verified = models.BooleanField(default=False)
    is_farmer = models.BooleanField(default=False)
    country = models.CharField(max_length=64, blank=True, default="")
    def __str__(self): return self.company_name

class FarmerProfile(SupplierProfile):
    farm_name = models.CharField(max_length=255, blank=True, default="")
    organic_certified = models.BooleanField(default=False)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)

# ---------- Products & Media ----------
class Product(models.Model):
    CURRENCY_CHOICES = [("EUR","EUR"),("USD","USD"),("RUB","RUB")]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, default="kg")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="EUR")
    available_from = models.DateField()
    available_to = models.DateField(null=True, blank=True)
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="products")
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_available(self):
        today = timezone.now().date()
        if self.available_to:
            return self.available_from <= today <= self.available_to
        return self.available_from <= today

    def display_price(self):
        symbol = {"EUR": "€", "USD": "$", "RUB": "₽"}.get(self.currency, "")
        return f"{symbol}{self.price_per_unit}"

    def __str__(self): return f"{self.name} ({self.category})"

class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="media")
    image = models.ImageField(upload_to='products/images/', null=True, blank=True)
    video = models.FileField(upload_to='products/videos/', null=True, blank=True)

# ---------- Orders & Offers ----------
class Order(models.Model):
    STATUS_CHOICES = [
        ("pending","Pending"),("accepted","Accepted"),
        ("assembling","Assembling"),("in_transit","In Transit"),
        ("delivered","Delivered"),("cancelled","Cancelled"),
    ]
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, related_name="orders")
    delivery_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)

class Offer(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="offers")
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="offers")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_eta = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["price","delivery_eta"]

# ---------- PreOrders (reserved-only in MVP) ----------
class PreOrder(models.Model):
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, related_name="preorders")
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="preorders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField()
    status = models.CharField(max_length=50, default="reserved")
    created_at = models.DateTimeField(auto_now_add=True)

# ---------- Calendar (both sides) ----------
class CalendarEvent(models.Model):
    EVENT_CHOICES = [("order","Order"),("preorder","PreOrder")]
    date = models.DateField()
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    preorder = models.ForeignKey(PreOrder, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    status = models.CharField(max_length=50, default="scheduled")

# ---------- Reviews (both sides) ----------
class Review(models.Model):
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="given_reviews")
    target = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_reviews")
    rating = models.IntegerField()
    comment = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="reviews/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# ---------- Favorites (partners) ----------
class FavoritePartner(models.Model):
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, related_name="favorites")
    partner_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="favored_by")
    created_at = models.DateTimeField(auto_now_add=True)

# ---------- Waitlist ----------
class ProductWaitlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="waitlist")
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)
    desired_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# ---------- Subscriptions (Phase 2 ready) ----------
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.JSONField(default=dict)

class UserSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
