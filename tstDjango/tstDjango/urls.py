"""tstDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django_web.views import index
from django_web.views import chart
from django_web.views import chart2
from django_web.views import map
from django_web.views import slatter
from django_web.views import tables
from django_web.views import charts
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^index/', index),
    url(r'^chart/',chart),
    url(r'^chart2/',chart2),
    url(r'^map/',map),
    url(r'^tables/',tables),
    url(r'^charts/',charts)
]
