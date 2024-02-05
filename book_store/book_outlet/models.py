from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name}"


class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=6)

    def full_address(self):
        return f"{self.street}, {self.city}, {self.postal_code}"

    def __str__(self):
        return self.full_address()
    class Meta:
        verbose_name_plural = "Addresses"

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True) # One to One connection between author and address

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()
    

class Book(models.Model):
    title = models.CharField(max_length=50)
    rating= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    #One to Many : An author can have many books but a book should have one author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True) 
    is_bestselling = models.BooleanField(default=False)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    published_country = models.ManyToManyField(Country, null=True, related_name="books")

# This function is used to get Url for the single book detail page
    def get_absolute_url(self):
        return reverse("book-detail", args=[self.slug])
    
    # # This function overwrite the default save method
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title) #here we are transforming the string to slug using slugify function
    #     super().save(*args, **kwargs) #This enable to continue with the default save method

    def __str__(self):
        return f"{self.title} ({self.rating})"