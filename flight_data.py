import requests
import os
import datetime as dt
import data_manager

#TODO add own tequila API as env variable

TEQUILA_API_KEY = os.environ["TEQUILA_API_KEY"]
TEQUILA_HEADER = {
    "apikey": TEQUILA_API_KEY
}
TEQUILA_EP = "https://tequila-api.kiwi.com/"
SEARCH_EP = "v2/search?"

data_manager = data_manager.DataManager()


class FlightData:
    def __init__(self):
        self.today = dt.datetime.today()
        self.sheet_data = data_manager.get_data()
        self.depart_city = "LON"

    # check for cheapest price available for each listed city, between tomorrow +6 months (6 x 30days). Round trips
    # between 7-28 days in length, currency in GBP

    def get_tomorrows_date(self):
        """returns tomorrow's date"""
        tomorrow_date = self.today + dt.timedelta(days=1)
        return tomorrow_date.strftime("%d/%m/%Y")

    def get_end_date(self):
        """returns end date, as tomorrow's date +180 days"""
        end_date = self.today + dt.timedelta(days=181)
        return end_date.strftime("%d/%m/%Y")

    def get_city_flight_data(self):
        """returns data for each city as a json and appends to list"""
        city_flight_data_list = []
        for row in self.sheet_data:
            query = {
                "fly_from": self.depart_city,
                "fly_to": row["IATA Code"],
                "date_from": self.get_tomorrows_date(),
                "date_to": self.get_end_date(),
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "flight_type": "round",
                "one_for_city": 1,
                "max_stopovers": 1,
                "curr": "GBP"
            }
            try:
                response = requests.get(
                    url=f"{TEQUILA_EP}{SEARCH_EP}",
                    headers=TEQUILA_HEADER,
                    params=query,
                )
                city_flight_data_list.append(response.json()['data'][0])

            except IndexError:
                pass

        return city_flight_data_list

    @staticmethod
    def convert_dates(json):
        """static used to convert depart date into datetime, then calculate return, and return list of str dates"""
        depart_date = json['local_departure'][0:10]
        depart_dt_obj = dt.datetime.strptime(depart_date, "%Y-%m-%d")
        duration = int(json['nightsInDest'])
        return_date = depart_dt_obj + dt.timedelta(days=duration)
        return (str(depart_dt_obj)[0:10], str(return_date)[0:10])

    def output_flight_data(self, json_list):
        """returns a dict of needed data from inputed json list"""
        flight_data_list = []
        for item in json_list:
            flight_data = {
                "price": item['price'],
                "departCity": item['cityFrom'],
                "departIATA": item['flyFrom'],
                "arriveCity": item['cityTo'],
                "arriveIATA": item['flyTo'],
                "outboundDate": self.convert_dates(item)[0],
                "returnDate": self.convert_dates(item)[1]
            }
            flight_data_list.append(flight_data)
        return flight_data_list
