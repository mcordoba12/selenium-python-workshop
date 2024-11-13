from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  # Para configurar el WebDriver automáticamente
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin(StaticLiveServerTestCase):
    def setUp(self):
        """
        Método que se ejecuta antes de cada prueba. Aquí se inicializa el navegador.
        """
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))  # Configuración automática del WebDriver
        self.driver.implicitly_wait(10)  # Espera implícita
        self.driver.maximize_window()
        self.login_url = f"{self.live_server_url}{reverse('loginUsers')}"  # Ajuste para utilizar la URL de Django
    
    def tearDown(self):
        """
        Método que se ejecuta después de cada prueba. Cierra el navegador.
        """
        self.driver.quit()

    def test_login_success(self):
        """
        Prueba para verificar que un usuario puede iniciar sesión con credenciales válidas.
        """
        # Ir a la página de inicio de sesión
        self.driver.get(self.login_url)
        
        # Esperar explícitamente hasta que los campos estén disponibles
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, "password")))
        
        # Completar los campos de usuario y contraseña
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        
        username_input.send_keys("angela")  # Cambia por un usuario válido de prueba
        password_input.send_keys("StrongPassword2024!@")  # Cambia por la contraseña válida
        
        # Enviar el formulario
        password_input.send_keys(Keys.RETURN)
        
        # Verificar que la página se redirige correctamente
        time.sleep(2)
        self.assertIn("Bienvenido", self.driver.page_source)

    def test_login_failure(self):
        """
        Prueba para verificar que el login falla con credenciales incorrectas.
        """
        self.driver.get(self.login_url)
        
        # Esperar explícitamente hasta que los campos estén disponibles
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, "password")))
        
        # Intento de inicio de sesión con credenciales incorrectas
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        
        username_input.send_keys("invalid_user")
        password_input.send_keys("invalid_password")
        password_input.send_keys(Keys.RETURN)
        
        # Verificar mensaje de error
        time.sleep(2)
        error_message = self.driver.find_element(By.CSS_SELECTOR, ".alert-warning").text
        self.assertIn("Usuario o contraseña incorrectos", error_message)

