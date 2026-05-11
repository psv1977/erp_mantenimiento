from django.contrib import admin
from .models import Activo, PerfilUsuario  # Importamos el nuevo modelo

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('codigo_interno', 'nombre', 'marca', 'criticidad', 'fecha_instalacion')
    search_fields = ('nombre', 'codigo_interno')
    list_filter = ('criticidad', 'marca')

# Registro del Perfil de Usuario
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'especialidad')
    list_filter = ('rol',)

    