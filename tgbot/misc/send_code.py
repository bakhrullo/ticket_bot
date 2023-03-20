import random


async def send_code(number, config):
    rand_int = random.randint(1000, 9999)
    return rand_int
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url=f"{config.db.database_url}user/create/",
    #                             data={"tg_id": user_id, "user_name": user_name,
    #                                   "user_phone": user_phone}) as response:
    #         return await response.json()