from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField( max_digits=50, decimal_places=2)
    color = models.CharField(max_length=20)
    brand = models.CharField(max_length=100)
    make_country = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.price} {self.price}"