# Generated by Django 5.0.6 on 2024-05-12 16:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('num_telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('rfc', models.CharField(max_length=13)),
                ('cargo', models.CharField(choices=[('gerente', 'Gerente'), ('tecnico', 'Técnico'), ('asistente', 'Asistente')], default='técnico', max_length=25)),
                ('activo', models.BooleanField(default=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='empleado', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
