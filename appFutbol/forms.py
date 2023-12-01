from django import forms
from django.forms import ModelForm
from .models import *

class ReservaModelForm(ModelForm):
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

    def clean(self):
        super().clean()
        #Obtenemos los datos de los campos
        n_jugadores = self.cleaned_data.get("n_jugadores")

        #Aplicamos las restricciones a los campos
        if n_jugadores > 22:
            self.add_error("n_jugadores", "Error, no se puede jugar un partido con más de 22 jugadores porrita")

        #Especificamos si devuelve bien los todos los datos (si hay alguno  mal devulve False)
        return self.cleaned_data
    
class BusquedaReservaForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)