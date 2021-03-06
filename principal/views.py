# -*- coding: utf8 -*-
from principal.models import Lugar, Tapa, Comentario
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from principal.forms import AltaTapaForm, AltaComentarioForm, RegisterForm, \
    LugarNuevo, lugaresCercanos, addTapaForm, AltaLugarForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import urllib2
import requests
from xml.dom import minidom
import urllib
import random
from googlemaps import GoogleMaps
import sys


#Añadimos al path de python lo modulos que se encuentran en la carpeta modules\
#de alwaysdata para mas informacion mirar en:
#http://wiki.alwaysdata.com/wiki/Instalar_un_m%C3%B3dulo_en_Python_(Es)
sys.path.append('~/modules')


@login_required(login_url='/ingresar')
def tapas(request):
    tapas = Tapa.objects.all()
    return render_to_response('tapas.html', {'tapas': tapas},
        context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def detalle_tapa(request, id_tapa):
    dato = get_object_or_404(Tapa, pk=id_tapa)
    comments = Comentario.objects.filter(com_tapa=dato)
    return render_to_response('tapa.html', {'dato': dato,
    'comments': comments}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def localizacion(request):
    return render_to_response('localizacion.html')


@login_required(login_url='/ingresar')
def nueva_tapa(request):
    if request.method == 'POST':
        #obtenemos el valor del usuario dado de alta en la aplicacion
        tapa = Tapa(usuario=request.user)
        #con instance introducimos el valor obtenido antes del usuario dado
        #de alta en la tapa
        formulario = AltaTapaForm(request.POST, request.FILES, instance=tapa)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/tapas')
    else:
        formulario = AltaTapaForm()
    return render_to_response('altatapa.html', {'formulario': formulario},
        context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def comentar_tapa(request, id_tapa):
    dato = get_object_or_404(Tapa, pk=id_tapa)
    comments = Comentario.objects.filter(com_tapa=dato)
    #valorar el formulario de comentarios
    if request.method == 'POST':
        formulario = AltaComentarioForm(request.POST)
        if formulario.is_valid():
            #hacemos un falso commit para despues variar valores antes de
            #hacer el verdero commit
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
            #com_tapa = formulario.cleaned_data['com_tapa']
            #comentario = formulario.cleaned_data['comentario']
            #usuario = request.user
            return HttpResponseRedirect('/tapas')
        else:
            formulario = AltaComentarioForm()
    return render_to_response('altacomentario.html', {'dato': dato,
        'comments': comments, 'formulario': formulario},
        context_instance=RequestContext(request))


def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/privado')
    if request.method == 'POST':
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
                    return render_to_response('noactivo.html',
                        context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html',
                    context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html', {'formulario': formulario},
        context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    return render_to_response('privado.html', {'usuario': usuario},
        context_instance=RequestContext(request))


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
    return render_to_response('inicio.html',
        {'aleatoriaselegidas': aleatoriaselegidas},
        context_instance=RequestContext(request))


def usuarioNuevo(request):
    if request.method == 'POST':
        usuario = RegisterForm(request.POST)
        if usuario.is_valid():
            usuario.save()
            HttpResponseRedirect('/ingresar')
    else:
        usuario = RegisterForm()
    return render_to_response('usuarionuevo.html', {'usuario': usuario},
        context_instance=RequestContext(request))


def localizarlugares(request):
    return render_to_response('lugares.html')


def obtenerPosicion(request):
    if request.method == 'POST':
        localizacion = request.POST['ubicacion']
        #Distancia desde el lugar que te encuentras
        distancia_lugar = '1000'
        #lugares que buscarmos
        lugar = 'bar|cafeteria|comida|restaurante'
        #obtenemos los lugares cercanos con un XML del API de Google Maps
        lugares = 'https://maps.googleapis.com/maps/api/place/search/xml?\
            location=' + localizacion + '&radius= \
            ' + distancia_lugar + '&types=' + lugar + '&sensor \
            =true&key=AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A'
        print lugares
        xmldoc = minidom.parse(urllib.urlopen(lugares))
        local = []
        for item in xmldoc.getElementsByTagName("result"):
            for item in item.getElementsByTagName('name'):
                local.append(item.firstChild.data)
        return render_to_response('lugarescercanos.html',
        {'local': local}, context_instance=RequestContext(request))
    else:
        return render_to_response('obtenerposicion.html',
            context_instance=RequestContext(request))


def lugarnuevo(request):
    if request.method == 'POST':
        formulario = LugarNuevo(request.POST)
        if formulario.is_valid():
            #Obtencion de valores del formulario para generar el XML
            direccion = formulario.cleaned_data['direccion']
            print direccion
            poblacion = formulario.cleaned_data['poblacion']
            print poblacion
            nombre = formulario.cleaned_data['nombre']
            print nombre
            tipo = formulario.cleaned_data['tipo']
            print tipo
            gmaps = GoogleMaps('AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A')
            direccion = direccion + ',' + poblacion
            lat, lng = gmaps.address_to_latlng(direccion)
            lat = str(lat)
            lng = str(lng)
            if tipo == '1':
                tipo = 'bar'
            elif tipo == '2':
                tipo = 'cafeteria'
            elif tipo == '3':
                tipo = 'comida'
            elif tipo == '4':
                tipo = 'restaurante'
            print tipo
            xml = "<PlaceAddRequest>" + "<location>" + "<lat>" + \
                lat + \
                "</lat>" + "<lng>" + lng + "</lng>" + \
                "</location>" + \
                "<accuracy>" + "5" + "</accuracy>" + \
                "<name>" + nombre + "</name>" + \
                "<type>" + tipo + "</type>" + \
                "<language>" + "es" + "</language>" + \
                "</PlaceAddRequest>"
            #print xml
            ##utilizamos request, una libreria mas optimizada que urllib2
            #r = requests.post('https://maps.googleapis.com/maps/api/place/ \
            #add/xml?sensor=false&key= \
            #AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A', xml)
            #print r.content
            url = 'https://maps.googleapis.com/maps/api/place/add/xml?sensor=false&key=AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A'
            req = urllib2.Request(url,
                xml,
                headers={'Content-Type': 'application/xml'})
            consulta = urllib2.urlopen(req)
            print consulta.read()
    else:
        formulario = LugarNuevo()
    return render_to_response('lugarnuevo.html', {'formulario': formulario},
    context_instance=RequestContext(request))


def obtpos(request):
    gmaps = GoogleMaps('AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A')
    #Distancia desde el lugar que te encuentras
    radio = '1000'
    #lugares que buscamos
    lugar = 'bar|cafeteria|comida|restaurante'
    if request.method == 'POST':
        formulario = lugaresCercanos(request.POST)
        if formulario.is_valid:
            direccion = request.POST['direccion']
            poblacion = request.POST['poblacion']
            direccion = direccion + ',' + poblacion
            print direccion
            radio = request.POST['radio_distancia']
            #utilizamos la libreria de google maps
            lat, lng = gmaps.address_to_latlng(direccion)
            lat = str(lat)
            lng = str(lng)
            print lat
            print lng
            lugares = 'https://maps.googleapis.com/maps/api/place/search/' + \
                'xml?location=' + lat + ',' + lng + '&radius=' + radio + \
                '&types=' + lugar + \
                '&sensor=true&key=AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A'
            print lugares
            xmldoc = minidom.parse(urllib.urlopen(lugares))
            local = []
            ref = []
            datos = []
            i = 0
            for item in xmldoc.getElementsByTagName("result"):
                for item in item.getElementsByTagName('name'):
                    local.append(item.firstChild.data)
                    print item.firstChild.data
                for item in xmldoc.getElementsByTagName("reference"):
                    ref.append(item.firstChild.data)
            #vamos a meter las listas en un diccionario para facilitar la
            #union en el template
            for i in range(0, len(local)):
                datos.append({'local': local[i], 'ref': ref[i]})
        return render_to_response('lugarescercanos.html', {'datos': datos},
        context_instance=RequestContext(request))
    else:
        formulario = lugaresCercanos()
        return render_to_response('direccion.html', {'formulario': formulario},
        context_instance=RequestContext(request))


def nuevaTapaPosicion(request):
    #Lo primero es elegir el local de donde es la tapa
    gmaps = GoogleMaps('AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A')
    #Distancia desde el lugar que te encuentras
    radio = '1000'
    #lugares que buscamos
    lugar = 'bar|cafeteria|comida|restaurante'
    if request.method == 'POST':
        formulario = lugaresCercanos(request.POST)
        if formulario.is_valid:
            direccion = request.POST['direccion']
            poblacion = request.POST['poblacion']
            direccion = direccion + ',' + poblacion
            print direccion
            radio = request.POST['radio_distancia']
            #utilizamos la libreria de google maps
            lat, lng = gmaps.address_to_latlng(direccion)
            lat = str(lat)
            lng = str(lng)
            print lat
            print lng
            lugares = 'https://maps.googleapis.com/maps/api/place/search/xml? \
            location=' + lat + ',' + lng + '&radius=' + radio + '&types= \
            ' + lugar + '&sensor= \
            true&key=AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A'
            print lugares
            xmldoc = minidom.parse(urllib.urlopen(lugares))
            local = []
            for item in xmldoc.getElementsByTagName("result"):
                for item in item.getElementsByTagName('name'):
                    local.append(item.firstChild.data)
        return render_to_response('alttapa.html', {'local': local},
        context_instance=RequestContext(request))
    else:
        formulario = lugaresCercanos()
        return render_to_response('direccion.html', {'formulario': formulario},
        context_instance=RequestContext(request))


def selecciondeLocal(request, referencia):
    #direccion  url y telefono desconocida en caso de que falle la
    #API de google Maps
    direccion = ""
    url = ""
    telefono = ""
    lugar = \
        'https://maps.googleapis.com/maps/api/place/details/xml?reference=' \
        + referencia + \
        '&sensor=true&key=AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A'
    print lugar
    xmldoc = minidom.parse(urllib.urlopen(lugar))
    local = []
    for item in xmldoc.getElementsByTagName("result"):
        for item in xmldoc.getElementsByTagName("name"):
            local = item.firstChild.data
        for item in xmldoc.getElementsByTagName("vicinity"):
            direccion = item.firstChild.data
        for item in xmldoc.getElementsByTagName("url"):
            url = item.firstChild.data
        for item in xmldoc.getElementsByTagName("formatted_phone_number"):
            telefono = item.firstChild.data
    return render_to_response('lugarescercanos.html',
        {'local': local, 'direccion': direccion, 'url': url,
        'telefono': telefono, 'referencia': referencia},
        context_instance=RequestContext(request))


def addTapa(request, referencia, local, direccion):
    print referencia
    print local
    if request.method == 'POST':
        formulario = addTapaForm(request.POST, request.FILES)
        if formulario.is_valid():
            #creamos el objeto del modelo Tapa
            lugar = Lugar()
            lugar.nombre = local
            lugar.direccion = direccion
            lugar.referencia = referencia
            #comprobamos si existe el lugar de antemano y si existe
            #capturamos su id para agregar una nueva Tapa, y sino existe
            #lo creamos
            #Si no existe lo damos de alta
            print "REFERENCIA: " + referencia
            #comprobemos si existe el lugar, y en el caso de que no exista
            #lo damos de alta en nuestra bbdd
            existeLugar = Lugar.objects.filter(referencia=referencia)            
            if not existeLugar:
                print "no existe el lugar....."
                #demos de alta el lugar
                lugar.save()
            #procedamos a dar de alta la tapa            
            tapa = Tapa()
            tapa.imagen = request.FILES['imagen']
            tapa.nombre = request.POST['nombreTapa']            
            tapa.lugar = lugar          
            tapa.usuario = request.user
            tapa.save()            
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/obtpos')
    else:
        formulario = addTapaForm(initial={'referencia': referencia,
            'nombreLugar': local})
        if local == "":
            local = "No existe el nombre del local"
        print "Referencia:" + referencia
        print "Nombre:" + local
        return render_to_response('altatapa.html',
            {'formulario': formulario,
            'referencia': referencia, 'local': local},
            context_instance=RequestContext(request))



#*****************************************************************************
#KEY DE MITAPA
#https://maps.googleapis.com/maps/api/place/search/xml? \
#location=39.16276,-3.028257&radius=1000&types=bar&sensor= \
#false&key=AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A
#key=AIzaSyCNUf4Y4LBWWkQAYSvJmQCriCzNmEJkD0A
#*****************************************************************************
