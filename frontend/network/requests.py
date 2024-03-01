import aiohttp


BASE_URL = "http://backend:8000/"


async def prefetch_business_type_data(*args) -> list[dict]:
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.get(f"/businesstype") as resp:
            response = await resp.json()
            return response


async def prefetch_business_area_data(*args) -> list[dict]:
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        business_type_id = args[0]
        async with session.get(f"/businessarea/{business_type_id}") as resp:
            response = await resp.json()
            return response


async def get_all_existing_business_areas(*args) -> list[dict]:
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.get("/businessarea") as resp:
            response = await resp.json()
            return response


async def add_business_type(*args, data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.post("/businesstype", json=data) as resp:
            print(resp.status)


async def add_business(data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.post("/business", json=data) as resp:
            response = await resp.json()
            return response


async def update_business(business_id: str, data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.patch(f"/business/{business_id}", json=data) as resp:
            print(resp.status)


async def add_business_area(*args, data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        business_type_id = args[0]
        data["businesstype_id"] = business_type_id
        async with session.post(f"/businessarea/{business_type_id}", json=data) as resp:
            print(resp.status)


async def delete_business_type(business_type_id: str):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.delete(f"/businesstype/{business_type_id}") as resp:
            print(resp.status)


async def delete_business_area(business_area_id: str):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.delete(f"/businessarea/{business_area_id}") as resp:
            print(resp.status)


async def delete_question(question_id: str):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.delete(f"/question/{question_id}") as resp:
            print(resp.status)


async def get_business_area_questions(business_area_id: str):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.get(f"/businessarea/{business_area_id}/questions") as resp:
            response = await resp.json()
            return response


async def get_question_areas(question_id: str):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.get(f"/question/{question_id}/business_areas") as resp:
            response = await resp.json()
            return response


async def add_question(*args, data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.post("/question", json=data) as resp:
            response = await resp.json()
            return response


async def update_question(*args, question_id: str, data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.patch(f"/question/{question_id}", json=data) as resp:
            print(resp.status)


async def create_or_update_answer(data: dict):
    async with aiohttp.ClientSession(base_url=BASE_URL) as session:
        async with session.post("/answer", json=data) as resp:
            print(resp.status)
