"""serfa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from serfa_panel.views import add_mes, profile_after_login, sensors, sensorview, addsensor, signup, activate, account_activation_sent, change_password, checkeverything


urlpatterns = [
    url(r'^$', auth_views.login, {'template_name': 'l_login.html'}, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^addmes/$', add_mes),
    url(r'^checkeve/$', checkeverything),
    url(r'^accounts/sensors/$', sensorview, name='sensorss'),
    url(r'^login/$', auth_views.login, {'template_name': 'l_login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^accounts/profile/$', profile_after_login, name='profile'),
    url(r'^accounts/change-password/$', change_password, name='changepassword'),
    url(r'^accounts/sensors-list/$', sensors, name='sensorslist'),
    url(r'^accounts/add-sensor/$', addsensor, name='addsensor'),
    url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

]
