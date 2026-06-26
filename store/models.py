from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class UserData(models.Model):
    """
    Simple profile-like model used by admin views.
    Kept in sync with auth.User via post_save signal.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userdata', null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email or (self.user.username if self.user else "UserData")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "User Data"

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    old_customer_name = models.CharField(max_length=200, null=True, blank=True)

    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    total = models.FloatField()
    payment_status = models.CharField(max_length=50, default="Pending")
    order_date = models.DateTimeField(auto_now_add=True)

    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.product_name
    

