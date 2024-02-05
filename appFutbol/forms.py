from django import forms
from django.forms import ModelForm
from .models import *
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm

# FORMULARIOS - USUARIO
class RegistroForm(UserCreationForm):
    roles = (
        (Usuario.CLIENTE, "cliente"),
        (Usuario.DUEÑORECINTO, "dueñorecinto")
    )
    rol = forms.ChoiceField(choices=roles)
    class Meta:
        model = Usuario
        fields = ("username", "email", "password1", "password2", "rol")


# Búsqueda avanzada usuario
class BusquedaAvanzadaUsuarioForm(forms.Form):
   textoBusqueda = forms.CharField(required=False,
                                   label=("Buscar usuario"),
                                   widget=forms.TextInput(attrs={"placeholder": "Nombre o apellidos"}))


   nivel = forms.FloatField(required=False)


   def clean(self):
       super().clean()


       textoBusqueda = self.cleaned_data.get('textoBusqueda')
       nivel = self.cleaned_data.get("nivel")


       if (textoBusqueda == ""
           and nivel == 0.0):
           self.add_error("textoBusqueda", "Debe introducir al menos un valor en un campo del formulario")
           self.add_error("nivel", "Debe introducir al menos un valor en un campo del formulario")


       return self.cleaned_data


# FORMULARIOS - PARTIDO
# Variable que muestra las horas en el desplegable de forms.Select() de hora
horas_choices = [(f'{i}:00', f'{i}:00') for i in range(0, 24)]

class PartidoModelForm(ModelForm):
    #Uso el widget forms.Select() y el campo "hora" fuera del meta para cambiar un poco
    hora= forms.ChoiceField(choices=horas_choices,
                            widget=forms.Select(),
                            label="Escoja una hora")

    class Meta:
        model = Partido
        fields = ["hora","tipo", "estilo", "creador", "campo_reservado", "usuarios_jugadores"]
        labels = {
            "tipo": ("Pública o privada")
        }
        help_texts = {
            "tipo": ("Selecciona alguna opción"),
        }
        widgets = {
            "creador": forms.HiddenInput(),
        }


    def clean(self):
        super().clean()
        #Obtenemos los datos de los campos
        hora = self.cleaned_data.get("hora")
        tipo = self.cleaned_data.get("tipo")
        estilo = self.cleaned_data.get("estilo")
        usuarios_jugadores = self.cleaned_data.get("usuarios_jugadores")

        #Aplicamos las restricciones a los campos

        #Primero paso todas las horas a formato "strptime" para comparar horas
        hora_datetime = datetime.strptime(hora, "%H:%M")
        hora_siete_datetime = datetime.strptime("7:00", "%H:%M")

        if hora_datetime < hora_siete_datetime:
            self.add_error("hora", "Error, no puedes seleccionar esa hora")

        if tipo == "Pu" and estilo == "5":
            self.add_error("tipo", "Error, los partidos de fútbol sala sólo pueden ser privados")

        if len(usuarios_jugadores) > 10 and estilo == "5":
            self.cleaned_data("usuarios_jugadores", "Error, has elegido más jugadores de la cuenta")

        if len(usuarios_jugadores) > 14 and estilo == "7":
            self.cleaned_data("usuarios_jugadores", "Error, has elegido más jugadores de la cuenta")

        if len(usuarios_jugadores) > 22 and estilo == "11":
            self.cleaned_data("usuarios_jugadores", "Error, has elegido más jugadores de la cuenta")


        #Especificamos si devuelve bien los todos los datos (si hay alguno  mal devulve False)
        return self.cleaned_data


class PartidoModelFormRequest(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PartidoModelFormRequest, self).__init__(*args, **kwargs)
        jugadoresdisponibles = Jugador_partido.objects.exclude(partido__cliente=self.request.user.cliente).all()
        self.fields["usuarios_jugadores"] = forms.ModelChoiceField(
            queryset=jugadoresdisponibles,
            widget=forms.Select,
            required=True,
            empty_label="Ninguna"
        )


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


# FORMULARIOS - RECINTO
class RecintoModelForm(ModelForm):
    class Meta:
        model = Recinto
        fields = ['nombre', 'ubicacion', 'telefono', 'dueño_recinto']
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Introduce nombre del recinto"}),
            "dueño_recinto": forms.HiddenInput()
        }

    def clean(self):
        super().clean()

        nombre = self.cleaned_data.get("nombre")
        telefono = self.cleaned_data.get("telefono")

        recintoNombre = Recinto.objects.filter(nombre=nombre).first()
        if(not recintoNombre is None):
            if(not self.instance is None and recintoNombre.id == self.instance.id):
                pass
            else:
                self.add_error('nombre','Ya existe un recinto con ese nombre')

        if len(telefono) < 9:
            self.add_error("telefono", "Error, formato de teléfono incorrecto")

        return self.cleaned_data


