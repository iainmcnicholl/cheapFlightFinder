import requests
import os

#TODO add own tequila API as env variable


TEQUILA_API_KEY = os.environ["TEQUILA_API_KEY"]
TEQUILA_HEADER = {
    "apikey": TEQUILA_API_KEY
}
TEQUILA_EP = "https://tequila-api.kiwi.com/"
LOCATION_EP = "locations/query?"


class FlightSearch:

    def return_iata_code(self, city):
        """returns IATA code for the city passed to function"""
        params = {
            "term": city,
            "location_types": "airport"
        }
        response = requests.get(url=f"{TEQUILA_EP}{LOCATION_EP}", params=params, headers=TEQUILA_HEADER)
        iata_data = response.json()
        return iata_data["locations"][0]["code"]


