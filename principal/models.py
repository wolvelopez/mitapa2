from django.db import models
#Anado la tabla de usuarios del sistema de django para integrar los usuarios con sus tapas
from django.contrib.auth.models import User

# Create your models here.
class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    #referencia de la API de google places
    referencia = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nombre
        
class Tapa(models.Model):
    nombre = models.CharField(max_length=50)
    lugar = models.ForeignKey(Lugar)
    imagen = models.ImageField(upload_to='tapas', verbose_name='tapas')    
    usuario = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.nombre

class Comentario(models.Model):
    com_tapa = models.ForeignKey(Tapa)
    comentarios = models.TextField()
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.comentarios
    

