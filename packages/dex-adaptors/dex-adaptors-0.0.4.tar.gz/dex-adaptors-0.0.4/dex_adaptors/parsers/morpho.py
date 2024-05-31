from .base import Parser


class MorphoParser(Parser):
    def __init__(self):
        super().__init__(name="morpho")

    @staticmethod
    def parse_instrument_id(data: dict) -> str:
        """
        return instrument_id with {loan asset}/{collateral asset}
        """
        return f"{data['loanAsset']['symbol']}/{data['collateralAsset']['symbol']}"

    def parse_vault_by_address(self, response: dict) -> dict:
        return

    def parse_exchange_info(self, response: dict) -> dict:
        datas = response["markets"]["items"]

        results = {}
        for data in datas:
            if not data["collateralAsset"]:
                continue
            instrument_id = self.parse_instrument_id(data)
            results[data["uniqueKey"]] = {
                "active": True,
                "instrument_id": instrument_id,
                "symbol": instrument_id,
                "base": {
                    "name": data["loanAsset"]["symbol"],
                    "address": data["loanAsset"]["address"],
                    "decimals": data["loanAsset"]["decimals"],
                },
                "quote": {
                    "name": data["collateralAsset"]["symbol"],
                    "address": data["collateralAsset"]["address"],
                    "decimals": data["collateralAsset"]["decimals"],
                },
                "borrow_apy": self.parse_str(data["state"]["borrowApy"], float),
                "supply_apy": self.parse_str(data["state"]["supplyApy"], float),
                "unique_key": data["uniqueKey"],
                "raw_data": data,
            }
        return results

    def parse_user_positions(self, response: dict, pools_info: dict) -> dict:
        def parse_positions(positions) -> dict:
            results = {}
            for position in positions:
                unique_key = position["market"]["uniqueKey"]
                pool_name = pools_info[unique_key]["instrument_id"]
                result = {
                    "pool_name": pool_name,
                    "unique_key": position["market"]["uniqueKey"],
                    "lltv": self.parse_str(position["market"]["lltv"], float) / 10**18,
                    "health_factor": self.parse_str(position["healthFactor"], float),
                    "collateral": {
                        "currency": position["market"]["collateralAsset"]["symbol"],
                        "amount": self.parse_str(position["collateral"], float)
                        / 10 ** (position["market"]["collateralAsset"]["decimals"]),
                        "usd_value": self.parse_str(position["collateralUsd"], float),
                    },
                    "borrow": {
                        "currency": position["market"]["loanAsset"]["symbol"],
                        "amount": self.parse_str(position["borrowAssets"], float)
                        / 10 ** (position["market"]["loanAsset"]["decimals"]),
                        "usd_value": self.parse_str(position["borrowAssetsUsd"], float),
                    },
                }
                result["current_ltv"] = result["borrow"]["usd_value"] / result["collateral"]["usd_value"]
                results[unique_key] = result
            return results

        data = response["userByAddress"]
        positions = data["marketPositions"]
        return {
            "timestamp": self.get_timestamp(),
            "user_address": data["address"],
            "positions": parse_positions(positions),
            "raw_data": data,
        }

    def parse_market_positions(self, response: dict, pools_info: dict) -> list:
        datas = response["marketPositions"]["items"]
        results = []

        unique_key = datas[0]["market"]["uniqueKey"]
        pool = pools_info[unique_key]
        for data in datas:
            if not data["healthFactor"]:
                continue
            results.append(
                {
                    "pool_name": pool["instrument_id"],
                    "unique_key": data["market"]["uniqueKey"],
                    "user_address": data["user"]["address"],
                    "lltv": self.parse_str(data["market"]["lltv"], float) / 10**18,
                    "health_factor": self.parse_str(data["healthFactor"], float),
                    "collateral": {
                        "currency": data["market"]["collateralAsset"]["symbol"],
                        "amount": self.parse_str(data["collateral"], float)
                        / 10 ** (data["market"]["collateralAsset"]["decimals"]),
                        "usd_value": self.parse_str(data["collateralUsd"], float),
                    },
                    "borrow": {
                        "currency": data["market"]["loanAsset"]["symbol"],
                        "amount": self.parse_str(data["borrowAssets"], float)
                        / 10 ** (data["market"]["loanAsset"]["decimals"]),
                        "usd_value": self.parse_str(data["borrowAssetsUsd"], float),
                    },
                    "current_ltv": self.parse_str(data["borrowAssetsUsd"], float)
                    / self.parse_str(data["collateralUsd"], float),
                    "raw_data": data,
                }
            )
        return results
