from django import forms
from django.forms import ModelForm
from .models import CrearGasto
from .models import IngresarIngresos
from .models import Grupo

class CrearGastoForm(forms.ModelForm):
    class Meta:
        model = CrearGasto
        fields = ['Nombre', 'TipoGasto', 'Descripcion', 'Valor', 'important']

class IngresarIngresosForm(forms.ModelForm):
    class Meta:
        model = IngresarIngresos
        fields = ['Nombre', 'Cantidad', 'FechaDeRegistro']
        widgets = {
            'FechaDeRegistro': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre', 'descripcion'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'Nombre del Grupo'
        self.fields['descripcion'].widget = forms.Textarea(attrs={'rows': 4})
