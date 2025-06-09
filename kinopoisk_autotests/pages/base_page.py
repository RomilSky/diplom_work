from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import Settings


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Settings.UI_TIMEOUT)

    def wait_for_visibility(self, locator):
        """Ожидает видимости элемента на странице"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        """Ожидает, когда элемент станет кликабельным"""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def open(self):
        """Открывает базовый URL"""
        self.driver.get(Settings.BASE_URL)
        return self

    def is_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def is_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    # Новый метод для ожидания видимости с явным таймаутом
    def wait_for_visibility(self, locator, timeout=Settings.UI_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    # Новый метод для ожидания кликабельности с явным таймаутом
    def wait_for_clickable(self, locator, timeout=Settings.UI_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

