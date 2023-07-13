from django.db import models
from django.utils import timezone
from .utils import get_random_filename
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.conf import settings


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

    title_en = models.CharField(max_length=200)
    title_tr = models.CharField(max_length=200)
    title_no = models.CharField(max_length=200)
    
    content_en = models.TextField()
    content_tr = models.TextField()
    content_no = models.TextField()
    
    tags_en = models.CharField(max_length=200)
    tags_tr = models.CharField(max_length=200)
    tags_no = models.CharField(max_length=200)

    slug_en = models.SlugField(unique=True, blank=True)
    slug_tr = models.SlugField(unique=True, blank=True)
    slug_no = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    blog_image = models.ImageField(upload_to=get_random_filename)
    image_filter = models.CharField(
        max_length=255, choices=FILTER_CHOICES, default='none', null=True)
    status = models.CharField(max_length=255, choices=[(
        'draft', 'Draft'), ('published', 'Published')], default='draft')
    pub_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title_en

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug_en = slugify(self.title_en)
            self.slug_tr = slugify(self.title_tr)
            self.slug_no = slugify(self.title_no)
        else:
            self.slug_en = self.get_unique_slug('slug_en', self.title_en)
            self.slug_tr = self.get_unique_slug('slug_tr', self.title_tr)
            self.slug_no = self.get_unique_slug('slug_no', self.title_no)

        if self.status == 'published' and not self.pub_date:
            self.pub_date = timezone.now()
        
        if self.pk:
            old_blog = Blog.objects.get(pk=self.pk)
            if old_blog.blog_image.name != self.blog_image.name:
                if default_storage.exists(old_blog.blog_image.name):
                    default_storage.delete(old_blog.blog_image.name)

        super().save(*args, **kwargs)

    def get_unique_slug(self, slug_field, title):
        unique_slug = slugify(title)
        counter = 1
        while Blog.objects.filter(**{slug_field: unique_slug}).exclude(id=self.id).exists():
            unique_slug = f"{slugify(title)}-{counter}"
            counter += 1
        return unique_slug
    

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=False) 


    def __str__(self):
        return self.text[:50]

