from .models import Prato, Reserva, Evento, Utilizador
from django.contrib.auth.models import User
from rest_framework import serializers

class PratoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prato
        fields = ('id', 'nome', 'preco')

class ReservaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reserva
        fields = ('id', 'data', 'hora', 'n_lugares', 'nome_cliente', 'contacto')

class EventoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Evento
        fields = ('id', 'nome', 'data', 'taxaDesconto', 'prato')

class UtilizadorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilizador
        fiels = ('id', 'email', 'nome', 'password', 'admin')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="user-detail")
    class Meta:
        model = User
        fields = ('url', 'username')