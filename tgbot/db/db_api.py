import aiohttp


async def create_user(user_id, user_name, user_phone, config):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}user/create/",
                                data={"tg_id": user_id, "user_name": user_name,
                                      "user_phone": user_phone}) as response:
            return await response.json()


async def get_user(user_id, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}user/get/{user_id}") as response:
            return await response.json()


async def get_contacts(config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}calls/") as response:
            return await response.json()


async def get_sector(config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}sector/") as response:
            return await response.json()


async def get_rows(option, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}row/", params={"option": option}) as response:
            return await response.json()


async def get_places(option, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}place/", params={"option": option}) as response:
            return await response.json()


async def get_place(option, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}place/{option}") as response:
            return await response.json()


async def create_order(config, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}order/create/", data={"user": kwargs["user"],
                                                                                    "place": kwargs["place"],
                                                                                    "pay_type": kwargs["pay_type"],
                                                                                    "total_price": kwargs["total_price"]
                                                                                    }) as response:
            return await response.json()


async def get_order(config, tg_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}order/get/", params={"tg_id": tg_id}) as response:
            return await response.json()


async def get_about(config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}about/") as response:
            return await response.json()

