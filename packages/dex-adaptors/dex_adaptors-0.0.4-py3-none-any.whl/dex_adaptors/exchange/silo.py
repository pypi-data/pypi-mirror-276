from .base import GqlClient


class SiloUnified(GqlClient):
    BASE_ENDPOINT = (
        "https://gateway-arbitrum.network.thegraph.com/api/{}/"
        "subgraphs/id/81ER342viJd3oRvPf28M7GwsnToa1RVWDNLnTr1eBciC"
    )

    def __init__(self, subgraph_api_key: str):
        super().__init__(base_endpoint=self.BASE_ENDPOINT.format(subgraph_api_key), fetch_schema_from_transport=False)

    async def _get_silo(self, address: str) -> dict:
        query = f"""
        {{
            silo(id: "{address.lower()}") {{
                id
                name
                isActive
                rates {{
                    rate
                    side
                    type
                    token {{
                        symbol
                    }}
                    utilization
                }}
                totalBorrowBalanceUSD
                totalDepositBalanceUSD
                totalValueLockedUSD
                market {{
                    name
                    borrowed
                    balance
                    supply
                }}
                baseAsset {{
                    name
                    symbol
                    decimals
                }}
                bridgeAsset {{
                    name
                    symbol
                    decimals
                }}
            }}
        }}
        """
        return await self.request(query)
