# Асинхронный

from aiohttp import web

from typing import Type
import json

from models import Session, Ad
from validate_scheme import CreateAd, PatchAd
from security import md5_hash_password

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


JSON_TYPE = 'application/json'


async def validate(json_data: dict,
             model_class: Type[CreateAd] | Type[PatchAd]):
    try:
        model_item = model_class(**json_data)
        return model_item.model_dump(exclude_none=True)
    except ValidationError as err:
        errHTTP = web.HTTPBadRequest
        errMSG = err.errors()[0]
        text = json.dumps({
            "status": str(errHTTP.status_code),  # 400
            "message": f"{errMSG['msg']} ({errMSG['input']})"
        })
        raise errHTTP(text=text, content_type=JSON_TYPE)


async def get_ad(ad_id: int, session: Session) -> Ad:
    ad = await session.get(Ad, ad_id)
    if ad is None:
        errHTTP = web.HTTPNotFound
        text = json.dumps({
            "status": errHTTP.status_code,  # 404
            "message": f"ad id={ad_id} not found"
        })
        raise errHTTP(text=text, content_type=JSON_TYPE)
    return ad


class AdView(web.View):
    async def get(self, user_id: int):                          # НАЙТИ
        pass

    async def post(self):                                       # ДОБАВИТЬ
        json_data = await self.request.json()
        json_data = await validate(json_data, CreateAd)

        new_ad = Ad(**json_data)
        self.request['session_from_middleware'].add(new_ad)
        try:
            await self.request['session_from_middleware'].commit()
        except IntegrityError as err:
            errHTTP = web.HTTPConflict
            text = json.dumps({
                "status":   str(errHTTP.status_code),  # 409
                "message":  f'ad already exists with the same data   {err}'
            })
            raise errHTTP(text=text, content_type=JSON_TYPE)
        return web.json_response({
                "status": f"advertisement add success",
                "id": new_ad.id
        })

    async def patch(self):
        pass

    async def delete(self):
        pass







