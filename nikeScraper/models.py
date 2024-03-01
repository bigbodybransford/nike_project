from django.db import models
from django.utils import timezone

# Create your models here.
class Shoes(models.Model):
 category = models.CharField(max_length=150)
 name = models.CharField(max_length=150)
 price = models.DecimalField(max_digits=10, decimal_places=2)
 description = models.TextField()

 def __str__(self):
  return (f" {self.category} - {self.name} - {self.price} |")