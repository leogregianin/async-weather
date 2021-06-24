import os
import asyncio
import json

from httpx import AsyncClient

api_token = os.getenv('API_TOKEN', None)
if not api_token:
    raise Exception('API Token not identify')


async def get_weather(client, city):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_token}"
    response = await client.get(api_url)
    weather = response.json()
    return weather


async def main(loop):
    requests = []
    cities = []
    with open('cities.json', encoding='utf-8') as cities_json:
        cities_load = json.load(cities_json)
    [cities.append(c["name"]) for c in cities_load]

    async with AsyncClient() as session:
        for city in cities:
            requests.append(get_weather(session, city))
        temps = await asyncio.gather(*requests)
        return temps


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
