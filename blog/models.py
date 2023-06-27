from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .utils import get_random_filename
from django.utils.text import slugify
from django.core.files.storage import default_storage


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    FILTER_CHOICES = (
        ('none', 'None'),
        ('blur', 'Blur'),
        ('brightness', 'Brightness'),
        ('contrast', 'Contrast'),
        ('grayscale', 'Grayscale'),
        ('huerotate', 'Huerotate'),
        ('invert', 'Invert'),
        ('opacity', 'Opacity'),
        ('saturate', 'Saturate'),
        ('sepia', 'Sepia'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    blog_image = models.ImageField(upload_to=get_random_filename)
    image_filter = models.CharField(
        max_length=255, choices=FILTER_CHOICES, default='none', null=True)
    status = models.CharField(max_length=255, choices=[(
        'draft', 'Draft'), ('published', 'Published')], default='draft')
    tags = models.CharField(max_length=255, null=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255, null=True)  # SEO Url

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_blog_image = self.blog_image

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        unique_slug = self.slug
        counter = 1
        while Blog.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
            unique_slug = f"{self.slug}-{counter}"
            counter += 1

        self.slug = unique_slug

        if self.status == 'published' and not self.pub_date:
            self.pub_date = timezone.now()
        
        if self.pk:
            old_blog = Blog.objects.get(pk=self.pk)
            if old_blog.blog_image.name != self.blog_image.name:
                if default_storage.exists(old_blog.blog_image.name):
                    default_storage.delete(old_blog.blog_image.name)

        super().save(*args, **kwargs)
