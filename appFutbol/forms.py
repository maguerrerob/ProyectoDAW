from django import forms
from django.forms import ModelForm
from .models import *

horas_choices = [(f'{i}:00', f'{i}:00') for i in range(0, 24)]

class PartidoModelForm(ModelForm):
    hora= forms.ChoiceField(choices=horas_choices,
                            widget=forms.Select(),
                            label="Escoja una hora")
    
    class Meta:
        model = Partido
        fields = ["hora","tipo", "estilo", "creador", "campo_reservado", "usuarios_jugadores"]
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
        hora = self.cleaned_data.get("hora")
        estado = self.cleaned_data.get("estado")
        tipo = self.cleaned_data.get("tipo")
        estilo = self.cleaned_data.get("estilo")
        creador = self.cleaned_data.get("creador")
        campo_reservado = self.cleaned_data.get("campo_reservado")
        usuarios_jugadores = self.cleaned_data.get("usuarios_jugadores")

        #Aplicamos las restricciones a los campos
        if hora < "7:00":
            self.add_error("hora", "Error, no puedes seleccionar esa hora")
        
        if estado == "F":
            self.add_error("estado", "Error, no puedes crear una reserva completa")

        if tipo == "Pu" and estilo == "5":
            self.add_error("tipo", "Error, los partidos de fútbol sala sólo pueden ser privados")

        if creador == Usuario.objects.filter(nombre="Guti").get() and campo_reservado == Recinto.objects.filter(nombre="La Oliva").get():
            self.add_error("creador", "Error, el usuario elegido tiene betada la entrada a ese campo")

        # Me gustaría hacer referencia a todos los registros del atributo nombre del modelo "Recinto", pero lo hago con listas de nombres de los recintos
        #fut_sala = ["CEIP Espartinas", "La Oliva", "Los Mares"]
        #for campo in fut_sala:
        #    if campo_reservado == campo and estilo == "5":
        #        self.add_error("campo_reservado", "Error, ese campo no está disponible para jugar fútbol sala")

        if len(usuarios_jugadores) > 10 and estilo == "5":
            self.cleaned_data("usuarios_jugadores", "Error, has elegido más jugadores de la cuenta")
        
        if len(usuarios_jugadores) > 14 and estilo == "7":
            self.cleaned_data("usuarios_jugadores", "Error, has elegido más jugadores de la cuenta")         
        
        if len(usuarios_jugadores) > 22 and estilo == "11":
            self.cleaned_data("usuarios_jugadores", "Error, has elegido más jugadores de la cuenta")   


        #Especificamos si devuelve bien los todos los datos (si hay alguno  mal devulve False)
        return self.cleaned_data
    
    
class RecintoForm(forms.ModelForm):
    class Meta:
        model = Recinto
        fields = ['nombre','telefono']
    
    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get("nombre")
        
        
        
        if nombre == "ej":
            self.cleaned_data("nombre", "Error, ese nombre no se puede")
            
        return self.cleaned_data
    
    
class BusquedaRecintoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)


class BusquedaAvanzadaPartidoForm(forms.Form):
    estado_form = forms.ChoiceField(choices=Partido.ESTADO,
                                  required=False)

    estilos_form = forms.MultipleChoiceField(choices=Partido.ESTILO,
                                       required=False,
                                       widget=forms.CheckboxSelectMultiple()
                                       )

    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos

        estado_form = self.cleaned_data.get("estado_form")
        estilos_form = self.cleaned_data.get("estilos_form")

        if (len(estilos_form) == 0
            and estado_form is None):
            self.add_error("estados", "Debe introducir al menos un campo")
            self.add_error("estilos_form", "Debe introducir al menos un campo")

        return self.cleaned_data


class DatosUsuarioModelForm(ModelForm):
    class Meta:
        model = DatosUsuario
        fields = ["descripcion", "posicion", "ubicacion", "usuario", "partidos_jugados"]

    def clean(self):
        super().clean()
        descripcion = self.cleaned_data.get("descripcion")
        posicion = self.cleaned_data.get("posicion")
        ubicacion = self.cleaned_data.get("ubicacion")
        usuario = self.cleaned_data.get("usuario")
        partidos_jugados = self.cleaned_data.get("partidos_jugados")

        if (posicion is None):
            self.add_error("posicion", "Error, seleccione una opción")

        nombreUsuario = DatosUsuario.objects.filter(usuario=usuario).first()

        if(not nombreUsuario is None):
            if(not self.instance is None and nombreUsuario.id == self.instance.id):
                pass
            else:
                self.add_error('usuario','Ya se registraron datos de este usuario')

        return self.cleaned_data
    
# FORMULARIOS EXAMEN

class PromocionModelForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ["nombre", "descripcion", "descuento", "fecha_promocion", "miusuario"]
        
    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get("nombre")
        descripcion = self.cleaned_data.get("descripcion")
        descuento = self.cleaned_data.get("descuento")
        fecha_promocion = self.cleaned_data.get("fecha_promocion")
        miusuario = self.cleaned_data.get("miusuario")
        
      
        
        if len(descripcion) < 50:
            self.add_error('descripcion','Al menos debes indicar 50 caracteres')
            

class BusquedaAvanzadaPromocionForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)

    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2024))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Hasta",
                                  required=False,
                                  widget= forms.SelectDateWidget(years=range(1990,2024))
                                  )

    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        
        fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2023))
                                )
        
        fecha_hasta = forms.DateField(label="Fecha Desde",
                                  required=False,
                                  widget= forms.SelectDateWidget(years=range(1990,2023))
                                  )

        if (textoBusqueda == ""
            and fecha_desde is None
            and fecha_hasta is None):
            self.add_error("textoBusqueda", "Error, introduce algo en la búsqueda")
            self.add_error("fecha_desde", "Error, introduce algo en la búsqueda")
            self.add_error("fecha_hasta", "Error, introduce algo en la búsqueda")

        return self.cleaned_data