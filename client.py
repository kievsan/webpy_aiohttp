import asyncio

import aiohttp

from db_conf import AIOHTTP_HOST, AIOHTTP_PORT


async def main():
    URL = f'http://{AIOHTTP_HOST}:{AIOHTTP_PORT}'

    async with aiohttp.ClientSession() as session:
        response = await session.get(URL + '/', json={})
        data = await response.json()
        print(data)

        # response = await session.post(
        #     URL + '/',
        #     json={
        #         'json_key': 'json_value'
        #     },
        #     params={
        #         'qs_key_1': 'qs_value_1'  # query string
        #     },
        #     headers={
        #         'token': 'some_token'
        #     }
        # )
        # #   читаем json от сервера
        # data = await response.json()
        # print(data)  # должен прийти словарик {'Hello': 'world'}

        response = await session.post(URL + '/user/',
            json={
                'username': 'user_111',
                'password': '12345678',
                'email': 'u111@ya.ru'
            },
            params={}, headers={}
        )
        data = await response.json()
        print(data)


        response = await session.get(URL + '/user/1',
            json={},params={}, headers={}
        )
        try:
            data = await response.json()
        except Exception as err:
            print(err)
            data = await response.text()
        print(data)





asyncio.run(main())