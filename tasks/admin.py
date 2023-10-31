from django.contrib import admin
from .models import CrearGasto, IngresarIngresos

class CrearGastoAdmin(admin.ModelAdmin):
    readonly_fields = ("datecreated",)

class IngresarIngresosAdmin(admin.ModelAdmin):
    readonly_fields = ("FechaDeRegistro",)


admin.site.register(CrearGasto, CrearGastoAdmin)


admin.site.register(IngresarIngresos, IngresarIngresosAdmin)
