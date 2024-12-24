import requests
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from utils.validation import validate_city
from exceptions import InvalidCityError

# https://medium.com/@rekalantar/how-to-build-a-simple-weather-app-in-python-with-openweathermap-api-447a2dd27898
# https://blog.bytescrum.com/how-to-create-a-python-weather-app

class WeatherForecast:
    def __init__(self, city: str):
        self.city = validate_city(city)
        self.api_key = "0cbec79a00bd524d73e94372be27c4ca"
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast?"

    # Отправляем запрос для того, чтобы получить данные о погоде
    def fetch_weather_data(self):
        params = {"q": self.city, "appid": self.api_key, "units": "metric"}
        response = requests.get(self.base_url, params=params)
        if response.status_code == 404:
            raise InvalidCityError(f"City '{self.city}' not found.")
        response.raise_for_status()
        return response.json()

    # обрабатываем данные
    def process_weather_data(self, data):
        daily_data = {}
        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0] # извлекаем дату
            temp = round(entry["main"]["temp"]) # округляем температуру до целого числа
            if date not in daily_data:
                daily_data[date] = []
            daily_data[date].append(temp)

        # считаем максимальную среднюю и минимальную температуру
        # апи присылает нам данные за каждые 3 часа на 5 дней
        daily_summary = []
        for date, temps in daily_data.items():
            daily_summary.append({
                "date": date,
                "min": min(temps),
                "max": max(temps),
                "avg": round(sum(temps) / len(temps))
            })
        return daily_summary

    def display_forecast(self):
        data = self.fetch_weather_data()
        processed_data = self.process_weather_data(data)

        # https://pypi.org/project/prettytable/
        # с помощью PrettyTable будем выводить красивую таблицу в консоль
        table = PrettyTable()
        table.field_names = ["Date", "Min Temp (°C)", "Max Temp (°C)", "Avg Temp (°C)"]

        # для каждой температуры устанавливаем цвет
        for entry in processed_data:
            _, bg_min = self.get_color(entry["min"])
            _, bg_max = self.get_color(entry["max"])
            _, bg_avg = self.get_color(entry["avg"])

            # добавляем в таблицу данные: дата без изменения стилелй, а температура с установленным задним фоном и центрирована
            table.add_row([
                entry["date"],
                f"{bg_min}{str(entry['min']).center(len(table.field_names[1]))}{Style.RESET_ALL}",
                f"{bg_max}{str(entry['max']).center(len(table.field_names[2]))}{Style.RESET_ALL}",
                f"{bg_avg}{str(entry['avg']).center(len(table.field_names[3]))}{Style.RESET_ALL}"
            ])

        print(table)


    # https://www.geeksforgeeks.org/introduction-to-python-colorama/
    # устанавливаем цвет ячейки в зависимости от температуры
    @staticmethod
    def get_color(temp):
        if temp < -10:
            return Fore.LIGHTBLUE_EX, Back.LIGHTBLUE_EX
        elif -10 <= temp < 0:
            return Fore.LIGHTCYAN_EX, Back.CYAN
        elif 0 <= temp < 10:
            return Fore.LIGHTGREEN_EX, Back.GREEN
        elif 10 <= temp < 20:
            return Fore.LIGHTYELLOW_EX, Back.YELLOW
        elif 20 <= temp < 30:
            return Fore.LIGHTMAGENTA_EX, Back.MAGENTA
        elif temp >= 30:
            return Fore.LIGHTRED_EX, Back.RED