class WeatherForecastError(Exception):
    """Базовый класс ошибко для прогноза погоды."""
    pass

class InvalidCityError(WeatherForecastError):
    """Класс для ошибок связанных с названием города."""
    pass