import os
import requests
from dotenv import load_dotenv


class StockData:

    def __init__(self):
        self.base_url: str = "https://www.alphavantage.co/query"

    def get_data(self, stock: str):

        try:

            FUNCTION = "TIME_SERIES_DAILY"

            apikey = os.getenv("ALPHA_VANTAGE_API_KEY")
            if not apikey:
                print("No API Key encountered")
                SystemExit("API KEY not found.")

            url = f"{self.base_url}?function={FUNCTION}&symbol={stock}&apikey={apikey}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            return data
        
        except requests.exceptions.HTTPError as error:
            print(f"HTTP Error: {error.response.status_code} - {error.response.reason}")
            SystemExit("Error")