from django import template
from django.conf import settings

register = template.Library()

@register.filter
def safe_image_url(image_field):
    """
    Güvenli bir şekilde ImageField URL'sini döndürür.
    Eğer resim yoksa veya geçersizse None döndürür.
    """
    if image_field and hasattr(image_field, 'name') and image_field.name:
        try:
            return image_field.url
        except ValueError:
            return None
    return None
