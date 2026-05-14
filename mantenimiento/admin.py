from django.contrib import admin
# Importa tus modelos (asegúrate de que los nombres coincidan con models.py)
from .models import Clientes, Estrategias, Equipos, Planes, Horometros, OrdenesTrabajo
from phonenumber_field.widgets import PhoneNumberPrefixWidget

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'telefono')

    # Esta es la forma correcta de inyectar el widget del teléfono
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'telefono':
            kwargs['widget'] = PhoneNumberPrefixWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)

@admin.register(Equipos)
class EquiposAdmin(admin.ModelAdmin):
    list_display = ('tag', 'nombre', 'cliente')

@admin.register(Estrategias)
class EstrategiasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Planes)
class PlanesAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'descripcion_tarea', 'frecuencia_horas')

@admin.register(Horometros)
class HorometrosAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'valor_acumulado', 'fecha_lectura')

@admin.register(OrdenesTrabajo)
class OrdenesTrabajoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'fecha_programada', 'estado')