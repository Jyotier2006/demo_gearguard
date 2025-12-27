"""registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from app1 import views
from django.urls import path
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('create_account/', views.create_account, name='create_account'),
    path("maintainance/", views.maintainance, name="maintainance"),
    path("equipment/", views.equipment, name="equipment"),
    path("maintainance/<int:id>/", views.maintainance_detail, name="maintainance_detail"),
    path('logout/', views.logout_user, name='logout'),
    path('create-account/', views.create_account, name='create_account'),  
    path("dashboard/", views.dashboard, name="dashboard"),
    path("maintenance_calendar/", views.maintenance_calendar, name="maintenance_calendar"),
    path("reporting/", views.reporting, name="reporting"),
    path("teams/", views.teams, name="teams"),
    path("home/", views.home, name="home"),
    path("maintenance-calendar/", views.maintenance_calendar, name="maintenance_calendar"),
    path("api/calendar/events/", views.calendar_events, name="calendar_events"),
    path("api/calendar/events/<int:pk>/update/", views.calendar_event_update, name="calendar_event_update"),
    path("api/calendar/events/create/", views.calendar_event_create, name="calendar_event_create"),
]