from unittest.mock import Mock, patch

import pytest
import requests

from src.APIadapter import APIAdapter


@pytest.fixture
def api() -> APIAdapter:
    """Фикстура для APIAdapter"""
    return APIAdapter()


def test_init(api: APIAdapter) -> None:
    """Тест инициализации"""
    assert api.aeroplanes == []


def test_connect_success(api: APIAdapter) -> None:
    """Тест успешного подключения"""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 200

    # Патчим метод get у Session, а не приватный атрибут
    with patch("requests.Session.get", return_value=mock_response) as mock_get:
        result = api._connect("https://test.com")

        mock_get.assert_called_once()
        assert result == mock_response


def test_connect_failure(api: APIAdapter) -> None:
    """Тест ошибки подключения"""
    with patch("requests.Session.get", side_effect=Exception("Error")):
        result = api._connect("https://test.com")
        assert result is None


def test_connect_with_params(api: APIAdapter) -> None:
    """Тест подключения с параметрами"""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 200
    params = {"q": "test"}

    with patch("requests.Session.get", return_value=mock_response) as mock_get:
        result = api._connect("https://test.com", params)

        mock_get.assert_called_once_with("https://test.com", params=params, timeout=10)
        assert result == mock_response


def test_connect_bad_status(api: APIAdapter) -> None:
    """Тест плохого статус-кода"""
    mock_response = Mock(spec=requests.Response)
    mock_response.status_code = 404

    with patch("requests.Session.get", return_value=mock_response):
        with patch("builtins.print") as mock_print:
            result = api._connect("https://test.com")

            mock_print.assert_called_with("Ошибка: статус 404")
            assert result is None


def test_get_coordinates_default(api: APIAdapter) -> None:
    """Тест координат по умолчанию"""
    # Патчим метод _connect, который используется внутри
    with patch.object(api, "_connect", return_value=None):
        coords = api.get_coordinates("Russia")

        assert coords == {"min_lat": 40.0, "max_lat": 50.0, "min_lon": 30.0, "max_lon": 40.0}


def test_get_coordinates_success(api: APIAdapter) -> None:
    """Тест успешного получения координат"""
    mock_response = Mock()
    mock_response.json.return_value = [{"boundingbox": ["55.0", "65.0", "30.0", "40.0"]}]

    with patch.object(api, "_connect", return_value=mock_response):
        coords = api.get_coordinates("Russia")

        assert coords == {"min_lat": 55.0, "max_lat": 65.0, "min_lon": 30.0, "max_lon": 40.0}


def test_get_coordinates_api_error(api: APIAdapter) -> None:
    """Тест ошибки API при получении координат"""
    with patch.object(api, "_connect", return_value=None):
        coords = api.get_coordinates("InvalidCountry")

        # Должны получить координаты по умолчанию
        assert coords == {"min_lat": 40.0, "max_lat": 50.0, "min_lon": 30.0, "max_lon": 40.0}


def test_get_aeroplanes_success(api: APIAdapter) -> None:
    """Тест успешного получения самолетов"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "states": [["abc123", "AFL101", "Russia", 123, 123, 55.5, 37.5, 10000, False, 250, 45, 0, None, 10500]]
    }
    coords = {"min_lat": 40.0, "max_lat": 50.0, "min_lon": 30.0, "max_lon": 40.0}

    with patch.object(api, "_connect", return_value=mock_response):
        api.get_aeroplanes(coords)

        # Проверяем через публичный геттер
        assert len(api.aeroplanes) == 1
        assert api.aeroplanes[0][1] == "AFL101"


def test_get_aeroplanes_empty(api: APIAdapter) -> None:
    """Тест получения пустого списка самолетов"""
    mock_response = Mock()
    mock_response.json.return_value = {"states": []}
    coords = {"min_lat": 40.0, "max_lat": 50.0, "min_lon": 30.0, "max_lon": 40.0}

    with patch.object(api, "_connect", return_value=mock_response):
        api.get_aeroplanes(coords)

        assert api.aeroplanes == []


def test_get_aeroplanes_no_connection(api: APIAdapter) -> None:
    """Тест ошибки подключения при получении самолетов"""
    coords = {"min_lat": 40.0, "max_lat": 50.0, "min_lon": 30.0, "max_lon": 40.0}

    with patch.object(api, "_connect", return_value=None):
        api.get_aeroplanes(coords)

        assert api.aeroplanes == []


def test_property_aeroplanes(api: APIAdapter) -> None:
    """Тест геттера aeroplanes"""
    # Используем публичный метод для установки значения
    mock_response = Mock()
    mock_response.json.return_value = {
        "states": [["test_id", "TEST", "Country", 0, 0, 0, 0, 0, False, 0, 0, 0, None, 0]]
    }
    coords = {"min_lat": 40.0, "max_lat": 50.0, "min_lon": 30.0, "max_lon": 40.0}

    with patch.object(api, "_connect", return_value=mock_response):
        api.get_aeroplanes(coords)

        assert isinstance(api.aeroplanes, list)
        assert len(api.aeroplanes) == 1
