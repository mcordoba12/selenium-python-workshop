from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse

@given('the user is on the Django freelancer registration page')
def step_given_user_on_registration_page(context):
    # Configuración del WebDriver
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    context.driver.maximize_window()

    # Cargar la página de registro de freelancer
    registration_url = f"{context.live_server_url}{reverse('register_freelancer')}"
    context.driver.get(registration_url)

    # Esperar que los campos necesarios se carguen
    WebDriverWait(context.driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
    WebDriverWait(context.driver, 20).until(EC.presence_of_element_located((By.NAME, 'email')))

@when('the user registers with valid freelancer credentials')
def step_when_user_registers_valid_freelancer(context):
    # Llenar el formulario de registro general
    context.driver.find_element(By.NAME, 'username').send_keys('freelancer123')
    context.driver.find_element(By.NAME, 'email').send_keys('freelancer123@example.com')
    context.driver.find_element(By.NAME, 'password1').send_keys('StrongPassword2024!@')
    context.driver.find_element(By.NAME, 'password2').send_keys('StrongPassword2024!@')
    context.driver.find_element(By.NAME, 'citizen_number').send_keys('987654321')
    context.driver.find_element(By.NAME, 'phone_number').send_keys('5551234567')
    
    # Subir una foto de perfil (opcional)
    #context.driver.find_element(By.NAME, 'profile_photo').send_keys('')

    # Hacer clic en el botón de registro
    context.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Esperar la redirección a la página de edición de perfil
    WebDriverWait(context.driver, 20).until(EC.url_contains('/freelancer'))

@when('the user registers with invalid freelancer credentials')
def step_when_user_registers_invalid_freelancer(context):
    # Llenar el formulario de registro con datos inválidos
    context.driver.find_element(By.NAME, 'username').send_keys('invaliduser')
    context.driver.find_element(By.NAME, 'email').send_keys('invaliduser@example.com')
    context.driver.find_element(By.NAME, 'password1').send_keys('differentpassword')
    context.driver.find_element(By.NAME, 'password2').send_keys('password123')

    # Llenar los demás campos
    context.driver.find_element(By.NAME, 'citizen_number').send_keys('987654321')
    context.driver.find_element(By.NAME, 'phone_number').send_keys('5559876543')

    # Hacer clic en el botón de registro
    context.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Esperar que el mensaje de error sea visible
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-danger')))

@when('the user fills the freelancer profile information')
def step_when_user_fills_profile_information(context):
    # Rellenar la información del perfil
    context.driver.find_element(By.NAME, 'description').send_keys('Experienced freelancer in IT')
    context.driver.find_element(By.NAME, 'portfolio_link').send_keys('https://example.com/portfolio')

    # Subir archivo de prueba si es necesario, o dejarlo vacío si no es obligatorio
    #context.driver.find_element(By.NAME, 'project_evidence').send_keys('')

    # Habilidades predefinidas (suponiendo que son checkboxes)
    context.driver.find_element(By.NAME, 'predefined_skills').send_keys('Desarrollo Web, Programación en Python')

    # Nivel de experiencia
    context.driver.find_element(By.NAME, 'experience_level').send_keys('junior')

    # Hacer clic en el botón para enviar el formulario
    context.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Esperamos que la página se redirija correctamente
    WebDriverWait(context.driver, 20).until(EC.url_contains('/freelancerHome'))

@then('the user should be redirected to the freelancer home page')
def step_then_user_redirected_to_freelancer_home(context):
    WebDriverWait(context.driver, 20).until(EC.url_contains('/freelancerHome'))
    assert '/freelancerHome' in context.driver.current_url

@then('an error message for freelancer registration should be displayed')
def step_then_error_message_for_registration_displayed(context):
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-danger')))
    error_message = context.driver.find_element(By.CSS_SELECTOR, '.alert-danger').text
    print(f"Error message: {error_message}")  # Para depuración, muestra el mensaje de error en la consola
    assert "Passwords don't match" in error_message  # Cambiar el mensaje esperado si es necesario
