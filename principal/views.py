from principal.models import Lugar, Tapa, Comentario
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from principal.forms import AltaTapaForm, AltaComentarioForm, AltaLugarForm, RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

import random



@login_required(login_url='/ingresar')
def tapas(request):
	tapas = Tapa.objects.all()
	return render_to_response('tapas.html',{'tapas':tapas}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def detalle_tapa(request, id_tapa):	
	dato = get_object_or_404(Tapa, pk=id_tapa)
	comments = Comentario.objects.filter(com_tapa = dato)
	return render_to_response('tapa.html', {'dato':dato, 'comments':comments}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def localizacion(request):
	return render_to_response('localizacion.html')

@login_required(login_url='/ingresar')
def nueva_tapa(request):    
	if request.method == 'POST':
		#obtenemos el valor del usuario dado de alta en la aplicacion 
		tapa = Tapa(usuario=request.user)
		#con instance introducimos el valor obtenido antes del usuario dado de alta en la tapa       
		formulario = AltaTapaForm(request.POST, request.FILES, instance=tapa)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/tapas')
	else:
		formulario = AltaTapaForm()	
	return render_to_response('altatapa.html', {'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def comentar_tapa(request, id_tapa):
    dato = get_object_or_404(Tapa, pk=id_tapa)
    comments = Comentario.objects.filter(com_tapa = dato)
    #valorar el formulario de comentarios
    if request.method == 'POST':    	
        formulario = AltaComentarioForm(request.POST)        
        if formulario.is_valid():
            #hacemos un falso commit para despues variar valores antes de hacer el verdero commit                       
            form = formulario.save(commit=False)
            #modificamos los valores
            form.usuario = request.user
            form.com_tapa = dato
            form.save()
            #devolver a pagina de comentarios
            pag_comentario = '/comentar_tapa/%s' % id_tapa                      
            return HttpResponseRedirect(pag_comentario)
    else:
        formulario = AltaComentarioForm()
        if formulario.is_valid():
            com_tapa = formulario.cleaned_data['com_tapa']
            comentario = formulario.cleaned_data['comentario']
            usuario = request.user            
            return HttpResponseRedirect('/tapas')
        else:
            formulario = AltaComentarioForm()   
    return render_to_response('altacomentario.html', {'dato':dato, 'comments':comments, 'formulario':formulario}, context_instance=RequestContext(request))

def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/privado')
    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/privado')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')            
def privado(request):
    usuario = request.user
    return render_to_response('privado.html', {'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


#funcion para mostrar tapas aleatorias de todos los lugares del mundo


def inicio(request):
	tapas = Tapa.objects.all()
	aleatoriaselegidas = []
	x = 5
	while x > 0:		
		aleatoriaselegidas.append(random.choice(tapas))
		x = x - 1 
	return render_to_response('inicio.html',{'aleatoriaselegidas':aleatoriaselegidas},context_instance=RequestContext(request))


def usuarioNuevo(request):    
    if request.method == 'POST':
        usuario = RegisterForm(request.POST)
        if usuario.is_valid():
            usuario.save() 
            HttpResponseRedirect('/ingresar')
    else:
        usuario = RegisterForm()
    return render_to_response('usuarionuevo.html', {'usuario':usuario}, context_instance=RequestContext(request))

       







