from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf.urls.static import static

app_name = 'tasks'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('signup/',views.signup, name = 'signup'),
    path('verGastos/',views.verGastos, name = 'verGastos'),
    path('verGastos/completados/',views.verGastosCompletados, name = 'verGastosCompletados'),
    path('verGastos/crearGastos/',views.crearGastos, name = 'crearGastos'),
    path('ingresarIngresos/',views.ingresarIngresos, name = 'ingresarIngresos'),
    path('verIngresos/',views.verIngresos, name = 'verIngresos'),
    path('verIngresos/<int:ingreso_id>/', views.ingresoDetail, name='ingresoDetail'),
    path('verIngresos/<int:ingreso_id>/delete/', views.deleteIngreso, name= 'deleteIngreso'),
    path('logout/', views.signout, name = 'logout'),
    path('signin/', views.signin,name = 'signin'),
    path('verGastos/<int:gasto_id>/', views.gastoDetail, name= 'gastoDetail'),
    path('verGastos/<int:gasto_id>/complete/', views.completeGasto, name= 'completeGasto'),
    path('verGastos/<int:gasto_id>/delete/', views.deleteGasto, name= 'deleteGasto'),
    path('verBalance/', views.verBalance, name='verBalance'),
    path('verBalance/pdf/', views.verBalance_pdf, name='verBalance_pdf'),
    path('lista_grupos/', views.lista_grupos, name='lista_grupos'),
    path('crear_grupo/', views.crear_grupo, name='crear_grupo'),
    path('unirse_grupo/<int:grupo_id>/', views.unirse_grupo, name='unirse_grupo'),
    path('crear_grupo/lista_grupos/', views.lista_grupos, name='lista_grupos'),
    path('estadisticas/', views.estadisticas, name='estadisticas')
]

