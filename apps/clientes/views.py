from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Cliente
from django.conf import settings
from django.http import JsonResponse
from .forms import ClienteForm
from django.contrib import messages


@login_required()
def clientes(request):
    return render(request, 'clientes.html', {})


@login_required()
def clientes_registro(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.activo = True  # Establecer activo como True
            cliente.save()
            return redirect('/home')
    else:
        form = ClienteForm()
    return render(request, 'clientes_form.html', {
        'form': form
    })



@login_required()
def clientes_gestion(request):
    clients = Cliente.objects.all()
    icono_ts_path = settings.STATIC_URL + 'img/icono_ts.png'
    logout_ts_path = settings.STATIC_URL + 'img/logout_ts.png'
    return render(request, 'clientes_gestion.html', {
        'clientes': clients,
        'icono_ts_path': icono_ts_path,
        'logout_ts_path': logout_ts_path,
    })


@login_required()
def filtrar_clientes(request):
    tipo_busqueda = request.GET.get('type')
    query = request.GET.get('query')

    if tipo_busqueda == 'id':
        clients = Cliente.objects.filter(id=query)
    elif tipo_busqueda == 'nombre':
        clients = Cliente.objects.filter(nombre__icontains=query)
    else:
        clients = Cliente.objects.filter(num_telefono=query)

    data = []
    for client in clients:
        data.append({
            'id': client.id,
            'nombre': client.nombre,
            'apellidos': client.apellidos,
            'num_telefono': client.num_telefono,
            'correo': client.correo,
            'activo': client.activo
        })
    return JsonResponse(data, safe=False)

@login_required()
def clientes_modificar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.activo = True  # Establecer activo como True
            cliente.save()
            messages.success(request, "Cliente actualizado con éxito.")
            return redirect('clientes_gestion')
        else:
            messages.error(request, "Error al actualizar el cliente.")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes_modificar.html', {
        'form': form, 'cliente': cliente
    })
