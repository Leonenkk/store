from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):#наследуемся от существующего класса и через upload_to добавляем новое необязательное поле
    image = models.ImageField(upload_to="users_images/", blank=True, null=True)
