from django.db import models
class signinm(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    cart=models.IntegerField(default=0,blank=True,null=True)
    items = models.JSONField(default=list)
class loginm(models.Model):
    email=models.EmailField(max_length=100)
class buy(models.Model):
    c=[('One-time order','One-time order'), ('Daily subscription - save 15%','Daily subscription - save 15%'),('Alternate day subscription - save 10%','Alternate day subscription - save 10%'),('Business supply quotation','Business supply quotation')]
    b=[('1 bottle','1 bottle'),('2 bottles','2 bottles'),('4 bottles','4 bottles'),('10 bottles - bulk','10 bottles - bulk')]
    add=models.CharField(max_length=100)
    order=models.CharField(max_length=100,choices=c)
    quantity=models.CharField(max_length=100,choices=b)
