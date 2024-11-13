from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import unittest

class TestRegisterClientPage(unittest.TestCase):

    def setUp(self):
        # Inicia el driver de Chrome
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()

        # Dirige al formulario de registro de cliente
        self.driver.get("http://localhost:8000/registerClient/")  # Cambia la URL si es necesario

    def test_register_client_page_loads(self):
        # Verifica que la página se haya cargado correctamente y contenga el título adecuado
        self.assertIn("Cliente Registro", self.driver.title)  # Ajusta el título de la página si es necesario
        self.assertTrue(self.driver.find_element(By.NAME, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'email').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'company_nit').is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, 'company_name').is_displayed())

    def test_register_client_submit_form_valid_data(self):
        # Completar los campos con datos válidos
        self.driver.find_element(By.NAME, 'username').send_keys('client_test')
        self.driver.find_element(By.NAME, 'email').send_keys('client_test@example.com')
        self.driver.find_element(By.NAME, 'password1').send_keys('StrongPassword2024!@')
        self.driver.find_element(By.NAME, 'password2').send_keys('StrongPassword2024!@')
        self.driver.find_element(By.NAME, 'company_nit').send_keys('123456789')
        self.driver.find_element(By.NAME, 'company_name').send_keys('Test Client Company')
        self.driver.find_element(By.NAME, 'business_type').send_keys('IT')

        # Seleccionar país, ciudad y vertical de negocio
        self.driver.find_element(By.NAME, 'country').send_keys('1')  # Asumiendo '1' es un ID válido de país
        self.driver.find_element(By.NAME, 'business_vertical').send_keys('1')  # Asumiendo '1' es un ID válido de vertical
        self.driver.find_element(By.NAME, 'city').send_keys('1')  # Asumiendo '1' es un ID válido de ciudad
        self.driver.find_element(By.NAME, 'address').send_keys('123 Business St')
        self.driver.find_element(By.NAME, 'phone_number').send_keys('5551234567')
        self.driver.find_element(By.NAME, 'legal_representative').send_keys('Legal Rep')
        self.driver.find_element(By.NAME, 'client_description').send_keys('Client description here.')

        # Enviar el formulario
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Esperar que la página redirija al cliente home
        success_message = self.driver.find_element(By.CSS_SELECTOR, ".success-message")  # Ajusta el selector si es necesario
        self.assertTrue(success_message.is_displayed())  # Verifica que el mensaje de éxito esté presente

    def test_register_client_submit_form_invalid_data(self):
        # Completar los campos con datos inválidos
        self.driver.find_element(By.NAME, 'username').send_keys('invalid_client')
        self.driver.find_element(By.NAME, 'email').send_keys('invalidemail')  # Correo inválido
        self.driver.find_element(By.NAME, 'password1').send_keys('short')  # Contraseña corta
        self.driver.find_element(By.NAME, 'password2').send_keys('short')
        
        # Seleccionar país, ciudad y vertical de negocio
        self.driver.find_element(By.NAME, 'country').send_keys('1')  # Asumiendo '1' es un ID válido de país
        self.driver.find_element(By.NAME, 'business_vertical').send_keys('1')  # Asumiendo '1' es un ID válido de vertical
        self.driver.find_element(By.NAME, 'city').send_keys('1')  # Asumiendo '1' es un ID válido de ciudad
        self.driver.find_element(By.NAME, 'address').send_keys('Invalid Address')
        self.driver.find_element(By.NAME, 'phone_number').send_keys('5559876543')
        self.driver.find_element(By.NAME, 'legal_representative').send_keys('Invalid Rep')

        # Enviar el formulario
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Esperar que el mensaje de error sea visible
        error_message = self.driver.find_element(By.CSS_SELECTOR, '.alert-danger')
        self.assertTrue(error_message.is_displayed())  # Verifica que el mensaje de error esté presente

    def tearDown(self):
        # Cierra el navegador después de la prueba
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
