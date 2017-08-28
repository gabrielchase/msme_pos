from django.db import models


class ItemOrder(models.Model):
    """ ItemOrder model """

    quantity = models.IntegerField()
    ordered_on = models.DateTimeField(auto_now_add=True)
    additional_notes = models.TextField(null=True)
    menu_item = models.ForeignKey('menu_item.MenuItem', related_name='item_orders', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quantity) + ' orders of ' + self.menu_item.name + ' from ' + self.menu_item.user_profile.business_name
