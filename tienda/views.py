from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from typing import Any
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from tienda.models import Compra, Producto, User
from django.db.models import Sum, Count

# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})


class Listado(ListView):
    model = Producto
    template_name = "tienda/productoCRUD/listado.html"


class Editar(UpdateView):
    model = Producto
    template_name = "tienda/productoCRUD/editar.html"
    fields = '__all__'
    success_url = reverse_lazy('listado')


class Eliminar(DeleteView):
    model = Producto
    template_name = "tienda/productoCRUD/eliminar.html"
    success_url = reverse_lazy ('listado')


class Añadir(CreateView):
    model = Producto
    template_name = "tienda/productoCRUD/añadir.html"
    fields = '__all__'
    success_url = reverse_lazy('listado')

class Comprar(ListView):
    model = Producto
    template_name = "tienda/compra/compra.html"
    
    def get_context_data(self,**kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            context['listado'] = Producto.objects.all()

            todosProductos =[]
            for producto in Producto.objects.all():
                if producto.marca not in todosProductos:
                    todosProductos.append(producto.marca)
            context['crearFiltro'] = todosProductos

            marcaSeleccionada = self.request.GET.get('marca')
            if marcaSeleccionada:
                context['listadoFiltrosMarca'] = marcaSeleccionada
                context['listado'] = context['listado'].filter(marca__nombre=marcaSeleccionada)
            return context


class Checkout(View):
    templateList = "tienda/compra/checkout.html"

    def get (self,request, pk):
        producto = get_object_or_404(Producto,pk=pk)
        return render(request,self.templateList,{'producto' : producto})

    def post (self, request, pk):

        producto = get_object_or_404(Producto, pk=pk)
        unidades = int(request.POST.get('unidades'))

        if producto.unidades >= unidades:
            producto.unidades = producto.unidades - unidades
            producto.save()

            Compra.objects.create(
                    fecha = datetime.now(),
                    producto = producto,
                    unidades = unidades,
                    user = request.user,
                    importe = producto.precio * unidades,
            )

            return redirect ('comprar')
        return render(request, "tienda/compra/confirmacionCompra.html")
    
# Comienzo punto de control, comienzo informes

class Informes(ListView):
    model = Producto
    template_name = "tienda/informes/informes.html"

class InformeMarca(ListView):
    model = Producto
    template_name = 'tienda/informes/informeMarca.html'

    def get_context_data(self,**kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['listado'] = Producto.objects.all()

        todosProductos =[]
        for producto in Producto.objects.all():
            if producto.marca not in todosProductos:
                todosProductos.append(producto.marca)
        context['crearFiltro'] = todosProductos

        marcaSeleccionada = self.request.GET.get('marca')
        if marcaSeleccionada:
            context['listadoFiltrosMarca'] = marcaSeleccionada
            context['listado'] = context['listado'].filter(marca__nombre=marcaSeleccionada)
        return context
    

class InformeCompraUsuario(ListView):
    model = Compra
    template_name = "tienda/informes/informeCompraUsuario.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listadoCompras'] = Compra.objects.all()

        todosUsuarios =[]
        for user in User.objects.all():
            if user.username not in todosUsuarios:
                todosUsuarios.append(user.username)
        context['crearFiltro'] = todosUsuarios

        usuarioSeleccionado = self.request.GET.get('user')
        if usuarioSeleccionado:
            context['listadoUsers'] = User.objects.all().filter(username=usuarioSeleccionado)
            context ['listadoCompras'] = context ['listadoCompras'].filter(user__username=usuarioSeleccionado)
        context['usuarioSeleccionado'] = usuarioSeleccionado
        return context


class InformeTopTenProductos(ListView):
    model = Compra
    template_name = "tienda/informes/informeTopTenProductos.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['listado'] = Compra.objects.annotate(sumVentas = Sum('importe'),sumUnidades = Sum('unidades')).order_by('-sumVentas')[:10]
        return context
    


class InformeTopTenClientes(ListView):
    model = Compra
    template_name = "tienda/informes/informeTopTenClientes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listadoUsuarios'] = Compra.objects.annotate(sumGastado = Sum('importe')).order_by('-sumGastado')[:10]
        return context