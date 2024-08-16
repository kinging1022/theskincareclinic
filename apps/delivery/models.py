from django.db import models

# Create your models here.
class Location(models.Model):
    location = models.CharField(max_length=225)


    def __str__(self) -> str:
        return self.location
    
class Area (models.Model):
    location = models.ForeignKey(Location, related_name='areas' , on_delete=models.CASCADE)
    area = models.CharField(max_length=225)

    def __str__(self) -> str:
        return self.area
    


class DeliveryPrice(models.Model):
    location = models.ForeignKey(Area ,on_delete=models.CASCADE)
    weight_from = models.DecimalField(max_digits=10, decimal_places=2)
    weight_to = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f" {self.location} - {self.weight_from} kg - {self.weight_to} kg"