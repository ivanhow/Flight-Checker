#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from flight_search import FlightSearch
from data_manager import DataManager


data = DataManager()



print('Welcome to my flight club')

registration_on = False
while not registration_on:
    first_name = input('Your first name: ')
    last_name = input('Your last name: ')
    email = input('Your e-mail: ')
    confirmed_mail = input('Confirm your e-mail: ')
    if email == confirmed_mail:
        data.update_user(first_name, last_name, email)
        registration_on = True







sheet_data = data.get_sheety_data()
# print(sheet_data)

flight_search = FlightSearch(sheet_data)
flight_search.populate_iatacode()
data.update_sheety_data(sheet_data)
updated_sheet_data = data.get_sheety_data()
flight_search.check_flights(updated_sheet_data)
