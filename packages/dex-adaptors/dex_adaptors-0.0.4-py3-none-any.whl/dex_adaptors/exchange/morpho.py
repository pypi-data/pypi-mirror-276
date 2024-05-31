from .base import GqlClient


class MorphoUnified(GqlClient):
    BASE_ENDPOINT = "https://blue-api.morpho.org/graphql"

    def __init__(self):
        super().__init__(self.BASE_ENDPOINT, fetch_schema_from_transport=False)

    async def _get_vault_by_address(self, chain_id: str, address: str):
        query = f"""
        query {{
            vaultByAddress(
                address: "{address}"
                chainId: {chain_id}
            )
            {{
                id
                state {{
                    allocation {{
                        market {{
                            uniqueKey
                        }}
                        supplyCap
                        supplyAssets
                        supplyAssetsUsd
                    }}
                }}
            }}
        }}
        """
        return await self.request(query=query)

    async def _get_markets_info(self) -> dict:
        query = """
        query {
            markets {
                items {
                    uniqueKey
                    lltv
                    oracleAddress
                    irmAddress
                    loanAsset {
                        address
                        symbol
                        decimals
                    }
                    collateralAsset {
                        address
                        symbol
                        decimals
                    }
                    state {
                        borrowApy
                        borrowAssets
                        borrowAssetsUsd
                        supplyApy
                        supplyAssets
                        supplyAssetsUsd
                        fee
                        utilization
                    }
                }
            }
        }
        """
        return await self.request(query=query)

    async def _get_user_positions(self, address: str) -> dict:
        query = f"""
        query {{
        userByAddress (
            address: "{address}"
        ) {{
            address
            marketPositions {{
                healthFactor
                borrowAssets
                collateral
                collateralUsd
                borrowAssetsUsd
                market {{
                    uniqueKey
                    lltv
                    collateralAsset {{
                        symbol
                        decimals
                    }}
                    loanAsset {{
                        symbol
                        decimals
                    }}
                    collateralPrice
                    }}
                }}
            }}
        }}
        """
        return await self.request(query=query)

    async def _get_market_positions(
        self, unique_key: str, num: int = 1000, orderBy: str = "BorrowShares", orderDirection: str = "Desc"
    ) -> dict:
        query = f"""
        {{
            marketPositions(
                first: {num}
                orderBy: {orderBy}
                orderDirection: {orderDirection}
                where: {{
                    marketUniqueKey_in: [
                        "{unique_key}"
                    ]
                }}
            ) {{
                items {{
                    healthFactor
                    supplyShares
                    supplyAssets
                    supplyAssetsUsd
                    borrowShares
                    borrowAssets
                    borrowAssetsUsd
                    collateral
                    collateralUsd
                    market {{
                        uniqueKey
                        lltv
                        loanAsset {{
                            address
                            symbol
                            decimals
                        }}
                        collateralAsset {{
                            address
                            symbol
                            decimals
                        }}
                    }}
                    user {{
                        address
                    }}
                }}
            }}
        }}
        """
        return await self.request(query=query)
