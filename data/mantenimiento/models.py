from django.db import models
from django.contrib.auth.models import User 

class Activo(models.Model):
    NIVEL_CRITICIDAD = [
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del Equipo")
    codigo_interno = models.CharField(max_length=50, unique=True, verbose_name="Código (Tag)")
    marca = models.CharField(max_length=50)
    fecha_instalacion = models.DateField(verbose_name="Fecha de Instalación")
    criticidad = models.CharField(max_length=5, choices=NIVEL_CRITICIDAD, default='MEDIA')

    def __str__(self):
        return f"{self.codigo_interno} - {self.nombre}"

    class Meta:
        verbose_name = "Activo"
        verbose_name_plural = "Activos"


class PerfilUsuario(models.Model):
    ROLES = [
        ('ADMIN', 'Administrador de Contrato'),
        ('JEFE', 'Jefe de Mantenimiento'),
        ('TECNICO', 'Técnico de Terreno'),
    ]
    
    user = models.OneToOneField(User, on_extended_user=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLES, default='TECNICO')
    especialidad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
            