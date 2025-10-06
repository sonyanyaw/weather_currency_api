import pytest
import httpx
from src.services.services import get_weather, convert_currency
from unittest.mock import patch
import os

# Тесты для функции get_weather

def weather_success_handler(request: httpx.Request) -> httpx.Response:
    """Обработчик успешного ответа погодного API"""
    if "meteosource.com" in request.url.host:
        return httpx.Response(200, json={
            "current": {
                "temperature": 18,
                "summary": "Rainy"
            }
        })
    return httpx.Response(404, json={"error": "Not found"})

def weather_error_handler(request: httpx.Request) -> httpx.Response:
    """Обработчик ошибки от погодного API"""
    if "meteosource.com" in request.url.host:
        return httpx.Response(500, json={
            "error": "Internal server error"
        })
    return httpx.Response(404, json={"error": "Not found"})

def weather_invalid_data_handler(request: httpx.Request) -> httpx.Response:
    """Обработчик с некорректными данными"""
    if "meteosource.com" in request.url.host:
        return httpx.Response(200, json={
            "invalid": "structure"
        })
    return httpx.Response(404, json={"error": "Not found"})

def weather_timeout_handler(request: httpx.Request) -> httpx.Response:
    """Обработчик имитации таймаута"""
    raise httpx.TimeoutException("Request timed out")

