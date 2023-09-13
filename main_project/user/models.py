from django.db import models
from admin1.models import *
from django.contrib.auth.models import User

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Products,on_delete=models.CASCADE )
    count=models.PositiveIntegerField(default=0)
    Total=models.PositiveBigIntegerField(default=0,null=True,blank=True)
    grand_total=models.PositiveBigIntegerField(default=0)

class Address(models.Model):
    Full_name = models.CharField(max_length=255)
    pinCode = models.PositiveIntegerField()
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    HouseName = models.CharField(max_length=150)
    landMark = models.CharField(max_length=150)
    aduser = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

class Order(models.Model):
    user_order = models.ForeignKey(User,on_delete=models.CASCADE)
    Product = models.ForeignKey(Products,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=10,decimal_places=2)
    Status = models.CharField(max_length=50)
    Qty = models.PositiveIntegerField()
    PaymentMethod = models.CharField(max_length=20)
    Date = models.DateField(auto_now_add=True)  