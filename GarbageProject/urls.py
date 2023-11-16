"""GarbageProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from garbageapp.views import *

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard2/', dashboard2, name="dashboard2"),
    path('dashboard3/', dashboard3, name="dashboard3"),
    path('login_user/', login_user, name="login_user"),
    path('logout_user/', logout_user, name="logout_user"),
    path('registration/', registration, name="registration"),
    path('reg_user/', reg_user, name="reg_user"),
    path('login2_user/', login2_user, name="login2_user"),
    path('logout2_user/', logout2_user, name="logout2_user"),
    path('add_complain/', add_complain, name="add_complain"),
    path('complainlist/', complainlist, name="complainlist"),
    path('edit_complain/<int:pid>/', edit_complain, name="edit_complain"),
    path('delete_complain/<int:pid>/', delete_complain, name="delete_complain"),
    path('detail/<int:pid>/', detail, name="detail"),

    path('add_bin/', add_bin, name="add_bin"),
    path('binlist/', binlist, name="binlist"),
    path('edit_bin/<int:pid>/', edit_bin, name="edit_bin"),
    path('delete_bin/<int:pid>/', delete_bin, name="delete_bin"),
    path('add_driver/', add_driver, name="add_driver"),
    path('driverlist/', driverlist, name="driverlist"),
    path('edit_driver/<int:pid>/', edit_driver, name="edit_driver"),
    path('delete_driver/<int:pid>/', delete_driver, name="delete_driver"),
    path('driver_login/', driver_login, name="driver_login"),
    path('user_profile/', user_profile, name="user_profile"),
    path('change_password/', change_password, name="change_password"),
    path('change_password2/', change_password2, name="change_password2"),
    path('change_password2/', change_password2, name="change_password2"),
    path('report/', report, name="report"),
    path('driverwise/', driverwise, name="driverwise"),
    path('driver_changhe_password/', driver_changhe_password, name="driver_changhe_password"),
    path('user_search/', user_search, name="user_search"),
    path('admincomplainlist/', admincomplainlist, name="admincomplainlist"),
    path('detail_driver/<int:pid>/', detail_driver, name="detail_driver"),
    path('driverbinlist/', driverbinlist, name="driverbinlist"),

    path('drivercomplainlist/', drivercomplainlist, name="drivercomplainlist"),
    path('complain_detail_driver/<int:pid>/', complain_detail_driver, name="complain_detail_driver"),
    path('search_complain/', search_complain, name="search_complain"),
    path('search_bin/', search_bin, name="search_bin"),
    path('report_search_bin/', report_search_bin, name="report_search_bin"),
    path('driverbin/', driverbin, name="driverbin"),
    path('search_complain_bin/', search_complain_bin, name="search_complain_bin"),
    path('complain_search_bin/', complain_search_bin, name="complain_search_bin"),
    path('search_complain_driver/', search_complain_driver, name="search_complain_driver"),
    path('delete_user/<int:pid>/',delete_user,name="delete_user")

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
