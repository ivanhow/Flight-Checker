import requests
from datetime import datetime, timedelta
from flight_data import FlightData
from notification_manager import NotificationManager

KIWI_ENDPOINT = "https://tequila-api.kiwi.com"
API_KIWI = '75yZDufIEWtYp6k5bPK9ogKG0uSRE0wr'


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self, destinations):
        self.destinations = destinations
        self.populate_iatacode()

    def search_iatacode(self, city_name):
        header = {'apikey': API_KIWI}
        parameters = {"term": city_name, "location_types": "city"}
        response = requests.get(url=f'{KIWI_ENDPOINT}/locations/query', params=parameters, headers=header)
        results = response.json()
        city_name = results['locations'][0]['code']
        return city_name

    def populate_iatacode(self):
        for i in range(len(self.destinations)):
            if self.destinations[i].get('iataCode') == '':
                city_name = self.search_iatacode(self.destinations[i].get('city'))
                self.destinations[i]['iataCode'] = city_name
        return self.destinations

    def check_flights(self, data):
        header = {'apikey': API_KIWI}
        self.destinations = data
        today = datetime.today()
        tomorrow = (today + timedelta(days=1)).strftime('%d/%m/%Y')
        six_months_ahead = (today + timedelta(180)).strftime('%d/%m/%Y')
        for i in range(len(self.destinations)):
            fly_to = self.destinations[i].get('iataCode')
            parameters = {
                'fly_from': 'LON',
                'fly_to': fly_to,
                'dateFrom': tomorrow,
                'dateTo': six_months_ahead,
                'flight_type': 'round',
                'one_for_city': 1,
                'adults': 1,
                'curr': 'GBP',
                'max_stopovers': 0,
                'nights_in_dst_from': 7,
                'nights_in_dst_to': 28,
            }
            response = requests.get(url=f'{KIWI_ENDPOINT}/v2/search', params=parameters, headers=header)

            try:
                data = response.json()["data"][0]
            except IndexError:
                pass
                # print(f"No flights found for {self.destinations[i]['city']}.\n")
                # return None

            # print(response.json()['data'][0])
            else:
                price = data['price']
                if price <= self.destinations[i].get('lowestPrice'):
                    flight_data = FlightData(
                        price=data['price'],
                        origin_city=data['cityFrom'],
                        origin_airport=data['flyFrom'],
                        destination_city=data['cityTo'],
                        destination_airport=data['flyTo'],
                        out_date=data['route'][0]['local_departure'].split('T')[0],
                        return_date=data['route'][1]['local_arrival'].split('T')[0]
                    )

                    NotificationManager(flight_data)

                    # print(f"{flight_data.destination_city}: £{flight_data.price}")
                    # print(f"Departure {flight_data.out_date}, return {flight_data.return_date}\n")
            # return flight_data
