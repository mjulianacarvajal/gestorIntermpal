from django.contrib import admin
from .models import Empresa, Sede, Bus, Programado, Despachado
# Register your models here.
admin.site.register(Empresa)
admin.site.register(Sede)
admin.site.register(Bus)
admin.site.register(Programado)
admin.site.register(Despachado)