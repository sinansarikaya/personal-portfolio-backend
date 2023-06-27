from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from pathlib import Path

from .models import Blog

@receiver(post_delete, sender=Blog)
def delete_blog_image(sender, instance, **kwargs):
    if instance.blog_image:
        img_path = Path(settings.MEDIA_ROOT) / instance.blog_image.path
        if img_path.is_file():
            img_path.unlink()
