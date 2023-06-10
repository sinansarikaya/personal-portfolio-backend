from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    image = models.ImageField(upload_to='profile/', default='media/profile/avatar.png')
    about = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name
