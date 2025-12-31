from django.shortcuts import render
from .models import TourPackage
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.core.mail import send_mail
from .models import Lead

def home(request):
    packages_all = TourPackage.objects.filter(is_active=True)
    # Show only up to 6 packages on the landing page (2 rows of 3)
    packages = packages_all[:6]
    has_more = packages_all.count() > 6

    # Build destinations list from model choices so the frontpage cards are dynamic
    images = {
        'beach': 'https://res.cloudinary.com/dzi2c0noo/image/upload/v1765953265/samples/landscapes/beach-boat.jpg?w=600&q=80',
        'mountain': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80',
        'historical': 'https://res.cloudinary.com/dzi2c0noo/image/upload/v1765999286/historical-stonehenge_uknovr.jpg?w=600&q=80',
        'nature': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&q=80',
        'lakes': 'https://res.cloudinary.com/dzi2c0noo/image/upload/v1765999137/Views-of-Portage-Lakes-State-Park-_wfgass.jpg?w=600&q=80',
    }

    destinations = []
    for slug, label in TourPackage.CATEGORY_CHOICES:
        destinations.append({
            'slug': slug,
            'label': label,
            'image': images.get(slug, ''),
        })

    return render(request, 'main/index.html', {
        'packages': packages,
        'destinations': destinations,
        'has_more': has_more,
    })


def category_packages(request, category_slug):
    """Show packages for a given category slug (e.g. 'beach')."""
    packages = TourPackage.objects.filter(category=category_slug, is_active=True)
    category_label = dict(TourPackage.CATEGORY_CHOICES).get(category_slug, category_slug.title())

    return render(request, 'main/category_packages.html', {
        'packages': packages,
        'category_label': category_label,
        'category_slug': category_slug,
    })


def all_packages(request):
    """Show all active packages in a paginated / full list."""
    packages = TourPackage.objects.filter(is_active=True)
    return render(request, 'main/all_packages.html', {
        'packages': packages,
    })


def book(request):
    """Display booking form (GET) and accept booking leads (POST)."""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        package_id = request.POST.get('package_id')
        package = None
        if package_id:
            package = get_object_or_404(TourPackage, id=package_id)

        lead = Lead.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
            package=package,
            source='book'
        )

        # Notify staff via email (best-effort)
        subject = f"New booking lead: {lead.email}"
        body = f"Name: {lead.name}\nEmail: {lead.email}\nPhone: {lead.phone}\nPackage: {getattr(package, 'title', 'N/A')}\nMessage:\n{lead.message}"
        try:
            send_mail(subject, body, getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@localhost'), [getattr(settings, 'ADMIN_EMAIL', 'sales@yourdomain.com')])
        except Exception:
            # don't break user flow on email failure
            pass

        return redirect('thank_you')

    # GET
    package = None
    package_id = request.GET.get('package_id')
    if package_id:
        package = TourPackage.objects.filter(id=package_id).first()

    return render(request, 'main/book_form.html', {
        'package': package,
        'admin_whatsapp': getattr(settings, 'ADMIN_WHATSAPP', '+919872573812'),
    })


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name', '')
        lead = Lead.objects.create(email=email, name=name, source='subscribe')

        # optional notify
        try:
            send_mail(f"New subscription: {email}", f"Email: {email}", getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@localhost'), [getattr(settings, 'ADMIN_EMAIL', 'sales@yourdomain.com')])
        except Exception:
            pass

        return redirect('thank_you')

    return redirect('home')


def thank_you(request):
    return render(request, 'main/thank_you.html')
