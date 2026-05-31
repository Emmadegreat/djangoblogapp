from .models import Category
from django.conf import settings

def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)

def get_whatsapp_number(request):
    return {
        'whatsapp_number': settings.WHATSAPP_NUMBER
    }