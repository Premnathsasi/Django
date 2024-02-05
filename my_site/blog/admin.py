from django.contrib import admin
from .models import Post, Author, Tag, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "author"]
    prepopulated_fields = {"slug": ["title"]}

class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email_address"]

class TagAdmin(admin.ModelAdmin):
    list_display = ["caption"]

admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)