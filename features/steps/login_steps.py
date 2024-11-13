from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_test.features.pages.login_page import LoginPage
from django.urls import reverse

@given('the user is on the Django login page')
def step_given_user_on_login_page(context):
    # Configuración automática del WebDriver
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    context.driver.implicitly_wait(10)  # Espera implícita para encontrar los elementos
    context.driver.maximize_window()

    # Construye la URL de login en Django
    login_url = f"{context.live_server_url}{reverse('loginUsers')}"
    context.driver.get(login_url)  # Navega a la URL de login
    
    # Esperamos hasta que los campos 'username' y 'password' estén disponibles
    WebDriverWait(context.driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
    WebDriverWait(context.driver, 20).until(EC.presence_of_element_located((By.NAME, 'password')))
    
    

@when('the user logs in with valid credentials')
def step_when_user_logs_in_valid(context):
    # Esperamos que los campos estén disponibles antes de enviar los datos
    username_input = context.driver.find_element(By.NAME, "username")
    password_input = context.driver.find_element(By.NAME, "password")
    
    # Enviar las credenciales válidas
    username_input.send_keys("angela")  # Cambia por un usuario válido de prueba
    password_input.send_keys("StrongPassword2024!@")  # Cambia por la contraseña válida
    
    # Enviar el formulario
    password_input.send_keys(Keys.RETURN)
    
    # Esperamos hasta que la URL contenga 'clientHome' después de la redirección
    WebDriverWait(context.driver, 20).until(EC.url_contains("/clientHome"))
    
    # Verificar que la página se redirige correctamente a la página de cliente
    assert "/clientHome" in context.driver.current_url

@when('the user logs in with invalid credentials')
def step_when_user_logs_in_invalid(context):
    # Esperar que los campos estén disponibles antes de enviar los datos
    username_input = context.driver.find_element(By.NAME, "username")
    password_input = context.driver.find_element(By.NAME, "password")
    
    username_input.send_keys("invalid_user")
    password_input.send_keys("invalid_password")
    password_input.send_keys(Keys.RETURN)
    
    # Esperar que el mensaje de error sea visible
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-warning")))

    error_message = context.driver.find_element(By.CSS_SELECTOR, ".alert-warning").text
    print("Error message:", error_message)  # Para debugging
    
    # Verificar que el mensaje de error es correcto
    assert "por favor verifica los datos ingresados." in error_message.strip().lower()

    # Verificar que la URL sigue siendo la de inicio de sesión
    assert "/login" in context.driver.current_url

# Then step: Verifica que el usuario es redirigido al dashboard
@then(u'the user should be redirected to the dashboard page')
def step_impl(context):
    # Esperar que la URL contenga la ruta del dashboard
    WebDriverWait(context.driver, 20).until(EC.url_contains("/clientHome"))
    
    # Asegurarse de que la URL contiene '/clientHome', lo que indica que el usuario ha sido redirigido correctamente
    assert "/clientHome" in context.driver.current_url


@then(u'an error message should be displayed')
def step_impl(context):
    # Esperar a que el mensaje de error sea visible
    WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-warning")))

    # Obtener el texto del mensaje de error
    error_message = context.driver.find_element(By.CSS_SELECTOR, ".alert-warning").text
    print("Error message:", error_message)  # Para depuración, muestra el mensaje de error en la consola
    
    # Verificar que el mensaje de error contiene el texto esperado
    assert "por favor verifica los datos ingresados." in error_message.strip().lower()

    # Asegurarse de que la URL siga siendo la de inicio de sesión
    assert "/login" in context.driver.current_url

