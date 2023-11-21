from django import forms
from django.forms import ModelForm
from .models import *

class PartidoModelForm(ModelForm):
    class Meta:
        model = Reserva
        fields = ["estado", "tipo", "n_jugadores", "creador", "campo_reservado"]
        labels = {
            "estado": ("Completa o disponible"),
            "tipo": ("Pública o privada")
        }
        help_texts = {
            "estado": ("Selecciona alguna opción"),
            "tipo": ("Selecciona alguna opción"),
        }