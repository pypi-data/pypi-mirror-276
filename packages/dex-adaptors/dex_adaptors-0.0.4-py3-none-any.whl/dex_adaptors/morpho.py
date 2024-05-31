from .exchange.morpho import MorphoUnified
from .parsers.morpho import MorphoParser


class Morpho(MorphoUnified, MorphoParser):
    def __init__(self):
        super().__init__()

        self.pools_info = None

    async def get_vault_by_address(self, chain: str, address: str) -> dict:
        if chain not in self.CHAIN_ID_MAP.keys():
            raise ValueError(f"Chain {chain} not supported. Supported chains: {self.CHAIN_ID_MAP.keys()}")
        chain_id = self.CHAIN_ID_MAP[chain]

        params = {"chain_id": chain_id, "address": address}
        return self.parse_vault_by_address(await self._get_vault_by_address(**params))

    async def get_exchange_info(self):
        self.pools_info = self.parse_exchange_info(await self._get_markets_info())
        return self.pools_info

    async def get_user_positions(self, address: str) -> dict:
        return self.parse_user_positions(await self._get_user_positions(address), self.pools_info)

    async def get_market_positions(self, unique_key: str, num: int = 1000) -> list:
        return self.parse_market_positions(await self._get_market_positions(unique_key, num), self.pools_info)
