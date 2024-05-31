from .base import Parser


class SiloParser(Parser):
    def __init__(self):
        super().__init__(name="silo")

    def parse_instrument_id(self, data: dict) -> str:
        base_asset = data["baseAsset"]["symbol"]

        bridge_asset = sorted([i["symbol"] for i in data["bridgeAsset"]])
        return f"{base_asset}-{'-'.join(bridge_asset)}"

    def parse_rates(self, data: dict, side: str) -> dict:
        brs = {}
        for rate in data["rates"]:
            if (side == "borrow" and rate["side"] == "BORROWER") or (side == "supply" and rate["side"] == "LENDER"):
                currency = rate["token"]["symbol"]
                brs[currency] = {
                    "currency": currency,
                    "side": side,
                    "rate": self.parse_str(rate["rate"], float) / 100,
                }
        return brs

    def parse_pool_data(self, response: dict) -> dict:
        data = response["silo"]
        instrument_id = self.parse_instrument_id(data)
        return {
            "timestamp": self.get_timestamp(),
            "active": data["isActive"],
            "chain": None,
            "address": data["id"],
            "instrument_id": instrument_id,
            "borrow_rates": self.parse_rates(data, "borrow"),
            "supply_rates": self.parse_rates(data, "supply"),
            "updated_timestamp": self.get_timestamp(),
            "raw_data": data,
        }
