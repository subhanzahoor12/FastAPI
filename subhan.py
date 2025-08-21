import os
import requests

with open(".env") as file:
    for line in file:
        
        key, value = line.strip().split("=", 1)
        os.environ[key] = value 

API_KEY = os.environ.get("API_KEY")
city = "Lahore"

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()  
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    print(f"The temperature in {city} is {temperature}°C with {description}.")
else:
    print("Failed to get weather data.")
    print("Status code:", response.status_code)
