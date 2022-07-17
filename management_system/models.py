
from django.db import models
import datetime


class Client(models.Model):
    CLIENT_STATUS =  [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(max_length=500)
    contact_number = models.IntegerField()
    email_address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=CLIENT_STATUS, default='active')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}".capitalize()


class Category(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"{self.name}".capitalize()


class Item(models.Model):
    item = models.CharField(max_length=255)
    serial_number = models.IntegerField()
    model = models.CharField(max_length=255)
    appraise_value = models.DecimalField(max_digits=10, decimal_places=2)
    item_description = models.CharField(max_length=255, blank=True, null=True)
    category = models.ManyToManyField(
        Category, blank=True, related_name="categories")
    remarks = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    

    def __str__(self) -> str:
        return f"{self.item}-{self.id}".capitalize()


class Transaction(models.Model):
    STATUS_CHOICE = [
        ('New', 'New'),
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Renew','Renew'),
    ]
    client = models.ForeignKey(Client, related_name='clients', on_delete=models.CASCADE) 
    item = models.ForeignKey(Item, related_name='items', on_delete=models.CASCADE)
    interest_rate = models.PositiveIntegerField()
    date_pawned = models.DateField(auto_now_add=True)
    month = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='New')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def due_date(self):
        month = datetime.timedelta(self.month*30)
        due_date = self.date_pawned + month
        return due_date


    def total(self):
        interest_rate = float(self.interest_rate) / 100
        interest = float(self.item.appraise_value) * interest_rate
        total = float(self.item.appraise_value) + interest
        return total
    
    def interest_amount(self):
        interest_rate = float(self.interest_rate) / 100
        return float(self.item.appraise_value) * interest_rate


    def __str__(self) -> str:
        return f"Date Pawned: {self.date_pawned}--Client: {self.client}-- Item: {self.item}"
    
