from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(validators=[MinLengthValidator(10)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= 'products', null=True)

    def __str__(self):
        return f"{self.name} {self.description} {self.price} {self.category}"
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def total_cost(self):
        total_cost = sum(item.total_cost() for item in self.items.all())
        return total_cost
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"CartItem {self.product.name} - Quantity: {self.quantity}"
    
    def total_cost(self):
        return self.product.price * self.quantity