import requests

class OddsAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.the-odds-api.com"
        self.api_key = api_key

    def get_odds(self, sport: str, bookmakers: str):
        try:
            url = f"{self.base_url}/v4/sports/{sport}/odds/"
            params = {
                "apiKey": self.api_key,
                "regions": "us",
                "bookmakers": bookmakers,
                "markets": "spreads,h2h,totals",
                "oddsFormat": "american",
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            raise exc