@pytest.mark.asyncio
async def test_get_weather_success():
    """Тест успешного получения погоды"""
    transport = httpx.MockTransport(weather_success_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        result = await get_weather("berlin", client=test_client)
    
    assert result["city"] == "berlin"
    assert result["temperature_c"] == 18
    assert result["description"] == "Rainy"

@pytest.mark.asyncio
async def test_get_weather_different_city():
    """Тест получения погоды для другого города"""
    transport = httpx.MockTransport(weather_success_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        result = await get_weather("paris", client=test_client)
    
    assert result["city"] == "paris"
    assert result["temperature_c"] == 18

@pytest.mark.asyncio
async def test_get_weather_api_error():
    """Тест обработки ошибки API"""
    transport = httpx.MockTransport(weather_error_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        with pytest.raises(Exception):  # Ожидаем, что функция выбросит исключение
            await get_weather("berlin", client=test_client)

@pytest.mark.asyncio
async def test_get_weather_invalid_data():
    """Тест обработки некорректных данных от API"""
    transport = httpx.MockTransport(weather_invalid_data_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        with pytest.raises(KeyError):  # Ожидаем KeyError при отсутствии нужных полей
            await get_weather("berlin", client=test_client)

@pytest.mark.asyncio
async def test_get_weather_timeout():
    """Тест обработки таймаута"""
    transport = httpx.MockTransport(weather_timeout_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        with pytest.raises(httpx.TimeoutException):
            await get_weather("berlin", client=test_client)

@pytest.mark.asyncio
async def test_get_weather_without_client():
    """Тест что функция работает без переданного клиента"""
    # Мокаем только API ключ, так как реальный запрос не должен уходить
    with patch.dict(os.environ, {'WEATHER_API_KEY': 'test_key'}):
        with patch('src.services.services.httpx.AsyncClient') as mock_client:
            mock_response = httpx.Response(200, json={
                "current": {
                    "temperature": 20,
                    "summary": "Sunny"
                }
            })
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await get_weather("london")
            
            assert result["city"] == "london"
            assert result["temperature_c"] == 20

# Тесты для функции convert_currency

def currency_success_handler(request: httpx.Request) -> httpx.Response:
    """Обработчик успешного ответа валютного API"""
    if "exchangerate-api.com" in request.url.host:
        return httpx.Response(200, json={
            "conversion_rates": {
                "USD": 1.0,
                "EUR": 0.85,
                "GBP": 0.75,
                "JPY": 110.0
            }
        })
    return httpx.Response(404, json={"error": "Not found"})

def currency_error_handler(request: httpx.Request) -> httpx.Response:
    """Обработчик ошибки от валютного API"""
    if "exchangerate-api.com" in request.url.host:
        return httpx.Response(403, json={
            "error": "Invalid API key"
        })
    return httpx.Response(404, json={"error": "Not found"})

def currency_missing_currency_handler(request: httpx.Request) -> httpx.Response:
    """Обработчик когда запрашиваемая валюта отсутствует"""
    if "exchangerate-api.com" in request.url.host:
        return httpx.Response(200, json={
            "conversion_rates": {
                "USD": 1.0,
                "EUR": 0.85
                # Нет GBP, JPY и других
            }
        })
    return httpx.Response(404, json={"error": "Not found"})

@pytest.mark.asyncio
async def test_convert_currency_success():
    """Тест успешного конвертирования валют"""
    transport = httpx.MockTransport(currency_success_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        # USD to EUR
        result = await convert_currency("USD", "EUR", 100.0, client=test_client)
        assert result == 85.0  # 100 * 0.85
        
        # USD to GBP
        result = await convert_currency("USD", "GBP", 100.0, client=test_client)
        assert result == 75.0  # 100 * 0.75
        
        # USD to JPY
        result = await convert_currency("USD", "JPY", 1.0, client=test_client)
        assert result == 110.0  # 1 * 110

@pytest.mark.asyncio
async def test_convert_currency_different_amounts():
    """Тест конвертации разных сумм"""
    transport = httpx.MockTransport(currency_success_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        # Маленькая сумма
        result = await convert_currency("USD", "EUR", 1.0, client=test_client)
        assert result == 0.85
        
        # Большая сумма
        result = await convert_currency("USD", "EUR", 1000.0, client=test_client)
        assert result == 850.0
        
        # Дробная сумма
        result = await convert_currency("USD", "EUR", 123.45, client=test_client)
        assert result == 104.9325  # 123.45 * 0.85

@pytest.mark.asyncio
async def test_convert_currency_api_error():
    """Тест обработки ошибки API при конвертации"""
    transport = httpx.MockTransport(currency_error_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        with pytest.raises(Exception):
            await convert_currency("USD", "EUR", 100.0, client=test_client)

@pytest.mark.asyncio
async def test_convert_currency_missing_currency():
    """Тест когда запрашиваемая валюта отсутствует в ответе"""
    transport = httpx.MockTransport(currency_missing_currency_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        with pytest.raises(KeyError):  # Ожидаем KeyError при отсутствии валюты
            await convert_currency("USD", "GBP", 100.0, client=test_client)

@pytest.mark.asyncio
async def test_convert_currency_same_currency():
    """Тест конвертации одинаковых валют (должен вернуть ту же сумму)"""
    transport = httpx.MockTransport(currency_success_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        result = await convert_currency("USD", "USD", 100.0, client=test_client)
        assert result == 100.0  # 100 * 1.0

# Интеграционные тесты

@pytest.mark.asyncio
async def test_multiple_requests_same_client():
    """Тест нескольких запросов с одним клиентом"""
    def combined_handler(request: httpx.Request) -> httpx.Response:
        if "meteosource.com" in request.url.host:
            return httpx.Response(200, json={
                "current": {
                    "temperature": 22,
                    "summary": "Sunny"
                }
            })
        elif "exchangerate-api.com" in request.url.host:
            return httpx.Response(200, json={
                "conversion_rates": {
                    "USD": 1.0,
                    "EUR": 0.9
                }
            })
        return httpx.Response(404, json={"error": "Not found"})
    
    transport = httpx.MockTransport(combined_handler)
    async with httpx.AsyncClient(transport=transport) as test_client:
        # Тестируем обе функции с одним клиентом
        weather_result = await get_weather("madrid", client=test_client)
        currency_result = await convert_currency("USD", "EUR", 50.0, client=test_client)
        
        assert weather_result["city"] == "madrid"
        assert weather_result["temperature_c"] == 22
        assert currency_result == 45.0  # 50 * 0.9