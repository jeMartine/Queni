from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Miembro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    miembros = models.ManyToManyField(User, related_name='grupos', blank=True)

    def __str__(self):
        return self.nombre
    
def create_default_group(sender, instance, created, **kwargs):
    if created:
        grupo_sin_nombre, _ = Grupo.objects.get_or_create(nombre="Sin Grupo", descripcion="Grupo predeterminado")
        instance.grupo = grupo_sin_nombre
        instance.save()

class CrearGasto(models.Model):
    # Campos existentes
    Nombre = models.CharField(max_length=50)
    TIPO_GASTO_CHOICES = [
        ('servicios', 'Servicio'),
        ('deuda', 'Deuda'),
        ('comida', 'Comida'),
        ('hogar', 'Hogar'),
        ('educacion','Educacion'),
        ('ocio','Ocio'),
        ('otros', 'Otros'),
    ]
    TipoGasto = models.CharField(max_length=50, choices=TIPO_GASTO_CHOICES)
    Descripcion = models.TextField(blank=True)
    Valor = models.BigIntegerField(default=0, blank=True, null=True)
    datecreated = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True, related_name='gastos')

    def __str__(self):
        return self.Nombre + ' creado por: ' + self.user.username

class IngresarIngresos(models.Model):
    Nombre = models.CharField(max_length=50)
    Cantidad = models.BigIntegerField(default=0, blank=True, null=True)
    FechaDeRegistro = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)