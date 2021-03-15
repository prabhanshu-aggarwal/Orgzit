from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser ,PermissionsMixin
)

# Create your models here.
class RegistrationManager(BaseUserManager):
    def create_user(self, email, title, description, time, status, created_date, modified_date,password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            title=title,
            description = description,
            time =time,
            status= status,
            created_date=created_date,
            modified_date=modified_date
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self,email, title, description, time, status, created_date, modified_date,password):

        user = self.create_user(
            email,
            title=title,
            password=password,
            description=description,
            time=time,
            status=status,
            created_date=created_date,
            modified_date=modified_date
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self,email, title, description, time, status, created_date, modified_date,password):

        user = self.create_user(
            email,
            title=title,
            password=password,
            description=description,
            time=time,
            status=status,
            created_date=created_date,
            modified_date=modified_date
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user



class Registration(AbstractBaseUser, PermissionsMixin):

    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'InProgress'),
        (3, 'Completed'),
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    time = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False) # a superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['title','description','time','status','created_date', 'modified_date']

    objects = RegistrationManager()

    def get_full_name(self):
        # The user is identified by their title
        return self.title

    def get_short_name(self):
        # The user is identified by their title
        return self.title

    def __str__(self):              # __unicode__ on Python 2
        return self.title

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_user_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_user_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_user_active(self):
        "Is the user active?"
        return self.active
