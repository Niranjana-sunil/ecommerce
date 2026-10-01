import uuid
from django.db import models
from cloudinary.models import CloudinaryField
#from django.contrib.auth.hashers import make_password,check_password

# Create your models here.

class Users(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=50)
    phone=models.IntegerField(max_length=10,)
    email=models.EmailField(unique=True)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username


class Product(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image=CloudinaryField("image",folder="product")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.id}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(Users,on_delete=models.CASCADE,related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Order(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    order = models.ForeignKey(Order,on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.product.name