from forecast import WeatherForecast

def main():
    city = input("Введите название города на английском: ")
    try:
        forecast = WeatherForecast(city)
        forecast.display_forecast()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()