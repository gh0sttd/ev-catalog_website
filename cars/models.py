from django.db import models
from django.conf import settings

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва бренду")
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Car(models.Model):
    brand = models.CharField(max_length=50, db_index=True)
    model = models.CharField(max_length=50, db_index=True)

# Типи приводів в машинах
    DRIVE_CHOICES = [
        ('AWD', 'Повний'),
        ('RWD', 'Задній'),
        ('FWD', 'Передній'),
    ]
    
    brand = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='cars')
    model = models.CharField(max_length=100)
    year  = models.PositiveBigIntegerField()
    
    # Характеристики
    battery_capacity = models.PositiveBigIntegerField(help_text="кВт·год")
    range_km = models.PositiveIntegerField(help_text="Запас ходу в км")
    power_kw = models.PositiveIntegerField(help_text="Потужність у кВт")
    acceleration_0_100 = models.FloatField(help_text="Час розгону до 100 км/год")
    drive_type  = models.CharField(max_length=3, choices=DRIVE_CHOICES)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cars_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year})"

class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name ='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ('user', 'car')

def __str__(self):
    return f"{self.user.username} - {self.car.model}"

class TestDriveRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    preferred_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.car.model}"
