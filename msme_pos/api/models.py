from django.db import models
from django.contrib.auth import get_user_model
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

        user.full_business_name = user.get_full_name()

        # `set_password` hashes the given password
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, owner_surname, owner_given_name, password, business_name=None, identifier=None):
        """ Creates and saves a superuser """

        business_name = 'app'
        identifier = 'admin'

        user = self.create_user(
            email, business_name, identifier,
            owner_surname, owner_given_name, password
        )

        user.full_business_name = user.get_full_name()
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
    full_business_name = models.CharField(max_length=255, unique=True)

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
        """ Used to get a user's business name and identifier"""

        return '{}-{}'.format(self.business_name, self.identifier)

    def get_short_name(self):
        """ Used to get a user's name """
        
        return '{}, {}'.format(self.owner_surname, self.owner_given_name)

    def get_email(self):
        """ Used to get a user's email """
        
        return self.email

    def __str__(self):
        """ business_name-identifier """ 

        return self.get_full_name()


class MenuItem(models.Model):
    """ User's menu items """

    name = models.CharField(max_length=255, blank=False, unique=True)
    url_param_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey('UserProfile', related_name='menu_items', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.url_param_name = self.name.replace(' ', '-').lower()
        super(MenuItem, self).save(*args, **kwargs)

    def __str__(self):
        
        return self.name


class ItemOrder(models.Model):
    """ ItemOrder model """

    quantity = models.IntegerField()
    ordered_on = models.DateTimeField(auto_now_add=True)
    additional_notes = models.TextField(null=True)
    menu_item = models.ForeignKey('MenuItem', related_name='item_orders', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quantity) + ' orders of ' + self.menu_item.name + ' from ' + self.menu_item.user_profile.business_name

