import aiohttp

from config import auth_data
from yarl import URL


class Alphador:
    def __init__(self):
        self.username = auth_data[0]
        self.password = auth_data[1]
        self.client = aiohttp.ClientSession(URL("https://alphador.ai/"))

    async def login(self) -> dict:
        return await self.requester(
            "/api/auth/login", "POST",
            data = {
                "username": self.username, 
                "password": self.password
            },
        )

    async def wallet_analyze(self, address: str, period: int = 7, chanid: int = 1) -> dict:
        return await self.requester(
            f"/api/wallets/analyze-pnl",
            params = {
                "address": address,
                "period": period,
                "chainId": chanid
            },
        )

    async def wallet_analyze_full(self, address: str) -> list:
        return [
            (await self.wallet_analyze(address, 1)),
            (await self.wallet_analyze(address, 7)),
            (await self.wallet_analyze(address, 30)),
        ]

    async def close(self) -> bool:
        await self.client.close()
        return True

    async def requester(
        self,
        url: str = "/",
        method: str = "GET",
        params: dict = {},
        data: dict = {},
        headers: dict = {},
        output="json",
    ):
        async with self.client.request(
            method, url, data=data, headers=headers, params=params
        ) as response:
            if output == "json":
                return await response.json()
            elif output == "text":
                return await response.text()
