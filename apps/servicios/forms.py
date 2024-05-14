from django import forms
from .models import Servicio, Celular, Cliente, AccionesServicio
from django.forms import inlineformset_factory
from django.forms import modelformset_factory




class ServicioRegistroForm(forms.ModelForm):
    num_telefono = forms.CharField(max_length=10, label='Num. Teléfono')
    imei = forms.CharField(max_length=15, label='Celular IMEI')
    marca = forms.CharField(max_length=100, required=False, label='Marca')
    modelo = forms.CharField(max_length=100, required=False, label='Modelo')
    clave_desbloqueo = forms.CharField(max_length=20, required=False, label='Clave desbloqueo')
    descripcion = forms.CharField(max_length=200, required=False, label='Descripción')
    cotizacion = forms.DecimalField(max_digits=10, required=False, decimal_places=2, label='Cotización')
    anticipo = forms.DecimalField(max_digits=10, required=False, decimal_places=2, label='Anticipo')  # Nuevo campo para el anticipo

    class Meta:
        model = Servicio
        fields = ['descripcion', 'cotizacion', 'anticipo']  # Añade el nuevo campo al formulario


    # Asumiendo que necesitas crear un nuevo Celular asociado en cada registro de Servicio
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            celular = Celular.objects.create(
                servicio=instance,
                imei=self.cleaned_data['imei'],
                marca=self.cleaned_data['marca'],
                modelo=self.cleaned_data['modelo']
            )
        return instance




from django import forms
from .models import Servicio, Celular, Cliente, AccionesServicio

class ServicioModificacionForm(forms.ModelForm):
    imei = forms.CharField(max_length=15, required=False, label='IMEI')
    marca = forms.CharField(max_length=100, required=False, label='Marca')
    modelo = forms.CharField(max_length=100, required=False, label='Modelo')
    clave_desbloqueo = forms.CharField(max_length=20, required=False, label='Clave desbloqueo')
    descripcion = forms.CharField(max_length=200, required=False, label='Descripción')
    # Reemplazar el campo cliente y celular por campos de texto
    cliente_nombre = forms.CharField(
        label='Cliente', 
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    numero_telefono = forms.CharField(
        label='Número de teléfono', 
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Servicio
        fields = ['cliente_nombre', 'numero_telefono', 'descripcion', 'cotizacion', 'estado', 'pagado', 'anticipo']

    def __init__(self, *args, **kwargs):
        super(ServicioModificacionForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.cliente:
            self.fields['cliente_nombre'].initial = self.instance.cliente.nombre + ' ' + self.instance.cliente.apellidos
            self.fields['numero_telefono'].initial = self.instance.cliente.num_telefono
            if hasattr(self.instance, 'celular'):
                self.fields['imei'].initial = self.instance.celular.imei
                self.fields['marca'].initial = self.instance.celular.marca
                self.fields['modelo'].initial = self.instance.celular.modelo
                self.fields['clave_desbloqueo'].initial = self.instance.celular.clave_desbloqueo

        # Asegurar que todos los campos sean opcionales
        for field_name in self.fields:
            self.fields[field_name].required = False







AccionesServicioFormSet = inlineformset_factory(
    Servicio, 
    AccionesServicio, 
    fields=('empleado', 'descripcion', 'costo', 'foto_antes', 'foto_despues'), 
    extra=1, 
    can_delete=False
)

class AccionesServicioForm(forms.ModelForm):
    class Meta:
        model = AccionesServicio
        fields = ['empleado', 'descripcion', 'costo', 'foto_antes', 'foto_despues']
        widgets = {
            'descripcion': forms.Textarea(attrs={'required': False}),
            'costo': forms.NumberInput(attrs={'required': False}),
            'foto_antes': forms.FileInput(attrs={'required': False}),
            'foto_despues': forms.FileInput(attrs={'required': False}),
        }

AccionesServicioFormSet = inlineformset_factory(
    Servicio, 
    AccionesServicio, 
    form=AccionesServicioForm,
    extra=1,  # Número de formas extras que deseas mostrar
    can_delete=False  # Permite marcar instancias para eliminación
)



