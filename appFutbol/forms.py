from django import forms
from django.forms import ModelForm
from .models import *

class PartidoModelForm(ModelForm):
    class Meta:
        model = Partido
        fields = ["estado", "tipo", "estilo", "creador", "campo_reservado", "usuarios_jugadores"]
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
        estado = self.cleaned_data.get("estado")
        tipo = self.cleaned_data.get("tipo")

        creador = self.cleaned_data.get("creador")
        campo_reservado = self.cleaned_data.get("campo_reservado")

        #Aplicamos las restricciones a los campos
        if estado != "F":
            self.add_error("estado", "Error, no puedes crear una reserva completa")

        # Comprobamos que no sean más de 22 jugadores para una reserva



        #Especificamos si devuelve bien los todos los datos (si hay alguno  mal devulve False)
        return self.cleaned_data
    
class BusquedaPartidoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)