from django.db import models
from django.utils import timezone

# Create your models here.

class WeatherData(models.Model):
    WEATHER_TYPE =[
        ('Sunny', 'Sunny'),
        ('Cloudy', 'Cloudy'),
        ('Rainy', 'Rainy'),
        ('Snowy', 'Snowy'),
    ]
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    weather_type = models.CharField(max_length=20, choices=WEATHER_TYPE)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='weather_images/')

    def __str__(self):
        return self.name






