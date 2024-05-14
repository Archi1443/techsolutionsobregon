from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from apps.empleados.models import Empleado

class EmpleadoForm(UserCreationForm):
    CARGO_CHOICES = [
        ('gerente', 'Gerente'),
        ('tecnico', 'Técnico'),
        ('asistente', 'Asistente'),
    ]

    nombre = forms.CharField(max_length=100, label='Nombres')
    apellidos = forms.CharField(max_length=100, label='Apellidos')
    num_telefono = forms.CharField(
        max_length=10,
        label='Num. Teléfono',
        validators=[
            RegexValidator(
                regex='^\d{10}$',
                message='Introduce un número válido de 10 dígitos.'
            )
        ]
    )
    rfc = forms.CharField(max_length=13, label='RFC')
    cargo = forms.ChoiceField(choices=CARGO_CHOICES, label="Cargo")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Usuario',
            'email': 'Correo',
            'password1': 'Contraseña',
            'password2': 'Confirmación de contraseña'
        }
        help_texts = {
            'username': 'Hasta 150 caracteres. Letras, dígitos y @/./+/-/_ solamente.',
            'email': 'Introduce una dirección de correo electrónico válida.',
            'password1': 'Crea una contraseña.',
            'password2': 'Repite la contraseña.'
        }
        error_messages = {
            'username': {
                'invalid': 'Este nombre de usuario contiene caracteres inválidos.',
                'unique': 'Un usuario con este nombre ya existe.'
            },
            'email': {
                'invalid': 'Introduce una dirección de correo válida.'
            }
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
            empleado, created = Empleado.objects.get_or_create(usuario=user)
            empleado.nombre = self.cleaned_data['nombre']
            empleado.apellidos = self.cleaned_data['apellidos']
            empleado.num_telefono = self.cleaned_data['num_telefono']
            empleado.rfc = self.cleaned_data['rfc']
            empleado.cargo = self.cleaned_data['cargo']
            empleado.save()
        return user
