from django.db import models
from apps.store.models import Product

# Create your models here.

class Order(models.Model):
   ORDERED = 'ordered' 
   SHIPPED = 'shipped'
   ARRIVED = 'arrived'

   STATUS_CHOICES = (
      (ORDERED,'Ordered'),
      (SHIPPED,'Shipped'),
      (ARRIVED,'Arrived'),
   )
   
   first_name = models.CharField(max_length=100)
   last_name = models.CharField(max_length=100)
   email = models.CharField(max_length=100)
   address = models.CharField(max_length=100)
   phone = models.CharField(max_length=225,blank=True, null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   
   paid = models.BooleanField(default=False)
   paid_amount = models.FloatField(blank=True, null=True)
   delivery_amount = models.FloatField(blank=True,null=True)
   transaction_ref = models.CharField(max_length=225,null=True,blank=True,editable=False)
   used_coupon = models.CharField(max_length=50, blank=True, null=True)
   shipped_date = models.DateTimeField(blank=True, null=True)
   status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)


   def __str__(self):
        return '%s' % self.first_name
   

   def get_total_quantity(self):
       return sum(int(item.quantity) for item in self.items.all())
   


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.DO_NOTHING)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)


    def __str__(self) -> str:
        return '%s' % self.id
