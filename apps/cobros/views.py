from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Servicio, Producto, ProductoEnTicket
from datetime import datetime

@login_required
def cobros(request):
    servicio_id = request.GET.get('servicio_id')
    contexto = {}

    if servicio_id:
        servicio = get_object_or_404(Servicio, id=servicio_id)
        contexto['servicio'] = servicio
        contexto['fecha_actual'] = datetime.now().strftime('%d/%m/%Y')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_product':
            producto_id = request.POST.get('producto_id')
            cantidad = int(request.POST.get('cantidad', 1))
            producto = get_object_or_404(Producto, id=producto_id)
            ProductoEnTicket.objects.create(servicio=servicio, producto=producto, cantidad=cantidad)
        elif action == 'update_product':
            pet_id = request.POST.get('pet_id')
            new_cantidad = int(request.POST.get('cantidad', 1))
            pet = get_object_or_404(ProductoEnTicket, id=pet_id)
            pet.cantidad = new_cantidad
            pet.save()
        elif action == 'delete_product':
            pet_id = request.POST.get('pet_id')
            pet = get_object_or_404(ProductoEnTicket, id=pet_id)
            pet.delete()

        return JsonResponse({'status': 'ok'})

    contexto['productos_en_ticket'] = ProductoEnTicket.objects.filter(servicio=contexto.get('servicio'))
    return render(request, 'cobros.html', contexto)

def detalles_producto(request):
    if request.method == 'GET' and 'producto_id' in request.GET:
        producto_id = request.GET.get('producto_id')
        producto = get_object_or_404(Producto, id=producto_id)
        data = {'nombre': producto.nombre, 'precio': producto.precio}
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'ID de producto no proporcionado'})

def buscar_producto(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        if query:
            productos = Producto.objects.filter(nombre_icontains=query)
        else:
            productos = Producto.objects.none()

        data = {'productos': [{'id': producto.id, 'nombre': producto.nombre} for producto in productos]}
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'La solicitud no fue de tipo GET'})
