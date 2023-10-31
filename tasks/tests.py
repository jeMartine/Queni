from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CrearGasto, IngresarIngresos

class TestInforme(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
    def test_creacion_y_descarga_de_informe(self):
        
        
        CrearGasto.objects.create(user=self.user, Nombre='Comida', Valor=50)
       

        IngresarIngresos.objects.create(user=self.user, Nombre='Salario', Cantidad=1000)
        
        
        response = self.client.get(reverse('verBalance'))
        self.assertEqual(response.status_code, 200)
        

        response = self.client.post(reverse('verBalance'), {
            'fecha_inicio': '2023-08-01',
            'fecha_fin': '2023-08-31',
        })
        self.assertEqual(response.status_code, 200)
        

        self.assertEqual(response['Content-Type'], 'application/pdf')
        
       
        self.assertTrue('Content-Disposition' in response)
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename="balance_report.pdf"'))
        
    def tearDown(self):
        self.client.logout()