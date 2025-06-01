from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional
from .base_page import BasePage
from config.settings import Settings

class AuthPage(BasePage):
    """Page Object для страницы авторизации Кинопоиска."""

    # Локаторы элементов
    LOGIN_FIELD = (By.NAME, "login")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Войти')]")
    ERROR_MESSAGE = (By.CLASS_NAME, "auth-form-error")
    SEARCH_FIELD = (By.NAME, "kp_query")
    LOGO = (By.CSS_SELECTOR, "div.header-logo")  # Локатор логотипа

    def open_auth_form(self) -> 'AuthPage':
        """Открывает страницу и ожидает загрузки формы авторизации."""
        self.open()
        self.wait_for_visibility(self.LOGO)
        self.wait_for_clickable(self.LOGIN_FIELD)
        return self

    def enter_login(self, email: str) -> 'AuthPage':
        """Вводит email/телефон в поле логина."""
        field = self.wait_for_visibility(self.LOGIN_FIELD)
        field.clear()
        field.send_keys(email)
        return self

    def enter_password(self, password: str) -> 'AuthPage':
        """Вводит пароль в соответствующее поле."""
        field = self.wait_for_visibility(self.PASSWORD_FIELD)
        field.clear()
        field.send_keys(password)
        return self

    def click_login_button(self) -> 'AuthPage':
        """Кликает по кнопке входа."""
        self.wait_for_clickable(self.LOGIN_BUTTON).click()
        return self

    def get_error_message(self) -> Optional[str]:
        """Получает текст сообщения об ошибке."""
        try:
            return self.wait_for_visibility(self.ERROR_MESSAGE, timeout=3).text
        except:
            return None

    def is_login_button_enabled(self) -> bool:
        """Проверяет, активна ли кнопка входа."""
        return self.wait_for_visibility(self.LOGIN_BUTTON).is_enabled()

    def get_login_placeholder(self) -> str:
        """Получает текст плейсхолдера поля логина."""
        return self.wait_for_visibility(self.LOGIN_FIELD).get_attribute("placeholder")

    def get_password_placeholder(self) -> str:
        """Получает текст плейсхолдера поля пароля."""
        return self.wait_for_visibility(self.PASSWORD_FIELD).get_attribute("placeholder")

    def is_search_field_visible(self) -> bool:
        """Проверяет видимость поля поиска."""
        try:
            return self.wait_for_visibility(self.SEARCH_FIELD, timeout=3).is_displayed()
        except:
            return False

    def login(self, email: str, password: str) -> None:
        """Выполняет полный процесс авторизации."""
        (self.open_auth_form()
         .enter_login(email)
         .enter_password(password)
         .click_login_button())
