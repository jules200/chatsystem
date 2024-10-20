from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, phone, first_name, last_name, profile_image, password):
        if not email:
            raise ValueError("Email is required")
        if not phone:
            raise ValueError("Phone is required")
        if not first_name:
            raise ValueError("First Name is required")
        if not last_name:
            raise ValueError("Last Name is required")

        user = self.model(
            email=self.normalize_email(email),
            phone = phone,
            first_name = first_name,
            last_name = last_name,
            profile_image=profile_image,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, phone, first_name, last_name, password):
        user = self.model(
            email=self.normalize_email(email),
            phone = phone,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user 


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", unique=True)
    phone = models.CharField(max_length=20)
    profile_image = models.ImageField(max_length=100, upload_to='uploads/', null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','first_name','last_name']

    objects =MyAccountManager()

    def __str__ (self):
        return self.first_name + "/ " + self.last_name

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser or super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return self.is_superuser
