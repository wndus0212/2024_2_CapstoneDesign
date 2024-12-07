from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
    id = models.AutoField(primary_key=True, blank=True)
    google_id = models.TextField(unique=True)
    email = models.TextField(unique=True)
    username = models.TextField(blank=True, null=True)
    profile_picture = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    password = models.CharField(max_length=128, default="")

    USERNAME_FIELD='google_id'
    REQUIRED_FIELDS = ['email']
    USER_ID_FIELD = 'id'

    class Meta:
        managed = True
        db_table = 'Users'
