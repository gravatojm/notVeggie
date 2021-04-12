from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# superuser
# admin
# pass1234

class Prato (models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=70)
    preco = models.IntegerField()

    def __str__(self):
        return self.nome

class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    hora = models.TimeField()
    n_lugares = models.IntegerField()
    nome_cliente = models.ForeignKey(settings.AUTH_USER_MODEL)
    contacto = models.IntegerField()

    def __str__(self):
        return str(self.data)

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=70)
    data = models.DateField()
    taxaDesconto = models.DecimalField(max_digits=3, decimal_places=3)
    prato = models.ForeignKey('Prato', on_delete=models.CASCADE,)

    def __str__(self):
        return self.nome

class Utilizador(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=70)
    nome = models.CharField(max_length=70)
    password = models.CharField(max_length=70)
    admin = models.BooleanField()

    def __str__(self):
        return self.email

