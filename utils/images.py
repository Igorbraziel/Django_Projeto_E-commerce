from PIL import Image
from pathlib import Path
from django.conf import settings

def resize_image(django_image, new_width=800, optimize=True, quality=70):
    django_image_path = Path(settings.MEDIA_ROOT / django_image.name).resolve()
    pillow_image = Image.open(django_image_path)
    
    current_width, current_height = pillow_image.size
    
    if current_width <= new_width:
        pillow_image.close()
        return pillow_image
    
    new_height = round(current_height * new_width / current_width)
    
    pillow_image = pillow_image.resize(size=(new_width, new_height))
    
    pillow_image.save(
        django_image_path,
        optimize=optimize,
        quality=quality,
    )
    
    return pillow_image