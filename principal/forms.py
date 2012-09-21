#encoding: utf-8
from django.forms import ModelForm
from django import forms
from principal.models import Lugar, Tapa, Comentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple



class AltaTapaForm(ModelForm):
    class Meta:
        model = Tapa
        #excluimos el usuario porque lo recogemos en la vista al estar logueado
        exclude = ('usuario',)


class AltaComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        exclude = ('com_tapa', 'usuario',)


class AltaLugarForm(ModelForm):
    class Meta:
        model = Lugar


#Modificamos la clase de UserCreationForm heredando de ella
#y añadiendo email, nombre y apellidos
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    firstname = forms.CharField(label="Nombre")
    lastname = forms.CharField(label="Apellidos")

    class Meta:
        model = User
        fields = ("firstname", "lastname", "email", "username", )

#Valores posibles a elegir de un lugar nuevo
tipos = (
    ('1', 'bar'),
    ('2', 'cafeteria'),
    ('3', 'comida'),
    ('4', 'restaurante'))


class LugarNuevo(forms.Form):
    latitud = forms.CharField(label="Latitud", required=False)
    longitud = forms.CharField(label="Longitud", required=False)
    precision = forms.CharField(label="Precision", required=False)
    nombre = forms.CharField(label="Nombre")
    tipo = forms.MultipleChoiceField(required=False,
        widget=CheckboxSelectMultiple, choices=tipos)
    lenguaje = forms.CharField(label="lenguaje", required=False)


class lugaresCercanos(forms.Form):
    direccion = forms.CharField(label="Direccion", required=True)
    poblacion = forms.CharField(label="Poblacion", required=True)
    radio_distancia = forms.CharField(label="Metros(0-5000)",
         required=True)


