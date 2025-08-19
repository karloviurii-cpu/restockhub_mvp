from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views as core_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'products', core_views.ProductViewSet, basename='product')
router.register(r'orders', core_views.OrderViewSet, basename='order')
router.register(r'offers', core_views.OfferViewSet, basename='offer')
router.register(r'preorders', core_views.PreOrderViewSet, basename='preorder')
router.register(r'calendar', core_views.CalendarEventViewSet, basename='calendar')
router.register(r'reviews', core_views.ReviewViewSet, basename='review')
router.register(r'waitlist', core_views.ProductWaitlistViewSet, basename='waitlist')
router.register(r'favorites', core_views.FavoritePartnerViewSet, basename='favorites')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # логин/логаут
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]