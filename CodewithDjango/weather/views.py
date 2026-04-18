from django.shortcuts import render
from .models import WeatherData

# Create your views here.
def all_weather(request):
    weather = WeatherData.objects.all()
    return render(request, 'weather/all_weather.html', {'weather': weather})