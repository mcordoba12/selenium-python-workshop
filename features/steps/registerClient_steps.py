from behave import given, when, then
from django.forms import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse

@given('the user is on the Django registration page')
def step_given_user_on_registration_page(context):
    # Configuración automática del WebDriver
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    context.driver.implicitly_wait(10)
    context.driver.maximize_window()

    # Construir la URL de registro
    registration_url = f"{context.live_server_url}{reverse('register_client')}"
    context.driver.get(registration_url)

    # Esperar a que los campos estén disponibles
    WebDriverWait(context.driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
    WebDriverWait(context.driver, 20).until(EC.presence_of_element_located((By.NAME, 'email')))

@when('the user registers with valid credentials')
def step_when_user_registers_valid(context):
    # Completar los campos del formulario con datos válidos
    context.driver.find_element(By.NAME, 'username').send_keys('client2')
    context.driver.find_element(By.NAME, 'email').send_keys('client2@example.com')
    context.driver.find_element(By.NAME, 'password1').send_keys('StrongPassword2024!@')
    context.driver.find_element(By.NAME, 'password2').send_keys('StrongPassword2024!@')
    context.driver.find_element(By.NAME, 'company_nit').send_keys('666')
    context.driver.find_element(By.NAME, 'company_name').send_keys('Valid Company')
    context.driver.find_element(By.NAME, 'business_type').send_keys('IT')

    # Completar los campos de selección y envío del formulario
    context.driver.find_element(By.NAME, 'country').send_keys('Country Name')
    context.driver.find_element(By.NAME, 'business_vertical').send_keys('Software')
    context.driver.find_element(By.NAME, 'city').send_keys('City Name')
    context.driver.find_element(By.NAME, 'address').send_keys('1234 Business St')
    context.driver.find_element(By.NAME, 'phone_number').send_keys('5551234567')
    context.driver.find_element(By.NAME, 'legal_representative').send_keys('John Doe')
    

    # Enviar el formulario
    context.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Esperar la redirección a la página de cliente
    WebDriverWait(context.driver, 20).until(EC.url_contains('/clientHome'))

@when('the user registers with invalid credentials')
def step_when_user_registers_invalid(context):
    # Completar los campos con los mismos datos inválidos que en el test de Django (contraseñas que no coinciden)
    context.driver.find_element(By.NAME, 'username').send_keys('invalidclient')
    context.driver.find_element(By.NAME, 'email').send_keys('invalidclient@example.com')
    context.driver.find_element(By.NAME, 'password1').send_keys('password123')
    context.driver.find_element(By.NAME, 'password2').send_keys('differentpassword')
    context.driver.find_element(By.NAME, 'company_nit').send_keys('987654321')
    context.driver.find_element(By.NAME, 'company_name').send_keys('Invalid Company')
    context.driver.find_element(By.NAME, 'business_type').send_keys('IT')

    context.driver.find_element(By.NAME, 'country').send_keys('Country Name')
    context.driver.find_element(By.NAME, 'business_vertical').send_keys('Software')
    context.driver.find_element(By.NAME, 'city').send_keys('City Name')
    
    # Completar los otros campos
    context.driver.find_element(By.NAME, 'address').send_keys('1')  # Dirección inválida
    context.driver.find_element(By.NAME, 'phone_number').send_keys('5559876543')
    context.driver.find_element(By.NAME, 'legal_representative').send_keys('Jane Doe')

    # Enviar el formulario
    context.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Esperar que el mensaje de error sea visible
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-danger')))



@then('the user should be redirected to the client home page')
def step_then_user_redirected_to_client_home(context):
    # Verificar que la URL contiene '/clientHome'
    WebDriverWait(context.driver, 20).until(EC.url_contains('/clientHome'))
    assert '/clientHome' in context.driver.current_url

@then('an error message for registration should be displayed')
def step_then_error_message_for_registration_displayed(context):
    # Verificar que el mensaje de error sea visible
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-danger')))
    
    # Obtener el mensaje de error
    error_message = context.driver.find_element(By.CSS_SELECTOR, '.alert-danger').text
    print(f"Error message: {error_message}")  # Para depuración, muestra el mensaje de error en la consola
    
    # Verificar que el mensaje de error sea el esperado (en este caso, cuando las contraseñas no coinciden)
    assert "Las contraseñas no coinciden" in error_message  # Cambiar el mensaje esperado si es necesario

