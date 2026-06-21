from django.db import models
from django.contrib.auth.models import User
class sellm(models.Model):
    #('Fresh Milk','Fresh Milk'),('Pure Ghee','Pure Ghee'),('Paneer & Cheese','Paneer & Cheese'),('Curd & Yogurt','Curd & Yogurt'),('Butter & Cream','Butter & Cream'),('Family Combo','Family Combo')
    c=[('Fresh Milk','Fresh Milk'),('Pure Ghee','Pure Ghee'),('Paneer & Cheese','Paneer & Cheese'),('Curd & Yogurt','Curd & Yogurt'),('Butter & Cream','Butter & Cream'),('Family Combo','Family Combo')]
    s=[('In stock','In stock'),('Only few left','Only few left'),('Out of stock','Out of stock'),('Pre-order','Pre-order')]
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    category=models.CharField(max_length=100,choices=c)
    sku=models.CharField(max_length=100)
    short_description=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    main_image=models.ImageField(upload_to='images/')
    gallery_1=models.ImageField(upload_to='images/')
    gallery_2=models.ImageField(upload_to='images/')
    gallery_3=models.ImageField(upload_to='images/')
    video_url=models.URLField(max_length=200,blank=True,null=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    mrp=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.IntegerField()
    stock_status=models.CharField(max_length=100,choices=s)
    badge=models.CharField(max_length=100)
    tax_info=models.CharField(max_length=100)
    size=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    ingredients=models.CharField(max_length=100)
    shelf_life=models.CharField(max_length=100)
    packaging=models.CharField(max_length=100)
    allergen=models.CharField(max_length=100)
    highlights=models.CharField(max_length=100)
    delivery_area=models.CharField(max_length=100)
    delivery_slot=models.CharField(max_length=100)
    return_policy=models.CharField(max_length=100)
    business_minimum=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100, unique=True,blank=True,null=True)
    seller=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

class signins(models.Model):
    seller_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.IntegerField()
    location=models.CharField(max_length=100)
    gst_number=models.CharField(max_length=100, blank=True,null=True)

class logins(models.Model):
    email=models.EmailField(max_length=100)

