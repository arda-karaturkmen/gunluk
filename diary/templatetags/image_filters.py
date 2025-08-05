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
            # URL'yi al
            url = image_field.url
            # URL'nin geçerli olduğundan emin ol
            if url and url.strip():
                return url
            return None
        except (ValueError, AttributeError, Exception):
            # Herhangi bir hata durumunda None döndür
            return None
    return None
