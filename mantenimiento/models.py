# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
class Clientes(models.Model):
    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=20, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = PhoneNumberField(region="CL", blank=True, null=True)

    # El save SIEMPRE va al final, después de los campos
    def save(self, *args, **kwargs):
        rut_limpio = str(self.rut).replace(".", "").replace("-", "").upper()
        if len(rut_limpio) > 1:
            cuerpo = rut_limpio[:-1]
            dv = rut_limpio[-1]
            try:
                cuerpo_formateado = "{:,}".format(int(cuerpo)).replace(",", ".")
                self.rut = f"{cuerpo_formateado}-{dv}"
            except:
                pass
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'clientes'


class Equipos(models.Model):
    tag = models.CharField(unique=True, max_length=50)
    nombre = models.CharField(max_length=150)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, blank=True, null=True)
    estrategia = models.ForeignKey('Estrategias', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipos'


class Estrategias(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estrategias'


class EventosFalla(models.Model):
    equipo_id = models.IntegerField(blank=True, null=True)
    descripcion_problema = models.TextField()
    prioridad = models.CharField(max_length=20, blank=True, null=True)
    fecha_reporte = models.DateTimeField(blank=True, null=True)
    reportado_por = models.CharField(max_length=100, blank=True, null=True)
    ot_generada_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventos_falla'


class Horometros(models.Model):
    equipo = models.ForeignKey(Equipos, models.DO_NOTHING, blank=True, null=True)
    valor_acumulado = models.IntegerField()
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'horometros'


class OrdenesTrabajo(models.Model):
    equipo = models.ForeignKey(Equipos, models.DO_NOTHING, blank=True, null=True)
    plan = models.ForeignKey('Planes', models.DO_NOTHING, blank=True, null=True)
    fecha_programada = models.DateField()
    fecha_ejecucion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ordenes_trabajo'


class Planes(models.Model):
    equipo = models.ForeignKey(Equipos, models.DO_NOTHING, blank=True, null=True)
    descripcion_tarea = models.TextField()
    frecuencia_horas = models.IntegerField()
    ultimo_mantenimiento_horas = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'planes'
