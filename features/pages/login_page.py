from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class LoginPage:
    USERNAME_FIELD = (By.NAME, 'username')  # Ajusta el selector si es necesario
    PASSWORD_FIELD = (By.NAME, 'password')  # Ajusta el selector si es necesario
    LOGIN_BUTTON = (By.ID, 'loginbtn')      # Ajusta el selector si es necesario
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-warning")  # Selector del mensaje de error

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password, server_url):
        self.driver.get(f"{server_url}/loginUsers")  # Ajusta la URL de login según tu sistema
        self.enter_text(self.USERNAME_FIELD, username)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    def enter_text(self, element, text):
        self.driver.find_element(*element).send_keys(text)

    def click(self, element):
        self.driver.find_element(*element).click()

    def get_error_message(self):
        # Espera hasta que el mensaje de error sea visible
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return self.driver.find_element(*self.ERROR_MESSAGE).text
