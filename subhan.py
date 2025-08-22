# import os
# import requests
import httpx
import os
import asyncio

with open(".env") as file:
    for line in file:
        key, value = line.strip().split("=", 1)
        os.environ[key] = value 

# API_KEY = os.environ.get("API_KEY")
# city = "Islamabadq"

# url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()  
#     temperature = data["main"]["temp"]
#     description = data["weather"][0]["description"]
#     print(f"The temperature in {city} is {temperature}°C with {description}.")
# else:
#     print("Failed to get weather data.")
#     print("Status code:", response.status_code)



TOKEN = os.environ.get("EVENTBRITE_TOKEN")


async def get_organization_id():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = "https://www.eventbriteapi.com/v3/users/me/organizations/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json()
        print(data)  # see all data
        # get first organization's id
        org_id = data["organizations"][0]["id"]
        print("Organization ID:", org_id)
        return org_id


asyncio.run(get_organization_id())