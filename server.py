# Асинхронный

from aiohttp import web

from settings import AIOHTTP_PORT

from models import engine, Base, Session

from handlers_ad import AdView
from handlers_user import UserView
from handler_hello_world import hello_world


async def orm_context(app: web.Application):
    print('START')
    # первая миграция:
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print('SHUT DOWN')


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session_from_middleware'] = session
        response = await handler(request)
        return response


app = web.Application()
app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


app.add_routes([
    web.get('/', hello_world),
    web.post('/', hello_world),

    web.post('/user/', UserView),
    # передадим регулярку, которой user_id должен соответствовать
    # ожидаем цифры от одной и более
    web.get('/user/{user_id:\d+}', UserView),
    web.patch('/user/{user_id:\d+}', UserView),
    web.delete('/user/{user_id:\d+}', UserView),

    web.post('/ad/', AdView),
    web.get('/ad/{ad_id:\d+}', AdView),
    web.patch('/ad/{ad_id:\d+}', AdView),
    web.delete('/ad/{ad_id:\d+}', AdView)
])


# точка входа ( как у asyncio.run(main) )
web.run_app(app, host='0.0.0.0', port=AIOHTTP_PORT)

