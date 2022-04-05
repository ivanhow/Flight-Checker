import requests

api_sheety = 'https://api.sheety.co/Your Sheety Details'

sheety_headers = {
    "Authorization": "Bearer Your Sheety Key"
}


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        pass

    def get_sheety_data(self):
        sheety_request = requests.get(url=f'{api_sheety}/prices', headers=sheety_headers)
        return sheety_request.json()['prices']

    def update_sheety_data(self, travel_list):
        sheet_input = {
            'price': {

            }
        }
        for i in range(len(travel_list)):
            for k, v in travel_list[i].items():
                sheet_input['price'][k] = v
            # print(sheet_input)
            requests.put(url=f'{api_sheety}/prices/{sheet_input["price"]["id"]}', json=sheet_input,
                         headers=sheety_headers)

    def update_user(self, first_name, second_name, email):
        users = requests.get(url=f'{api_sheety}/users',
                             headers=sheety_headers)
        number_users = len(users.json()['users'])

        sheet_input = {
            'user': {
                'firstName': first_name,
                'lastName': second_name,
                'email': email
            }
        }

        requests.put(url=f'{api_sheety}/users/{number_users + 2}', json=sheet_input,
                     headers=sheety_headers)

    def get_user_mails(self):
        emails = []
        users = requests.get(url=f'{api_sheety}/users',
                             headers=sheety_headers)
        users_list = users.json()['users']
        for i in range(len(users_list)):
            emails.append(users_list[i]['email'])

        return emails
