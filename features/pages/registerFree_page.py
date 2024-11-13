from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse
from django.test import LiveServerTestCase

class RegisterFreelancerPageTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()

    def test_register_freelancer(self):
        # Primer paso: Registro general
        self.driver.get(self.live_server_url + reverse('register_freelancer'))

        # Esperar que los campos de registro estén disponibles
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))

        # Llenar el formulario de registro general
        self.driver.find_element(By.NAME, 'username').send_keys('freelancer123')
        self.driver.find_element(By.NAME, 'email').send_keys('freelancer123@example.com')
        self.driver.find_element(By.NAME, 'password1').send_keys('StrongPassword2024!@')
        self.driver.find_element(By.NAME, 'password2').send_keys('StrongPassword2024!@')
        self.driver.find_element(By.NAME, 'citizen_number').send_keys('987654321')
        self.driver.find_element(By.NAME, 'phone_number').send_keys('5551234567')
        
        # Subir una foto de perfil (opcional)
        self.driver.find_element(By.NAME, 'profile_photo').send_keys('')

        # Hacer clic en el botón de registro
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Verificar que se haya redirigido a la página de editar perfil
        WebDriverWait(self.driver, 10).until(EC.url_contains('/freelancer'))
        assert '/freelancer' in self.driver.current_url  # Verificar la URL

        # Segundo paso: Completar perfil del freelancer
        self.driver.find_element(By.NAME, 'description').send_keys('Experienced freelancer in IT')
        self.driver.find_element(By.NAME, 'portfolio_link').send_keys('https://example.com/portfolio')

        # Subir evidencia de proyecto (opcional)
        self.driver.find_element(By.NAME, 'project_evidence').send_keys('')

        # Habilidades
        self.driver.find_element(By.NAME, 'skills').send_keys('Desarrollo Web, Programación en Python')

        # Nivel de experiencia
        self.driver.find_element(By.NAME, 'experience_level').send_keys('junior')

        # Hacer clic en guardar cambios
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Esperar la redirección a la página principal del freelancer
        WebDriverWait(self.driver, 10).until(EC.url_contains('/freelancerHome'))
        assert '/freelancerHome' in self.driver.current_url

    def tearDown(self):
        self.driver.quit()
