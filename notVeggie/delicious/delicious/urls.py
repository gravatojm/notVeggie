"""delicious URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from . import views

# for web services
from rest_framework import routers
from .views import PratoViewSet
from .views import ReservaViewSet
from .views import EventoViewSet
from .views import UserViewSet

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'pratos', PratoViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.base, name='index'),
    url(r'^base/', views.base, name='base'),
    url(r'^login/', views.loginView, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': 'index'}, name='logout'),
    url(r'^registo/', views.registo, name='registo'),
    url(r'^menu/', views.menu, name='menu'),
    url(r'^cliente/', views.cliente, name='cliente'),
    url(r'^administrador/', views.administrador, name='administrador'),
    url(r'^criarprato/', views.criarPrato, name='criar_prato'),
    url(r'^criarreserva/', views.criarReserva, name='criar_reserva'),
    # Wire up our API using automatic URL routing.
    url(r'^', include(router.urls)),
]
