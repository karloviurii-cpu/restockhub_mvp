from django.contrib import admin
from . import models
for m in [
    models.CustomUser, models.RestaurantProfile, models.SupplierProfile, models.FarmerProfile,
    models.Product, models.ProductMedia, models.Order, models.OrderItem, models.Offer,
    models.PreOrder, models.CalendarEvent, models.Review, models.ProductWaitlist,
    models.SubscriptionPlan, models.UserSubscription, models.FavoritePartner
]:
    try:
        admin.site.register(m)
    except Exception:
        pass
