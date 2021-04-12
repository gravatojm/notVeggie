from django.contrib.auth.models import User
from .models import Prato, Reserva, Evento
from django.contrib.auth import authenticate, login, logout
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class PratoForm(forms.ModelForm):
    class Meta:
        model = Prato
        fields = ['nome', 'preco']


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data', 'hora', 'n_lugares', 'nome_cliente', 'contacto']


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data', 'hora', 'n_lugares', 'contacto']
