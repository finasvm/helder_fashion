from django.db import models

# Create your models here.

class Products(models.Model):
    name= models.CharField(max_length=255)
    main_image=models.ImageField(upload_to='mainimage')
    price=models.IntegerField(default=0)
