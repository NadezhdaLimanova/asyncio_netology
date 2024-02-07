import asyncio
import datetime
import aiohttp
from more_itertools import chunked
from sqlalchemy import select

from models import init_db, Session, engine, Person


async def get_persons(client, person_id):
    response = await client.get(f'https://swapi.dev/api/people/{person_id}')
    json_result = await response.json()
    return json_result


async def get_person_list():
    await init_db()
    client = aiohttp.ClientSession()
    for chunk in chunked(range(1, 20), 10):
        person_list = []
        for person_id in chunk:
            coro_person = get_persons(client, person_id)
            person_list.append(coro_person)
        result = await asyncio.gather(*person_list)
        insert_task = asyncio.create_task(fill_db(result))
    await client.close()
    await engine.dispose()



async def fill_db(list_of_jsons):
    for item in list_of_jsons:
        if 'name' in item:
            model = Person(birth_year=item['birth_year'], eye_color=item['eye_color'],
                           films=item['films'], gender=item['gender'], hair_color=item['hair_color'],
                           height=item['height'], homeworld=item['homeworld'], mass=item['mass'], name=item['name'],
                           skin_color=item['skin_color'], species=item['species'], starships=item['starships'],
                           vehicles=item['vehicles'])
            async with Session() as session:
                session.add(model)
    await session.commit()


if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(get_person_list())
    print(datetime.datetime.now() - start)
