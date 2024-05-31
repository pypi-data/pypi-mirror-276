from .exchange.silo import SiloUnified
from .parsers.silo import SiloParser


class Silo(SiloUnified, SiloParser):
    def __init__(self, subgrapoh_api_key: str):
        super().__init__(subgraph_api_key=subgrapoh_api_key)

    async def get_pool_data(self, address: str) -> dict:
        return self.parse_pool_data(await self._get_silo(address))
