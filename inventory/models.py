from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=10)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100 ,null=True,blank=True)
    UPIid = models.CharField(max_length=100)
    dlno = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    ownerName = models.OneToOneField(User,on_delete=models.CASCADE)
    GSTNo = models.CharField(max_length=100, null = True, blank = True)
    def __str__(self):
        return self.name

class medicines(models.Model):
    name = models.CharField(max_length=100)
    composition = models.CharField(max_length=200)
    quantity = models.IntegerField()
    purchasedPrice = models.FloatField(blank=True, null=True)
    batchNo = models.CharField(max_length = 100, blank = True, null = True)
    price = models.FloatField()
    expiryDate = models.DateField()
    HSN = models.CharField(max_length=100, null = True, blank = True)
    def __str__(self):
        return self.name

class bill(models.Model):
    meds = models.ForeignKey(medicines, on_delete=models.DO_NOTHING, null=True , blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.meds.name


class invoice(models.Model):
    name = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    subtotal = models.FloatField( blank=True, null=True)
    discount = models.FloatField(default=0)
    total = models.FloatField(default=0)
    meds = models.ManyToManyField(bill,null=True, blank=True)
    def __str__(self):
        return self.name

class backup(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name