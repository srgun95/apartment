from datetime import date

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import SelectDateWidget

from account.models import UserProfile


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = {
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2'
        }


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = {
            'password', 'email', 'first_name', 'last_name',
        }


class ExpenseForm(forms.Form):
    user_list = [(o.user_id, str(o.user_name)) for o in UserProfile.objects.all()]
    user_list.append(('0', 'common'))
    name = forms.ChoiceField(choices=user_list)
    user_name = forms.CharField()
    purpose = forms.CharField()
    date_spent = forms.DateField(widget=SelectDateWidget, initial=date.today())
    amount = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 22}))


def get_choices():
    user_list = UserProfile.objects.values_list('name', flat=True)
    choice_list = [['0', 'common']]
    count = 1
    for i in user_list:
        count += 1
        choice_list.append([str(count), i])
        return choice_list
