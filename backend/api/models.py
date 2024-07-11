from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.html import mark_safe
from django.utils.text import slugify

from shortuuid.django_fields import ShortUUIDField
import shortuuid


class User(AbstractUser):
    username = models.CharField(unique=True , max_length=100)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
   
    USERNAME_FIELD ='email' #USERNAME_FIELD : Définit le champ utilisé comme identifiant unique pour l'authentification. Ici, il est défini comme email au lieu du username par défaut.
    REQUIRED_FIELDS = ['username'] #: Liste des champs supplémentaires requis lors de la création d'un superutilisateur. Ici, le username est requis.
    
    def __str__(self):
        return self.username
    
    
    def save(self, *args , **kwargs):
        email_username , mobile = self.email.split("@")
        if self.fullname == "" or self.fullname == None : #Si fullname est vide ou nul, il est défini à email_username
            self.fulname = email_username
            
        if self.username == "" or self.username == None: #Si username est vide ou nul, il est défini à email_username.
            self.username = email_username
         
        super(User).save(*args , **kwargs)
    

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=CASCAD)
    image = models.FileField(upload_to=user_image , default="default/default-user.png " , null=True , blank=True)
    full_name = models.CharField(max_length=100 , blank=True,null = True)
    bio = models.CharField(max_length=100 , blank=True,null = True)
    about = models.CharField(max_length=100 , blank=True,null = True)
    author = models.BooleanField(default=False)
    country = models.CharField(max_length=100 , blank=True,null = True)
    facebook = models.CharField(max_length=100 , blank=True,null = True)
    twitter = models.CharField(max_length=100 , blank=True,null = True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args , **kwargs):
        email_username , mobile = self.email.split("@")
        if self.fullname == "" or self.fullname == None : #Si fullname est vide ou nul, il est défini à email_username
            self.fulname = email_username
            
        if self.username == "" or self.username == None: #Si username est vide ou nul, il est défini à email_username.
            self.username = email_username
         
        super(User).save(*args , **kwargs)
    