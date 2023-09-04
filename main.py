import asyncio
import time
from aiohttp import ClientSession
import re

# 1.Создать класс для хранения параметров погоды
class WeatherinSity:
    def __init__(self, city, temp, humidity, pressure, wind):
        self.city = city
        self.temp = temp
        self.humidity = humidity
        self.pressure = pressure
        self.wind = wind

# 2.Открыть файл cities.txt с названием городов, считать города и загрузить в программу список городов
with open('cities.txt', 'r', encoding='utf-8') as file:
    cities = []
    for row in file:
        city = re.search(r'\) [A-Za-z ]+', row)
        if city:
            cities.append(city.group()[2:].strip())

# 3.По считанным городам параллельно(асинхронно) запросить на openweatherAPI информацию о погоде
async def get_weather(city):
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2427d0de0c45562b3f6dcccddd2b3955', 'units': 'metric'}

        async with session.get(url=url, params=params) as response:
            w_js = await response.json()
            params = (city, w_js['main']['temp'], w_js['main']['humidity'], w_js['main']['pressure'], w_js['wind']['speed'])
            return WeatherinSity(*params)


async def main(cities):
    tasks = []
    for city in cities:
        tasks.append(asyncio.create_task(get_weather(city)))

    results = await asyncio.gather(*tasks)

    for result in results:
        print(f'city: {result.city}, temp: {result.temp} C, humidity: {result.humidity} %, pressure: {result.pressure} mmHg, wind: {result.wind} m/s')


asyncio.run(main(cities))