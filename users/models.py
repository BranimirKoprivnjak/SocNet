import PIL.Image as Image

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
#https://django-ratelimit.readthedocs.io/en/stable/

class UserManager(BaseUserManager):
    def create_user(self, identifier, email, password):
        if not identifier or not email:
            raise ValueError('Identifier and/or Email missing!')
        user = self.model(
            identifier = identifier,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, email, password):
        user = self.create_user(
            identifier,
            email,
            password=password
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    identifier = models.CharField(
        #human-readable name
        verbose_name = 'username',
        max_length=30,
        unique=True)
    email = models.EmailField(max_length=50, unique = True)
    name = models.CharField(max_length=35, blank=True, null=True)
    profile_info = models.TextField(max_length = 1000, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['password', 'email']
    #EMAIL_FIELD --> defaults to email

    def __str__(self):
        return self.identifier

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
        picture = Image.open(self.profile_pic)
        picture = picture.resize((150, 150), Image.ANTIALIAS)
        picture.save(self.profile_pic.path)


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse('users:login')

    @property
    def is_staff(self):
        return self.is_superuser

class Follower(models.Model):
    user = models.ForeignKey(User, related_name='following', null=True, on_delete=models.SET_NULL)
    follower = models.ForeignKey(User, related_name='follower', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.identifier

    class Meta:
        unique_together = ("user", "follower")
