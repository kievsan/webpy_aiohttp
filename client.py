import asyncio

import aiohttp


async def main():
    URL = 'http://127.0.0.1:8080'

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
                'username': 'user_222',
                'password': '23456789',
                'email': 'u222@ya.ru'
            },
            params={}, headers={}
        )
        data = await response.json()
        print(data)


        # response = await session.get(URL + '/user/1',
        #     json={},params={}, headers={}
        # )
        # data = await response.json()
        # print(data)





asyncio.run(main())
