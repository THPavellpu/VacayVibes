from django.db import models

class TourPackage(models.Model):
    # Use slug keys for internal storage and human-friendly labels for display
    CATEGORY_CHOICES = [
        ('beach', 'Beach'),
        ('mountain', 'Mountain'),
        ('historical', 'Historical Sites'),
        ('lakes', 'Lakes & River'),
        ('nature', 'Nature & Wildlife'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    # We keep `duration` for backward compatibility, but prefer explicit fields
    # `days` and `nights` which will be displayed on the site and editable from admin.
    duration = models.CharField(max_length=50, blank=True, null=True)   # e.g. "3 Days 2 Nights"
    days = models.PositiveIntegerField(default=0)
    nights = models.PositiveIntegerField(default=0)
    people = models.CharField(max_length=50)     # e.g. "2-6 People"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='packages/')
    inclusions = models.ManyToManyField('Inclusion', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Inclusion(models.Model):
    """Individual include items that can be attached to a TourPackage via a M2M."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = 'Inclusion'
        verbose_name_plural = 'Inclusions'

    def __str__(self):
        return self.name


class Lead(models.Model):
    """Stores leads from booking or newsletter subscriptions."""
    SOURCE_CHOICES = [
        ('book', 'Book Now'),
        ('subscribe', 'Subscribe'),
        ('contact', 'Contact Form'),
    ]

    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    package = models.ForeignKey(TourPackage, null=True, blank=True, on_delete=models.SET_NULL)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='book')
    utm_source = models.CharField(max_length=200, blank=True)
    utm_medium = models.CharField(max_length=200, blank=True)
    utm_campaign = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.source})"
