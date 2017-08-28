from django.db import models


class MenuItem(models.Model):
    """ User's menu items """

    name = models.CharField(max_length=255, blank=False, unique=True)
    url_param_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey('user_profile.UserProfile', related_name='menu_items', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.url_param_name = self.name.replace(' ', '-').lower()
        super(MenuItem, self).save(*args, **kwargs)

    def __str__(self):
        
        return self.name

