from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        # Manually creating superuser, so manually checking are we doing properly.
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        # For creating superuser we will ask email,user_name,password
        return self.create_user(email, user_name, password, **other_fields)
    
    def create_user(self, email, user_name, password, **other_fields):
        # Creating normal user.
        if not email:
            raise ValueError(_("You must provide an email address"))
        
        email = self.normalize_email(email)
        # self.model referes to UserBase model
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
# Create your models here.
class UserBase(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(('about'), max_length=500, blank=True)
    # Delivery details
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    # User status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.user_name