class RecintoModelFormRequest(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(RecintoModelFormRequest, self).__init__(*args, **kwargs)
        librosdisponibles = Recinto.objects.exclude(prestamo__cliente=self.request.user.cliente).all()
        self.fields["libro"] = forms.ModelChoiceField(
            queryset=librosdisponibles,
            widget=forms.Select,
            required=True,
            empty_label="Ninguna"
        )


class BusquedaRecintoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)

# Formulario genérico
class BusquedaAvanzadaRecintoFormGen(forms.Form):
    nombre = forms.CharField(required=True)
    ubicacion = forms.CharField(required=True)
    telefono = forms.CharField(required=True)

    def clean(self):

        #Validamos con el modelo actual
        super().clean()

        #Obtenemos los campos

        nombre = self.cleaned_data.get("nombre")
        ubicacion = self.cleaned_data.get("ubicacion")
        telefono = self.cleaned_data.get("telefono")

        if (nombre == ""
            and ubicacion == ""
            and telefono == ""):
            self.add_error("nombre", "Debe introducir al menos un campo")
            self.add_error("ubicacion", "Debe introducir al menos un campo")
            self.add_error("telefono", "Debe introducir al menos un campo")

        return self.cleaned_data

# Formulario de modelos
class BusquedaAvanzadaRecintoForm(ModelForm):
    class Meta:
        model = Recinto
        fields = ['nombre', 'telefono']
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Introduce algún caracter del recinto a buscar"})
        }

    def clean(self):
        #Validamos con el modelo actual
        super().clean()

        #Obtenemos los campos
        nombre = self.cleaned_data.get("nombre")
        telefono = self.cleaned_data.get("telefono")

        if (nombre == ""
            and telefono == ""):
            self.add_error("nombre", "Debe introducir al menos un campo")
            self.add_error("telefono", "Debe introducir al menos un campo")

        return self.cleaned_data


# FORMULARIOS - RESULTADO

class ResultadoModelForm(ModelForm):
    class Meta:
        model = Resultado
        fields = ['goles_local', 'goles_visitante']

    def clean(self):
        super().clean()

        goles_local = self.cleaned_data.get("goles_local")
        goles_visitante = self.cleaned_data.get("goles_visitante")

        if goles_local < 0:
            self.add_error("goles_local", "Error de resultado")
        if goles_visitante < 0:
            self.add_error("goles_visitante" "Error de resultado")

        return self.cleaned_data



# FORUMULARIOS - DATOSUSUARIO
class DatosUsuarioModelForm(ModelForm):
    class Meta:
        model = DatosUsuario
        fields = ["descripcion", "posicion", "ubicacion", "cliente", "partidos_jugados"]

    def clean(self):
        super().clean()
        descripcion = self.cleaned_data.get("descripcion")
        posicion = self.cleaned_data.get("posicion")
        ubicacion = self.cleaned_data.get("ubicacion")
        cliente = self.cleaned_data.get("cliente")
        partidos_jugados = self.cleaned_data.get("partidos_jugados")

        if (posicion is None):
            self.add_error("posicion", "Error, seleccione una opción")

        nombreUsuario = DatosUsuario.objects.filter(cliente=cliente).first()

        if(not nombreUsuario is None):
            if(not self.instance is None and nombreUsuario.id == self.instance.id):
                pass
            else:
                self.add_error('cliente','Ya se registraron datos de este usuario')

        return self.cleaned_data


class BusquedaAvanzadaDatosusuarioFormGen(forms.Form):
    descripcion = forms.CharField(required=True)
    posiciones = forms.MultipleChoiceField(choices=DatosUsuario.POSICION,
                                required=False,
                                widget=forms.CheckboxSelectMultiple())
    ubicacion = forms.CharField(required=True)

    def clean(self):

        #Validamos con el modelo actual
        super().clean()

        #Obtenemos los campos

        descripcion = self.cleaned_data.get("descripcion")
        posiciones = self.cleaned_data.get("posiciones")
        ubicacion = self.cleaned_data.get("ubicacion")

        if (descripcion == ""
            and len(posiciones) == ""
            and ubicacion == ""):
            self.add_error("nombre", "Debe introducir al menos un campo")
            self.add_error("posiciones", "Debe introducir al menos un campo")
            self.add_error("ubicacion", "Debe introducir al menos un campo")
        else:
            if (descripcion != "" and len(descripcion) < 3):
                self.add_error("descripcion", "Error, mínimo debe contener 3 carácteres")

        return self.cleaned_data



# FORMULARIOS EXAMEN
class PromocionModelForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ["nombre", "descripcion", "descuento", "fecha_promocion", "miusuario"]
        widgets = {
            "miusuario": forms.HiddenInput()
        }

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