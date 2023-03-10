from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Destination = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    State = models.CharField(max_length=200, null=True, blank=True)
    City = models.CharField(max_length=200, null=True, blank=True)

    Category = models.CharField(max_length=200, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.Destination
    

class Review(models.Model):
    data = models.ForeignKey(Database, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Destination = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)