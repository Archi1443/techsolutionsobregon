from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from apps.servicios.models import Servicio
from apps.clientes.models import Cliente, Celular
from techsolutionswebsite import settings
from django.contrib import messages
from .forms import ServicioRegistroForm, ServicioModificacionForm, AccionesServicioFormSet, AccionesServicioForm
from django.forms import inlineformset_factory
from .models import Servicio, AccionesServicio
from django.forms import BaseInlineFormSet
from django.core.mail import send_mail
from django.conf import settings
from apps.utils import enviar_correo


@login_required
def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    if request.method == 'POST':
        try:
            servicio.delete()
            messages.success(request, 'Servicio eliminado con éxito.')
            return redirect('servicios_gestion')
        except Exception as e:
            messages.error(request, f'Error al eliminar el servicio: {str(e)}')
            return redirect('servicios_gestion')
    else:
        messages.error(request, 'Método no permitido')
        return redirect('servicios_gestion')

AccionesServicioFormSet = inlineformset_factory(
    Servicio, AccionesServicio, form=AccionesServicioForm,
    fields=['descripcion', 'costo', 'foto_antes', 'foto_despues', 'empleado'], extra=1, can_delete=False)

class CustomInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data and not form.has_changed():
                form.cleaned_data['DELETE'] = True  # Marcar para eliminación si no se cambiaron datos


@login_required
def servicios_editar(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    AccionesServicioFormSet = inlineformset_factory(
        Servicio,
        AccionesServicio,
        form=AccionesServicioForm,
        formset=CustomInlineFormSet,  # Usar el FormSet personalizado
        fields=('empleado', 'descripcion', 'costo', 'foto_antes', 'foto_despues'),
        extra=1,
        can_delete=False
    )

    if request.method == 'POST':
        form = ServicioModificacionForm(request.POST or None, request.FILES or None, instance=servicio)
        formset = AccionesServicioFormSet(request.POST or None, request.FILES or None, instance=servicio)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'El servicio ha sido actualizado exitosamente.')
            enviar_correo(
                destinatario=servicio.cliente.correo,
                asunto='Actualización de su Servicio en Tech Solutions',
                mensaje='Su servicio ha sido actualizado exitosamente.'
            )
            return redirect('servicios_gestion')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
            
    else:
        form = ServicioModificacionForm(instance=servicio)
        formset = AccionesServicioFormSet(instance=servicio)

    return render(request, 'servicios_modificar.html', {
        'form': form,
        'formset': formset,
        'servicio': servicio
    })



@login_required()
def servicios(request):
    return render(request, 'servicios.html', {})


@login_required()
def filtrar_servicios(request):
    estado_busqueda = request.GET.get('estadoBusqueda')
    tipo_busqueda = request.GET.get('tipoBusqueda')
    query = request.GET.get('valorBusqueda')

    services = Servicio.objects.filter(estado=estado_busqueda)
    if tipo_busqueda == 'num_telefono':
        clientes = Cliente.objects.filter(num_telefono=query)
        cliente_ids = clientes.values_list('id', flat=True)
        services = services.filter(cliente_id__in=cliente_ids)
    elif tipo_busqueda == 'imei':
        celulares = Celular.objects.filter(imei=query)
        celular_ids = celulares.values_list('id', flat=True)
        services = services.filter(celular_id__in=celular_ids)

    data = []
    estados = {
        'ingresado': 'Ingresado',
        'en_proceso': 'En Proceso',
        'finalizado': 'Finalizado',
        'entregado': 'Entregado'
    }
    for service in services:
        data.append({
            'id': service.id,
            'cliente': service.cliente.nombre + " " + service.cliente.apellidos,
            'imei': service.celular.imei,
            'marca': service.celular.marca,
            'modelo': service.celular.modelo,
            'estado': estados[service.estado],
            'descripcion': service.descripcion,
        })
    return JsonResponse(data, safe=False)

@login_required
def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    if request.method == 'POST':
        try:
            servicio.delete()
            messages.success(request, 'Servicio eliminado con éxito.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el servicio: {str(e)}')
        return redirect('servicios_gestion')
    else:
        messages.error(request, 'Método no permitido')
        return redirect('servicios_gestion')


@login_required()
def servicios_registro(request):
    if request.method == 'POST':
        form = ServicioRegistroForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            try:
                cliente = Cliente.objects.get(num_telefono=request.POST.get('num_telefono'))
            except Cliente.DoesNotExist:
                return render(request, 'servicios_form.html', {'form': form})

            celular, created = Celular.objects.get_or_create(
                cliente=cliente,
                imei=request.POST.get('imei'),
                defaults={
                    'marca': request.POST.get('marca'),
                    'modelo': request.POST.get('modelo'),
                    'clave_desbloqueo': request.POST.get('clave_desbloqueo')
                }
            )

            servicio.cliente = cliente
            servicio.celular = celular
            servicio.save()
            return JsonResponse({'servicioId': servicio.id})
        else:
            print(form.errors)  
    else:
        form = ServicioRegistroForm()
    return render(request, 'servicios_form.html', {'form': form})






@login_required()
def buscar_cliente(request):
    if request.method == 'GET' and 'num_telefono' in request.GET:
        num_telefono = request.GET['num_telefono']
        try:
            cliente = Cliente.objects.get(num_telefono=num_telefono)
            data = {'cliente': cliente.nombre + " " + cliente.apellidos}
            return JsonResponse(data)
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required()
def servicios_consulta(request, id):
    try:
        servicio = Servicio.objects.get(id=id)
        acciones = AccionesServicio.objects.filter(servicio=servicio)
    except Servicio.DoesNotExist:
        return render(request, 'error.html', {'error': 'Servicio no encontrado'})

    return render(request, 'servicios_consulta.html', {
        'servicio': servicio,
        'cliente': servicio.cliente,
        'celular': servicio.celular,
        'acciones': acciones 
    })





@login_required()
def servicios_gestion(request):
    services = Servicio.objects.all()
    icono_ts_path = '/' + settings.STATIC_URL + 'img/icono_ts.png'
    editar_ts_path = '/' + settings.STATIC_URL + 'img/editar_ts.png'
    logout_ts_path = '/' + settings.STATIC_URL + 'img/logout_ts.png'
    return render(request, 'servicios_gestion.html', {
        'servicios': services,
        'icono_ts_path': icono_ts_path,
        'editar_ts_path': editar_ts_path,
        'logout_ts_path': logout_ts_path,
    })


#@login_required
#def servicios_editar(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    if request.method == 'POST':
        form = ServicioModificacionForm(request.POST, request.FILES, instance=servicio)
        formset = AccionesServicioFormSet(request.POST, request.FILES, instance=servicio)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return JsonResponse({'servicioId': servicio.id})
        else:
            # Manejar los errores de formulario aquí
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = ServicioModificacionForm(instance=servicio)
        formset = AccionesServicioFormSet(instance=servicio)
    # Si es GET, renderizar la página con los formularios
    return render(request, 'servicios_modificar.html', {
        'form': form,
        'formset': formset,
        'servicio': servicio
    })

