from django.db import models

# Create your models here.
class UserProfile(models.Model):
    image = models.FileField(upload_to="images")

    # instead of FileField we can use ImageFiled for image only upload file for that to work we have to install pip install pillow.