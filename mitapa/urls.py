from django.conf.urls import patterns, include, url
from django.conf import settings

# haber si funciona
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mitapa.views.home', name='home'),
    # url(r'^mitapa/', include('mitapa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'principal.views.inicio'),   
    url(r'^tapas/$', 'principal.views.tapas'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
		{'document_root':settings.MEDIA_ROOT,}
	),
	url(r'^tapa/(?P<id_tapa>\d+)$', 'principal.views.detalle_tapa'),
    url(r'^comentar_tapa/(?P<id_tapa>\d+)$', 'principal.views.comentar_tapa'),		
    url(r'^localizacion/$', 'principal.views.localizacion'),
    url(r'^altatapa/$', 'principal.views.nueva_tapa'),    
    url(r'^ingresar/$', 'principal.views.ingresar'),
    url(r'^privado/$','principal.views.privado'),
    url(r'^cerrar/$', 'principal.views.cerrar'),
    url(r'^usuario/nuevo/$', 'principal.views.usuarioNuevo'),
    url(r'^lugares/$','principal.views.localizarlugares'),
    url(r'^obtenerposicion/$', 'principal.views.obtenerPosicion'),
    url(r'^lugarnuevo/$', 'principal.views.lugarnuevo'),
    url(r'^obtpos/$', 'principal.views.obtpos'),
    url(r'^Nueva_tapa/$', 'principal.views.nuevaTapaPosicion')        
)
