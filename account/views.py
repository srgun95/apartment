from datetime import date, datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from account.forms import EditProfileForm, NewUserForm, ExpenseForm
from account.models import Month


class AddExpense(TemplateView):
    template_name = 'account/new-expense.html'

    def get(self, request):
        form = ExpenseForm()
        form.fields['user_name'].initial = request.user
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ExpenseForm(request.POST)
        if form.is_valid():
            month_obj = Month.objects.get(month_name=form.cleaned_data['date_spent'].month)
            month_obj.actual_amount += form.cleaned_data['amount']
            month_obj.amount_spent += form.cleaned_data['amount']
            current = [form.cleaned_data['user_name'],
                       form.cleaned_data['amount'],
                       form.cleaned_data['purpose'],
                       form.cleaned_data['date_spent'],
                       form.cleaned_data['description'],
                       datetime.now()]
            if month_obj.common_money == "" and month_obj.user_spent_list == "":
                month_obj.common_money = {}
                month_obj.user_spent_list = {}

            if form.cleaned_data['user_name'] == 'admin':  # Warning
                print(form.cleaned_data['name'])
                if not (int(form.cleaned_data['name'])):  # 1 for common
                    form.cleaned_data['user_name'] = 'common'
                    month_obj.actual_amount += form.cleaned_data['amount']
                    if form.cleaned_data['user_name'] in month_obj.common_money:  # user name will be set as common

                        print(month_obj.common_money)
                        month_obj.common_money[form.cleaned_data['user_name']].append(current)

                    else:

                        month_obj.common_money[form.cleaned_data['user_name']] = [current]
                else:  # o for user
                    # print("Hiii"+strcurrent)
                    current[0] = dict(form.fields['name'].choices)[int(form.cleaned_data['name'])]
                    month_obj.amount_spent += form.cleaned_data['amount']
                    if form.cleaned_data['user_name'] in month_obj.common_money:  # user name will be set as common
                        month_obj.common_money[form.cleaned_data['user_name']].append(current)
                    else:
                        month_obj.common_money[form.cleaned_data['user_name']] = [current]
            else:  # user adding money
                month_obj.actual_amount += form.cleaned_data['amount']
                month_obj.amount_spent += form.cleaned_data['amount']
                if form.cleaned_data['user_name'] in month_obj.user_spent_list:
                    month_obj.user_spent_list[form.cleaned_data['user_name']].append(current)
                else:
                    month_obj.user_spent_list[form.cleaned_data['user_name']] = [current]

            print("common money" + str(month_obj.common_money))
            print("User spent list " + str(month_obj.user_spent_list))
            month_obj.save()
        return render(request, 'account/home.html')


def checkAdmin(user):
    a = user.is_superuser
    return a


@login_required(login_url='/account/')
def home(request):
    return render(request, 'account/home.html', {'name': 'raghu'})


def reportUser(request):
    return render(request, 'account/report-user.html', {'name': 'reportUser'})


@user_passes_test(checkAdmin, login_url='/account/')
def reportAdmin(request):
    month = Month.objects.get(month_name=5)   # need to code
    args = {'actual': month.actual_amount, 'spent': month.amount_spent,
            'yetto': int(month.actual_amount) - int(month.amount_spent),
            'count': month.actual_amount / len(month.user_spent_list),
            'common': month.common_money['common'],
            'user_money': month.user_spent_list,
            }

    return render(request, 'account/report-admin.html', args)


@user_passes_test(checkAdmin, login_url='/account/')
def newUser(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account/home')
    else:
        form = NewUserForm()
    args = {'form': form}
    return render(request, 'account/new-user.html', args)


def newExpense(request):
    return render(request, 'account/new-expense.html', {'name': 'newUser'})


def welcome(request):
    return render(request, 'account/welcome.html', {'name': 'newUser'})


def profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/account/home')
    else:
        form = EditProfileForm(instance=request.user)
    args = {'form': form}
    return render(request, 'account/edit-profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            # update_session_auth_hash(request,form.user)
            form.save()
            update_session_auth_hash(request, form.user)  # Need to put this line here to get data after save

            return redirect('/account/profile')
    else:
        form = PasswordChangeForm(user=request.user)
    args = {'form': form}
    return render(request, 'account/change-password.html', args)
