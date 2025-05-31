from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import Settings


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Settings.UI_TIMEOUT)
        self.base_url = Settings.BASE_URL

    def open(self):
        self.driver.get(self.base_url)
        return self

    def is_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def is_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
