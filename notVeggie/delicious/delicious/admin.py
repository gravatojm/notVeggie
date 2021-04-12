from django.contrib import admin
from .models import Prato, Reserva, Evento, Utilizador

admin.site.register(Prato)
admin.site.register(Reserva)
admin.site.register(Evento)
admin.site.register(Utilizador)