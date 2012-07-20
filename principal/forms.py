#encoding: utf-8
from django.forms import ModelForm
from django import forms
from principal.models import Lugar, Tapa, Comentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class AltaTapaForm(ModelForm):
	class Meta:
		model = Tapa
		#excluimos el usuario porque lo recogemos en la vista al estar logueado 
		exclude = ('usuario',)

class AltaComentarioForm(ModelForm):
	class Meta:
		model = Comentario
		exclude = ('com_tapa','usuario',)

class AltaLugarForm(ModelForm):
	class Meta:
		model = Lugar

#Modificamos la clase de UserCreationForm heredando de ella y añadiendo email, nombre y apellidos
class RegisterForm(UserCreationForm):	
    email = forms.EmailField(label = "Email")
    firstname = forms.CharField(label = "Nombre")
    lastname = forms.CharField(label = "Apellidos")
    class Meta:
        model = User
        fields = ("firstname", "lastname", "email", "username", )

