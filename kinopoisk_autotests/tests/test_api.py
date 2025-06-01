import pytest
import allure
import requests
from config.settings import Settings
from config.test_data import TestData


@pytest.mark.api
class TestKinopoiskAPI:
    @pytest.fixture
    def api_client(self):
        session = requests.Session()
        session.headers.update({
            "X-API-KEY": Settings.API_KEY,
            "Content-Type": "application/json"
        })
        yield session
        session.close()

    @allure.title("Search movie by exact title")
    def test_search_exact_title(self, api_client):
        url = f"{Settings.API_URL}{Settings.API_VERSION}/movie/search"
        params = {"query": TestData.MOVIE_TITLE_EXACT}

        response = api_client.get(url, params=params)
        assert response.status_code == 200
        assert any(movie["name"] == TestData.MOVIE_TITLE_EXACT
                   for movie in response.json().get("docs", []))

    @allure.title("Search movie by partial title")
    def test_search_partial_title(self, api_client):
        url = f"{Settings.API_URL}{Settings.API_VERSION}/movie/search"
        params = {"query": TestData.MOVIE_TITLE_PARTIAL}

        response = api_client.get(url, params=params)
        assert response.status_code == 200
        assert any(TestData.MOVIE_TITLE_PARTIAL in movie["name"]
                   for movie in response.json().get("docs", []))

    @allure.title("Search movie with year filter")
    def test_search_with_year_filter(self, api_client):
        url = f"{Settings.API_URL}{Settings.API_VERSION}/movie/search"
        params = {
            "query": TestData.MOVIE_TITLE_YEAR_FILTER,
            "year": TestData.MOVIE_YEAR
        }

        response = api_client.get(url, params=params)
        assert response.status_code == 200
        assert any(movie["year"] == TestData.MOVIE_YEAR
                   for movie in response.json().get("docs", []))

    @allure.title("Search non-existent movie")
    def test_search_non_existent_movie(self, api_client):
        url = f"{Settings.API_URL}{Settings.API_VERSION}/movie/search"
        params = {"query": TestData.NON_EXISTENT_MOVIE}

        response = api_client.get(url, params=params)
        assert response.status_code == 200
        assert len(response.json().get("docs", [])) == 0

    @allure.title("Search with invalid year parameter")
    def test_search_with_invalid_year(self, api_client):
        """Тест проверяет, что API возвращает корректные результаты даже при некорректном параметре года"""
        url = f"{Settings.API_URL}{Settings.API_VERSION}/movie/search"
        params = {
            "query": TestData.MOVIE_TITLE_YEAR_FILTER,
            "year": TestData.INVALID_YEAR
        }

        with allure.step("Отправляем запрос с некорректным годом"):
            response = api_client.get(url, params=params)
            assert response.status_code == 200, "API должен возвращать 200 даже при некорректных параметрах"

        with allure.step("Проверяем структуру ответа"):
            data = response.json()
            assert "docs" in data, "В ответе должно быть поле docs"

            # Проверяем, что в результатах нет фильмов с указанным некорректным годом
            if len(data["docs"]) > 0:
                for movie in data["docs"]:
                    assert "year" not in movie or movie["year"] != TestData.INVALID_YEAR, \
                        f"Найден фильм с некорректным годом: {movie.get('name')}"

