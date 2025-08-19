from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core import models
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = "Seed demo data for RestockHub"

    def handle(self, *args, **options):
        restaurant_u, _ = User.objects.get_or_create(username="demo_restaurant", defaults={"email": "resto@example.com"})
        restaurant_u.set_password("demo12345"); restaurant_u.is_restaurant=True; restaurant_u.save()

        supplier_u, _ = User.objects.get_or_create(username="demo_supplier", defaults={"email": "supplier@example.com"})
        supplier_u.set_password("demo12345"); supplier_u.is_supplier=True; supplier_u.save()

        farmer_u, _ = User.objects.get_or_create(username="demo_farmer", defaults={"email": "farmer@example.com"})
        farmer_u.set_password("demo12345"); farmer_u.is_supplier=True; farmer_u.save()

        resto, _ = models.RestaurantProfile.objects.get_or_create(user=restaurant_u, defaults={
            "company_name":"La Piccola Cucina","manager_name":"Chef Marco","preferred_currency":"EUR"
        })
        supplier, _ = models.SupplierProfile.objects.get_or_create(user=supplier_u, defaults={
            "company_name":"FreshSea Ltd","categories":"рыба, морепродукты","verified":True,"is_farmer":False
        })
        farmer, _ = models.FarmerProfile.objects.get_or_create(user=farmer_u, defaults={
            "company_name":"BerryFields","farm_name":"BerryFields Farm","organic_certified":True,"verified":True,"is_farmer":True
        })

        today=date.today()
        p1,_=models.Product.objects.get_or_create(name="Лосось свежий",category="Рыба",unit="kg",
            price_per_unit=18.50,currency="EUR",available_from=today- timedelta(days=1),supplier=supplier,verified=True)
        p2,_=models.Product.objects.get_or_create(name="Говядина премиум",category="Мясо",unit="kg",
            price_per_unit=14.90,currency="EUR",available_from=today- timedelta(days=1),supplier=supplier,verified=True)
        p3,_=models.Product.objects.get_or_create(name="Клубника",category="Фрукты и ягоды",unit="kg",
            price_per_unit=5.20,currency="EUR",available_from=today+ timedelta(days=20),available_to=today+timedelta(days=50),
            supplier=farmer,verified=True)

        order=models.Order.objects.create(restaurant=resto,delivery_date=today+timedelta(days=2),status="pending")
        models.OrderItem.objects.create(order=order,product=p1,quantity=5,unit_price_snapshot=p1.price_per_unit)
        models.OrderItem.objects.create(order=order,product=p2,quantity=8,unit_price_snapshot=p2.price_per_unit)

        models.Offer.objects.create(order=order,supplier=supplier,
            price=(5*p1.price_per_unit+8*p2.price_per_unit)*0.98,delivery_eta=today+timedelta(days=2))

        preorder=models.PreOrder.objects.create(restaurant=resto,supplier=farmer,product=p3,quantity=10,delivery_date=today+timedelta(days=25))

        models.CalendarEvent.objects.create(date=order.delivery_date,restaurant=resto,supplier=supplier,order=order,event_type="order",status="scheduled")
        models.CalendarEvent.objects.create(date=preorder.delivery_date,restaurant=resto,supplier=farmer,preorder=preorder,event_type="preorder",status="scheduled")

        models.Review.objects.create(reviewer=restaurant_u,target=supplier_u,rating=5,comment="Отличная свежая рыба!")
        models.Review.objects.create(reviewer=supplier_u,target=restaurant_u,rating=5,comment="Быстрая приёмка, всё чётко.")

        models.FavoritePartner.objects.get_or_create(restaurant=resto,partner_user=supplier_u)
        models.ProductWaitlist.objects.get_or_create(product=p3,restaurant=resto,desired_quantity=12)

        self.stdout.write(self.style.SUCCESS("Seed completed. Users: demo_restaurant/demo12345, demo_supplier/demo12345, demo_farmer/demo12345"))
