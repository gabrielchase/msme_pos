from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


# Inherits and extends the Django base user manager 
class UserProfileManager(BaseUserManager):
    """ Helps Django work with out custom user """

    def create_user(self, email, surname, given_name, password=None):
        """ Create a new user profile object """
        
        if not email: 
            raise ValueError('Users must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, surname=surname, given_name=given_name)

        # `set_password` hashes the given password
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, surname, given_name, password):
        """ Creates and saves a superuser """

        user = self.create_user(email, surname, given_name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


# Inherits and extends the Django base user model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Represent a user profile in the application. """

    email = models.EmailField(max_length=255, unique=True)
    given_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['given_name', 'surname']

    def get_full_name(self):
        """ Used to get a user's full name """

        return self.given_name + self.surname

    def get_short_name(self):
        """ Used to get a user's surname """

        return self.surname

    def __str__(self):
        return self.email

