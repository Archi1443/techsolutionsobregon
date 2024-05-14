from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from apps.empleados.models import Empleado
from apps.empleados.forms import EmpleadoForm



@login_required
def empleados_modificar(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    user = empleado.usuario

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('empleados_gestion')
    else:
        initial_data = {
            'nombre': empleado.nombre,
            'apellidos': empleado.apellidos,
            'num_telefono': empleado.num_telefono,
            'rfc': empleado.rfc,
            'cargo': empleado.cargo,
            'username': user.username,
            'email': user.email,
        }
        form = EmpleadoForm(instance=user, initial=initial_data)

    return render(request, 'empleados_modificar.html', {'form': form, 'empleado': empleado})



@login_required
def empleados(request):
    return render(request, 'empleados.html', {})

@login_required
def empleados_registro(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empleados_gestion')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados_form.html', {'form': form})

@login_required
def empleados_gestion(request):
    try:
        empleados = Empleado.objects.all()
        return render(request, 'empleados_gestion.html', {'empleados': empleados})
    except Exception as e:
        print("Error al cargar los empleados:", e)
        # Puedes pasar un mensaje de error al contexto para mostrarlo en la plantilla
        return render(request, 'empleados_gestion.html', {'error': 'Error al cargar los empleados.'})


@login_required
def eliminar_empleado(request, id):
    if request.method == 'POST':
        try:
            empleado = Empleado.objects.get(pk=id)
            empleado.delete()
            return JsonResponse({'success': True})
        except Empleado.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Empleado no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
    
@login_required
def buscar_empleado(request):
    query = request.GET.get('q', '')
    try:
        empleados = Empleado.objects.filter(nombre__icontains=query)
        data = list(empleados.values('id', 'nombre', 'apellidos', 'num_telefono', 'rfc', 'cargo', 'activo')) # Ajusta según tu modelo
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(f"Error al buscar empleados: {e}")
        return JsonResponse({'error': 'Error al buscar empleados'}, status=500)  
