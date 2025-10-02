import requests
import os 
from dotenv import load_dotenv

api_key = os.getenv("WEATHER_API_KEY")
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=Ha Noi"

def fetch_data():
    print("Fetching weather data from Weather API...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("API response received successfully.")
        return response.json()
    except requests.exception.RequestException as e:
        print(f"An error occured: {e}")
        raise

