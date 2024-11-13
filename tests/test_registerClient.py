import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from register.models import ClientProfile

class RegisterClientTest(TestCase):
    def setUp(self):
        self.url = reverse('register_client')

    def test_register_client_success(self):
        data = {
            'username': 'client2',
            'email': 'client2@example.com',
            'password1': 'StrongPassword2024!@',
            'password2': 'StrongPassword2024!@',
            'company_nit': '666',
            'company_name': 'Test Company',
            'business_type': 'IT',
            'country': '1',  # ID del país
            'business_vertical': '1',  # ID de la vertical de negocio
            'city': '1',  # ID de la ciudad
            'address': '123 Business St',
            'phone_number': '5551234567',
            'legal_representative': 'John Doe',
            'profile_photo': None,  # Opcional
            'client_description': 'Descripción de la empresa'
        }

        # Realizamos una solicitud POST con los datos de registro
        response = self.client.post(self.url, data)

        # Verificamos que la respuesta sea una redirección
        self.assertRedirects(response, reverse('clientHome'))
        
        # Verificamos que el usuario se haya creado
        self.assertTrue(User.objects.filter(username='client2').exists())
        
        time.sleep(10)
        
        # Verificamos que el perfil del cliente se haya creado
        self.assertTrue(ClientProfile.objects.filter(user__username='client2').exists())

    def test_register_client_invalid_data(self):
        data = {
            'username': 'invalidclient',
            'email': 'invalidclient@example.com',
            'password1': 'password123',
            'password2': 'differentpassword',
            'company_nit': '987654321',
            'company_name': 'Invalid Company',
            'business_type': 'IT',
            'country': '1',
            'business_vertical': '1',  # ID de la vertical de negocio
            'city': '1',
            'address': '1',
            'phone_number': '5559876543',
            'legal_representative': 'Jane Doe',
            'profile_photo': None,
            'client_description': 'Invalid client description'
        }

        # Realizamos una solicitud POST con los datos inválidos
        response = self.client.post(self.url, data)

        # Verificamos que la respuesta sea 200 y se muestren los errores
        self.assertEqual(response.status_code, 200)
        
        time.sleep(10)

        # Verificamos que los errores de la contraseña se muestren correctamente
        self.assertFormError(response, 'user_form', 'password2', 'Las contraseñas no coinciden.')

    def tearDown(self):
            """
            Limpiar la base de datos después de cada prueba.
            """
            # Elimina cualquier dato creado en la base de datos
            User.objects.filter(username='client2').delete()
            ClientProfile.objects.filter(user__username='client2').delete()