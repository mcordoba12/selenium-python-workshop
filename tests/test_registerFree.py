from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from register.models import Freelancer_Profile

User = get_user_model()

class RegisterFreelancerTest(TestCase):
    def setUp(self):
        self.url = reverse('register_freelancer')

    def test_register_freelancer_success(self):
        data = {
            'username': 'freelancer123',
            'email': 'freelancer123@example.com',
            'password1': 'StrongPassword2024!@',
            'password2': 'StrongPassword2024!@',
            'citizen_number': '987654321',
            'phone_number': '5551234567',
            'profile_photo': None,  # Optional
            'experience_level': 'junior',
            'description': 'Experienced freelancer in IT',
            'portfolio_link': 'https://example.com/portfolio',
            'project_evidence': None,  # Optional
        }

        response = self.client.post(self.url, data)

        self.assertRedirects(response, reverse('freelancer'))  # Check if redirected to profile editing
        self.assertTrue(User.objects.filter(username='freelancer123').exists())
        self.assertTrue(Freelancer_Profile.objects.filter(user__username='freelancer123').exists())

    def test_register_freelancer_invalid_data(self):
        data = {
            'username': 'invalidfreelancer',
            'email': 'invalidfreelancer@example.com',
            'password1': 'differentpassword',
            'password2': 'password123',
            'citizen_number': '987654321',
            'phone_number': 'invalidphone',  # Número de teléfono no válido
            'profile_photo': None,
            'experience_level': 'junior',
            'description': 'Invalid freelancer',
            'portfolio_link': '',
            'project_evidence': None,
        }

        response = self.client.post(self.url, data)

        # Verificamos que el formulario no haya pasado y que haya errores
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'password2', 'Las contraseñas no coinciden.')
        self.assertFormError(response, 'user_form', 'phone_number', 'Número de teléfono no válido')  # Asumiendo que este es el mensaje de error para el teléfono

    def tearDown(self):
        User.objects.filter(username='freelancer123').delete()
        Freelancer_Profile.objects.filter(user__username='freelancer123').delete()
