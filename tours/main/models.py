from django.db import models

class TourPackage(models.Model):
    CATEGORY_CHOICES = [
        ('Family', 'Family'),
        ('Adventure', 'Adventure'),
        ('Luxury', 'Luxury'),
        ('Budget', 'Budget'),
        ('Friends', 'Friends'),
        ('Wildlife', 'Wildlife'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    duration = models.CharField(max_length=50)   # e.g. "3 Days 2 Nights"
    people = models.CharField(max_length=50)     # e.g. "2-6 People"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='packages/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
