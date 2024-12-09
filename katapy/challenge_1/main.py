import requests
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class WeatherService:

    """
    The WeatherService class provides weather data from OpenWeatherMap API.

    Args:
        units (Optional[str]): Units is used to define the temperature metric

    Attributes:
        base_url (str): The base url for the API endpoint.
        units  (Optional[str]): Units is used to define the temperature metric
    
    
    """

    def __init__(self, units: Optional[str] = 'imperial'):
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.units = units

    def _get_by_city(self, city_name: str):

        """
        Get weather data from OpenWeatherMap API.

        Args:
            city_name (str): The city name to retrieve it's weather current data.

        Raises:
            HttpError: The status code and message returned by OpenWeatherMap API.
            RequesteException: Something went wrong.
            ConnectionError: Error during connection.
            Timeout: Timeout error.
            ValueError: Expects an API Key.

        Returns:
            data: Te weather data in the form of dictionary
        
        """

        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("API Key is missing. Please, check your environment variables.")

        url = f"{self.base_url}?q={city_name}&appid={api_key}"

        if isinstance(self.units, str):
            url += f"&units={self.units}"

        try:

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            return data

        except requests.exceptions.HTTPError as error:
            print(f"HTTP Error: {error.response.status_code} = {error.response.reason}")
            raise SystemExit("Could not retrieve data from OpenWeather API")
        except requests.exceptions.RequestException as error:
            print(f"Request Exception: {error.response.reason}")
            raise SystemExit("Something went wrong")
        except requests.exceptions.ConnectionError as error:
            print(f"Connection Error: {error.response.reason}")
            raise SystemExit("Error during connection")
        except requests.exceptions.Timeout as error:
            print(f"Timeout Error: {error.response.reason}")
            raise SystemExit("A timeout error occurred")
        

    def display_weather(self, city:  str):

        """
        Display a weather report given a city name. The report will contain: City, Temperature, Feels Like, Humidity and Weather description.

        Args:
            city (str): The city name to retrieve it's weather current data.
        Returns:
            None


        """

        data = self._get_by_city(city)
        print(f""" Weather Report \n City: {city} \n Temperature ({'ºC' if self.units=='metric' else 'ºF' if self.units=='imperial' else 'ºK'}): {data['main']['temp']} \n Feels Like: {data['main']['feels_like']} \n Humidity: {data['main']['humidity']} \n Description: {data['weather'][0]['description']}""")



if __name__ == "__main__":

    while True:
        city = input("Enter the city name: ")
        units = input("Enter the unit system(metric/imperial/standard): \n") or "imperial"
        weather = WeatherService(units=units)
        weather.display_weather(city)
        leave = input("\nWould you like to continue? (y/n): ") or "y"
        if leave.lower() == 'n':
            break