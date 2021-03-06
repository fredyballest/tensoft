from django.conf.urls import url, include
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from inmobiliaria_tenant.views import *
from inmuebles.views import *
from RegUsuarios.views import *
from propietarios.views import *
from citas.views import *
from tensoft.settings import *
from reportes.views import *
from pagos.views import *

url_inmuebles = [
    url(r'^registrar/$', InmueblesCreateView.as_view(), name="registrar-inmueble"),
    url(r'^registrar/(?P<id_inmueble>[\w.@+-]+)/fotos/$', AgregarFotosInmueble.as_view(),
        name="registrar-fotos-inmueble"),
    url(r'^buscar/$', BuscarInmuebles.as_view(), name='buscar-inmuebles'),
    url(r'^lista/$', ListarInmuebles.as_view(), name='listar-inmuebles'),
    url(r'^mapa/$', InmueblesMapa.as_view(), name='inmuebles-mapa'),
    url(r'^lista/activos/$', ListarInmueblesActivos.as_view(), name='listar-inmuebles'),
    url(r'^(?P<pk>[\w.@+-]+)/$', DetallesInmueble.as_view(), name='detalles-inmueble'),
    url(r'^(?P<pk>[\w.@+-]+)/actualizar/$', ActualizarInmueble.as_view(), name='actualizar-inmueble'),
    url(r'^generar-pago/(?P<id_inmueble>[\w.@+-]+)/$', GenerarFacturaPago.as_view(), name="generar-factura"),
]

url_propietario = [
    url(r'^registrar$', PropietarioCreateView.as_view(), name="registrar-propietario"),
    url(r'^(?P<pk>[\w.@+-]+)/actualizar/$', ActualizarPropietario.as_view(), name='actualizar-propietario'),
    url(r'^lista/$', ListarPropietarios.as_view(), name='listar-propietarios'),
]

url_citas = [
    url(r'^registrar/(?P<id>[\w.@+-]+)/$', CitasCreateView.as_view(success_url="/citas/lista/?estado=1"), name="registrar-cita"),
    #url(r'^lista/$', ListarCitas.as_view(), name='listar-citas'),
    url(r'^(?P<pk>[\w.@+-]+)/$', DetallesCita.as_view(), name='detalles-cita'),
    url(r'^(?P<pk>[\w.@+-]+)/actualizar/$', ActualizarCita.as_view(), name='actualizar-cita'),
]

url_reportes_recaudos = [
    url(r'^facturas-vencidas/$', ReporteFacturas.as_view(), {'tipo': 'vencidas'}),
    url(r'^facturas-activas/$', ReporteFacturas.as_view(), {'tipo': 'activas'}),
    url(r'^seguimiento-inmuebles/$', SeguimientoPagosInmueble.as_view(), name="seguimiento-pagos"),
    url(r'^estado-pagos/$', EstadoPagos.as_view(), name="estado-pagos"),
]

url_reportes_citas = [
    url(r'^programacion/$', ConsultarCalendarioCitas.as_view(), name="programacion-citas"),
]

url_reportes = [
    url(r'^lista-inmuebles/(?P<formato>(html|pdf))/estado_operacional/(?P<id>[0-9]+)/$',
        ReporteListaInmueblesEstado.as_view(), name='reporte-lista-inmuebles-estado'),
    url(r'^lista-inmuebles/(?P<formato>(html|pdf))/tipo_inmueble/(?P<id>[0-9]+)/$',
        ReporteListaInmueblesTipo.as_view(), name='reporte-lista-inmuebles'),
    url(r'^tipo-inmuebles/$', ReporteInmueblesPorTipo.as_view(), name='reporte-inmuebles-tipo'),
    url(r'^estado-inmuebles/$', ReporteInmueblesDisponiblesOcupados.as_view(), name='reporte-estado-inmuebles'),
    url(r'^recaudos/', include(url_reportes_recaudos)),
    url(r'^recaudos/', include(url_reportes_citas)),
]

url_cuenta = [
    url(r'^registrar/$', UsuarioCreateView.as_view(), name="registrar-usuario"),
    url(r'^registrar/usuario/$', UsuarioClienteCreateView.as_view(), name="registrar-usuario-cliente"),
    url(r'^actualizar/$', ClienteUpdateView.as_view(), name="actualizar-usuario"),
    url(r'^login/$', auth_views.login, name="login-usuario"),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^login/$', auth_views.login, name="login-usuario"),
    url(r'^registrar/usuario/$', UsuarioClienteCreateView.as_view(), name="registrar-usuario-cliente"),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    # url(r'^my/$', login_required(CuentaCliente.as_view()), name="cuenta-cliente"),
    # url(r'^(?P<id_cliente>[\w.@+-]+)/$', login_required(CuentaCliente.as_view()), name="cuenta-cliente")
    url(r'^oauth/', include('social_django.urls', namespace='social')),

]

url_payments = [
    url(r'^consultar/$', ConsultarFacturas.as_view(), name="consultar-facturas"),
    url(r'^historico/$', ConsultarFacturasPagadas.as_view(), name="historico-facturas"),
    url(r'^factura/(?P<pk>[\w.@+-]+)/$', DetalleFactura.as_view(), name="detalles-facturas"),
    url(r'^process/$', payment_process, name="process"),
    url(r'^done/$', payment_done, name="done"),
    url(r'^cancelled/$', payment_cancelled, name="cancelled"),
]
if settings.DEBUG:
    urlpatterns = [
        url(r'^$', Inicio.as_view(), name='inicio'),
        url(r'^admin/', admin.site.urls),
        url(r'^cuenta/', include(url_cuenta)),
        url(r'^registrar-mensaje/', admin.site.urls),
        url(r'^inmuebles/', include(url_inmuebles)),
        url(r'^propietarios/', include(url_propietario)),
        url(r'^citas/', include(url_citas)),
        url(r'^reportes/', include(url_reportes)),
        url(r'^payment/', include(url_payments, namespace="payment")),
        url(r'^paypal/', include('paypal.standard.ipn.urls')),
    ]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
