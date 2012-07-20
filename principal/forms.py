#encoding: utf-8
from django.forms import ModelForm
from django import forms
from principal.models import Lugar, Tapa, Comentario

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
		


