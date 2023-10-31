from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Grupo, Miembro
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import CrearGastoForm, IngresarIngresosForm
from .models import CrearGasto, IngresarIngresos
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Sum
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from .models import Grupo
from .forms import GrupoForm 
from django.http import JsonResponse
import matplotlib.pyplot as plt
from io import BytesIO
from django.template.loader import get_template
from django.utils.timezone import make_aware



# Create your views here.
def home(request):
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'GET':
            return render(request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'
        })
        return render(request, 'signup.html',{
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })

@login_required 
def verGastos(request):
    gastos = CrearGasto.objects.filter(user=request.user, datecompleted__isnull=True ) 
    
    return render(request, 'verGastos.html',{'Gastos' : gastos})

@login_required 
def verGastosCompletados(request):
    gastos = CrearGasto.objects.filter(user=request.user, datecompleted__isnull=False).order_by
    ('-datecompleted') 
    
    return render(request, 'verGastos.html',{'Gastos' : gastos})

@login_required 
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
     if request.method=='GET':
          return render(request, 'signin.html', {
               'form': AuthenticationForm
          })
     else:
          user = authenticate(request, username=request.POST['username'], password=request.POST
                       ['password'])
          if user is None:
            return render(request, 'signin.html',{
               'form': AuthenticationForm,
               'error': 'El usuario o la contraseña son incorrectos'
          })   
          else:
              login(request, user)
              return redirect('verGastos')
          

@login_required 
def crearGastos(request):
    if request.method == 'GET':
        return render(request, 'crearGastos.html', {'form': CrearGastoForm})
    else:
        try:
            form = CrearGastoForm(request.POST)
            new_gasto = form.save(commit=False)
            new_gasto.user = request.user 
            new_gasto.save()
            return redirect('verGastos')  
        except ValueError:
            return render(request, 'crearGastos.html', {
                'form': CrearGastoForm(),
                'error': 'Ingresa datos válidos'
            })

        
@login_required         
def gastoDetail(request, gasto_id):

    if request.method == 'GET':
        crearGasto = get_object_or_404(CrearGasto, pk=gasto_id, user = request.user)
        form = CrearGastoForm(instance = crearGasto)
        return render(request, 'gastoDetail.html' , {'gasto' : crearGasto, 'form' : form})
    else:
        try:
            crearGasto = get_object_or_404 (CrearGasto, pk = gasto_id)
            form = CrearGastoForm(request.POST, instance = crearGasto)
            form.save()
            return redirect('verGastos')
        except ValueError:
            return render(request, 'gastoDetail.html' , {'gasto' : crearGasto, 'form' : form, 
            'error' : "Error actualizando el gasto"})

@login_required 
def completeGasto(request, gasto_id):
    crearGastos = get_object_or_404(CrearGasto, pk = gasto_id, user = request.user)
    if request.method == 'POST':
        crearGastos.datecompleted = timezone.now()
        crearGastos.save()
        return redirect('verGastos')
    
@login_required 
def deleteGasto(request, gasto_id):
    crearGastos = get_object_or_404(CrearGasto, pk = gasto_id, user = request.user)
    if request.method == 'POST':
        crearGastos.delete()
        return redirect('verGastos')
    

@login_required 
def ingresarIngresos(request):
    if request.method == 'GET':
        return render(request, 'ingresarIngresos.html', {'form': IngresarIngresosForm})
    else:
        try:
            form = IngresarIngresosForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user 
            new_task.save()
            return redirect(reverse('verIngresos')) 
        except ValueError:
            return render(request, 'ingresarIngresos.html', {
                'form': IngresarIngresosForm,
                'error': 'Ingresa datos válidos'}
            )

@login_required 
def verIngresos(request):
    if request.method == 'GET':
        # Obtenemos el mes y año actual
        now = datetime.now()
        year = now.year
        month = now.month
        
        # Definimos la fecha de inicio y fin del mes actual
        first_day = datetime(year, month, 1)
        last_day = first_day + timedelta(days=30)
        
        # Filtramos los ingresos por usuario y fecha
        ingresos = IngresarIngresos.objects.filter(user=request.user, FechaDeRegistro__range=[first_day, last_day])
        
        return render(request, 'verIngresos.html', {'Ingresos': ingresos})
@login_required         
def ingresoDetail(request, ingreso_id):
    ingresarIngresos = get_object_or_404(IngresarIngresos, pk=ingreso_id, user=request.user)
    
    if request.method == 'GET':
        form = IngresarIngresosForm(instance=ingresarIngresos)
        return render(request, 'ingresoDetail.html', {'ingreso': ingresarIngresos, 'form': form})
    else:
        form = IngresarIngresosForm(request.POST, instance=ingresarIngresos)
        if form.is_valid():
            form.save()
            return redirect('verIngresos')  # Redirige a la lista de ingresos después de actualizar
        else:
            return render(request, 'ingresoDetail.html', {'ingreso': ingresarIngresos, 'form': form, 
                                                         'error': "Error al actualizar el ingreso. Por favor, verifica los datos."})

