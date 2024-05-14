from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100, label='Nombres')
    apellidos = forms.CharField(max_length=100, label="Apellidos")
    num_telefono = forms.CharField(max_length=10, label="Num. Teléfono")
    
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'num_telefono', 'correo', 'activo']
