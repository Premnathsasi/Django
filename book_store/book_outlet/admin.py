from django.contrib import admin
from .models import Book, Author, Address, Country

class BookAdmin(admin.ModelAdmin):
    list_display= ["title", "rating", "author", "slug", "is_bestselling"]
    prepopulated_fields = {"slug": ["title"]} # populate the slug field with the value entered in title field

class AuthorAdmin(admin.ModelAdmin):
    list_display= ["first_name", "last_name", "address"]

class AddressAdmin(admin.ModelAdmin):
    list_display = ["street", "city", "postal_code"]

class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]

# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Country, CountryAdmin)