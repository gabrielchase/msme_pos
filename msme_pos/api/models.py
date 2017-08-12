from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


# Inherits and extends the Django base user manager 
class UserProfileManager(BaseUserManager):
    """ Helps Django work with out custom user """

    def create_user(self, email, business_name, identifier, owner_surname, owner_given_name, password, address=None, city=None, state=None):
        """ Create a new user profile object """
        
        if not email: 
            raise ValueError('Users must provide an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            business_name=business_name,
            identifier=identifier,
            owner_surname=owner_surname, 
            owner_given_name=owner_given_name, 
            address=address,
            city=city,
            state=state
        )

        # `set_password` hashes the given password
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, owner_surname, owner_given_name, password, business_name=None, identifier=None):
        """ Creates and saves a superuser """

        business_name = 'app'
        identifier = 'admin'

        user = self.create_user(email, business_name, identifier, owner_surname, owner_given_name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


# Inherits and extends the Django base user model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Represent a user profile in the application. """

    email = models.EmailField(max_length=255, unique=True)
    
    business_name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255, null=True)

    owner_surname = models.CharField(max_length=255)
    owner_given_name = models.CharField(max_length=255)
    
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['business_name', 'identifier', 'owner_surname', 'owner_given_name']

    def get_full_name(self):
        """ Used to get a user's business name """

        # return self.business_name + '-' + self.identifier
        return '{}-{}'.format(self.business_name, self.identifier)

    def get_short_name(self):
        """ Used to get a user's name """
        
        # return self.owner_surname + ', ' + self.owner_given_name
        return '{}, {}'.format(self.owner_surname, self.owner_given_name)

    def get_email(self):
        """ Used to get a user's email """
        
        return self.email

    def __str__(self):
        """ Business name: email """ 

        return self.get_full_name() + ': ' + self.get_short_name()
