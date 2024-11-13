import os
import sys
import django
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  # Para configurar el WebDriver automáticamente

# Configura Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Flexical.settings")
django.setup()

def before_all(context):
    """
    Este método se ejecuta antes de todas las pruebas. Inicializa el navegador.
    """
    # Inicializa el navegador con configuración automática
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    context.driver.maximize_window()  # Maximiza la ventana del navegador
    
    # Configura la URL del servidor Django local
    context.live_server_url = "http://localhost:8000"  # Establece la URL del servidor local

    # Abre la página de login directamente
    login_url = f"{context.live_server_url}/loginUsers"  # Ajusta la URL según tu configuración
    context.driver.get(login_url)

def after_scenario(context, scenario):
    """
    Este método se ejecuta después de cada escenario. Limpia el navegador.
    """
    context.driver.delete_all_cookies()  # Elimina las cookies entre escenarios

def after_all(context):
    """
    Este método se ejecuta después de todas las pruebas. Cierra el navegador.
    """
    context.driver.quit()  # Cierra el navegador
