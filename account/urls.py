from django.conf.urls import url
from django.contrib.auth.views import login, logout

from account import views
from account.views import AddExpense

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^home', views.home, name='home'),
    url(r'^login', login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^report-user', views.reportUser, name='report_user'),
    url(r'^report-admin', views.reportAdmin, name='report_admin'),
    url(r'^new-user', views.newUser, name='new-user'),
    url(r'^new-expense', AddExpense.as_view(), name='new_expense'),
    url(r'^logout', logout, {'template_name': 'account/logout.html'}, name='logout'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^change-password', views.change_password, name='change_password'),
]
