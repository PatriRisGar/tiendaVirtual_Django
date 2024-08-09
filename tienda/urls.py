from django.urls import path
from . import views
from tienda.views import Eliminar, Listado, Editar, Añadir,Comprar,Checkout,Informes,InformeMarca,InformeCompraUsuario,InformeTopTenProductos,InformeTopTenClientes
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/admin/producto/',Listado.as_view(),name='listado'),
    path('tienda/admin/producto/editar/<int:pk>',staff_member_required(Editar.as_view()),name='editar'),
    path('tienda/admin/producto/eliminar/<int:pk>',staff_member_required(Eliminar.as_view()),name='eliminar'),
    path('tienda/admin/producto/añadir',staff_member_required(Añadir.as_view()),name='añadir'),
    path('tienda/compra',login_required(Comprar.as_view()),name='comprar'),
    path('tienda/checkout/<int:pk>',login_required(Checkout.as_view()),name='checkout'),
    path('tienda/informes/',staff_member_required(Informes.as_view()),name='informes'),
    path('tienda/informes/marca',staff_member_required(InformeMarca.as_view()),name='informeMarca'),
    path('tienda/informes/compraUsuario',staff_member_required(InformeCompraUsuario.as_view()),name='informeCompraUsuario'),
    path('tienda/informes/topTenProductos',staff_member_required(InformeTopTenProductos.as_view()),name='informeTopTenProductos'),
    path('tienda/informes/informeTopTenClientes',staff_member_required(InformeTopTenClientes.as_view()),name='informeTopTenClientes'),
]
