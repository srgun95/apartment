from datetime import date, time, datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from picklefield import PickledObjectField


class Month(models.Model):
    month_name = models.IntegerField(_("Month"), default=date.today().month)
    actual_amount = models.IntegerField(default=0)
    amount_spent = models.IntegerField(default=0)
    user_spent_list = PickledObjectField()
    common_money = PickledObjectField()


class UserProfile(models.Model):
    user_id = models.IntegerField()
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='Unnamed')
    mobile_number = models.IntegerField(default='00000000')

    def __str__(self):
        return self.name


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user_name=kwargs['instance'], name=kwargs['instance'].first_name,
                                                  user_id=kwargs['instance'].id)


post_save.connect(create_profile, sender=User)
