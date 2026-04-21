import httpx
from fastapi import Depends


async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client