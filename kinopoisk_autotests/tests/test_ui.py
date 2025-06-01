import pytest
import allure
from selenium import webdriver
from config.settings import Settings
from config.test_data import TestData
from pages.auth_page import AuthPage


@pytest.fixture(scope="function", params=Settings.BROWSERS)
def browser(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Unsupported browser: {request.param}")

    driver.implicitly_wait(Settings.UI_TIMEOUT)
    yield driver
    driver.quit()


@pytest.mark.ui
class TestKinopoiskUI:
    @allure.title("Verify auth form consistency across browsers")
    def test_auth_form_consistency(self, browser):
        with allure.step("Open auth page"):
            page = AuthPage(browser).open_auth_form()

        with allure.step("Verify form elements"):
            assert page.get_login_placeholder() == "Электронная почта или телефон"
            assert page.get_password_placeholder() == "Пароль"
            assert not page.is_login_button_enabled()

    @allure.title("Verify login button state")
    def test_login_button_state(self, browser):
        page = AuthPage(browser).open_auth_form()

        with allure.step("Check button disabled with empty fields"):
            assert not page.is_login_button_enabled()

        with allure.step("Check button enabled with valid data"):
            page.enter_login(TestData.VALID_EMAIL)
            page.enter_password(TestData.VALID_PASSWORD)
            assert page.is_login_button_enabled()

    @allure.title("Verify validation errors")
    def test_validation_errors(self, browser):
        page = AuthPage(browser).open_auth_form()

        with allure.step("Submit invalid credentials"):
            page.enter_login(TestData.INVALID_EMAIL)
            page.enter_password(TestData.INVALID_PASSWORD)
            page.click_login_button()

        with allure.step("Verify error message"):
            assert "Неверный email или телефон" in page.get_error_message()

    @allure.title("Verify search field visibility")
    def test_search_visibility(self, browser):
        page = AuthPage(browser).open()
        assert page.is_search_field_visible()
