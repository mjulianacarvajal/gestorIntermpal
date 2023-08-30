from django.db import models
from django.utils import timezone
from django.db.models import Sum

#empresaxcategoria_
class Empresa(models.Model):
    nombre = models.CharField(max_length=250)
    caracteristicas = models.TextField()
    estado = models.CharField(max_length=2, choices=(('1', 'Activa'), ('2', 'Sin servicio')), default=1)
    fecha_creado = models.DateTimeField(default=timezone.now)
    fecha_actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

#tipo
class Sede(models.Model):
    sede = models.CharField(max_length=250)
    tipo = models.CharField(max_length=2, choices=(('1','Terminal'),('2','Oficina'),('3','Paradero')), default='1')
    fecha_creado = models.DateTimeField(default=timezone.now)
    fecha_actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sede


class Bus(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, blank=True, null=True)
    numero_bus = models.CharField(max_length=10)
    asientos = models.IntegerField(default=0)
    estado = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)
    fecha_creado = models.DateTimeField(default=timezone.now)
    fecha_actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.numero_bus


class Programado(models.Model):
    codigo = models.CharField(max_length=100)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    origen = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='origen')
    destino = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='destino')
    programado = models.DateTimeField()
    precio = models.FloatField()
    estado = models.CharField(max_length=2, choices=(('0','Cancelado'),('1','Programado')), default=1)
    fecha_creado = models.DateTimeField(default=timezone.now)
    fecha_actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.codigo + ' - ' + self.bus.numero_bus)

# restar asientos del bus -
    @property
    def count_asientosdisponibles(self):
        despachado = Despachado.objects.filter(programado=self).aggregate(Sum('asientos'))['asientos__sum']
        return self.bus.asientos - self.despachado.asientos


#despacho - existencia
class Despachado(models.Model):
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=250)
    programado = models.ForeignKey(Programado,on_delete=models.CASCADE)
    asientos = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=2, choices=(('1','Pendiente'),('2','Despachado')), default=1)
    fecha_creado = models.DateTimeField(default=timezone.now)
    fecha_actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.codigo + ' - ' + self.nombre)

#porcentajeocupacion_Salida
    def total_ocupacion(self):
        return self.asientos * self.programado.precio