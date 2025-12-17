from django.shortcuts import render
from .models import TourPackage

def home(request):
    packages = TourPackage.objects.filter(is_active=True)
    return render(request, 'main/index.html', {
        'packages': packages
    })