@login_required 
def deleteIngreso(request, ingreso_id):
    ingresarIngresos = get_object_or_404(IngresarIngresos, pk=ingreso_id, user=request.user)
    if request.method == 'POST':
        ingresarIngresos.delete()
        return redirect('verIngresos')
    
@login_required
def verBalance(request):
    template_path = 'verBalance_pdf.html'
    context = {
        'request': request,
    }
    
    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        
        gastos = CrearGasto.objects.filter(user=request.user, datecompleted__isnull=True, datecreated__gte=fecha_inicio, datecreated__lte=fecha_fin)
        ingresos = IngresarIngresos.objects.filter(user=request.user, FechaDeRegistro__gte=fecha_inicio, FechaDeRegistro__lte=fecha_fin)
        
        total_gastos = gastos.aggregate(Sum('Valor'))['Valor__sum']
        total_ingresos = ingresos.aggregate(Sum('Cantidad'))['Cantidad__sum']
        
        if total_gastos is None:
            total_gastos = 0
        
        if total_ingresos is None:
            total_ingresos = 0
        
        balance = total_ingresos - total_gastos
        
        context.update({
            'gastos': gastos,
            'ingresos': ingresos,
            'total_gastos': total_gastos,
            'total_ingresos': total_ingresos,
            'balance': balance,
        })
        
        # Generar el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="balance_report.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        
        return response
    
    return render(request, 'verBalance.html')

@login_required
def verBalance_pdf(request):
    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        
        gastos = CrearGasto.objects.filter(user=request.user, datecompleted__isnull=True, datecreated__gte=fecha_inicio, datecreated__lte=fecha_fin)
        ingresos = IngresarIngresos.objects.filter(user=request.user, FechaDeRegistro__gte=fecha_inicio, FechaDeRegistro__lte=fecha_fin)
        
        total_gastos = gastos.aggregate(Sum('Valor'))['Valor__sum']
        total_ingresos = ingresos.aggregate(Sum('Cantidad'))['Cantidad__sum']
        
        if total_gastos is None:
            total_gastos = 0
        
        if total_ingresos is None:
            total_ingresos = 0

        balance = total_ingresos - total_gastos

        if balance > 0:
            consejos = "¡Felicidades! Tu balance es positivo. Considera ahorrar e invertir una parte del excedente."
        elif balance < 0:
            consejos = "Tu balance es negativo. Revisa tus gastos y crea un plan para mejorar tu situación financiera."
        else:
            consejos = "Tu balance es neutral. Sigue gestionando tus ingresos y gastos de manera responsable."

        context = {
            'request': request,
            'gastos': gastos,
            'ingresos': ingresos,
            'total_gastos': total_gastos,
            'total_ingresos': total_ingresos,
            'balance': balance,
            'consejos': consejos,
        }

        # Generar el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="balance_report.pdf"'
        template_path = 'verBalance_pdf.html'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)

        return response

@login_required
def estadisticas(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        start_date = make_aware(datetime.strptime(start_date_str, '%Y-%m-%d'))
        end_date = make_aware(datetime.strptime(end_date_str, '%Y-%m-%d'))

        usuario = request.user

        # Calcular ingresos y gastos en el rango de fechas
        ingresos = IngresarIngresos.objects.filter(user=usuario, FechaDeRegistro__range=(start_date, end_date)).aggregate(Sum('Cantidad'))
        gastos = CrearGasto.objects.filter(user=usuario, datecreated__range=(start_date, end_date)).aggregate(Sum('Valor'))

        # Calcular saldo (ingresos - gastos)
        saldo = ingresos['Cantidad__sum'] - gastos['Valor__sum']

        return render(request, 'estadisticas.html', {'ingresos': ingresos, 'gastos': gastos, 'saldo': saldo})
    else:
        return render(request, 'seleccionar_fechas.html')
    
def crear_grupo(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.creador = request.user
            grupo.save()
            grupo.miembros.add(request.user)
            return redirect('lista_grupos')
    else:
        form = GrupoForm()
    return render(request, 'crear_grupo.html', {'form': form})


def lista_grupos(request):
    grupos = Grupo.objects.all()
    return render(request, 'lista_grupos.html', {'grupos': grupos})

def unirse_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    grupo.miembros.add(request.user)
    return redirect('lista_grupos')

