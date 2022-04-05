import smtplib

from data_manager import DataManager
from flight_data import FlightData

MY_EMAIL = 'test@photoretoucher.eu'
MY_PASSWORD = 'mikolino2009'


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self, flight_data: FlightData):
        self.flight = flight_data
        self.emails = DataManager().get_user_mails()
        self.send_mail(emails=self.emails)

    def send_mail(self, emails):
        for i in range(len(emails)):
            mail = emails[i]
            with smtplib.SMTP('mail.photoretoucher.eu') as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL,
                                    to_addrs=f'{mail}',
                                    msg=f'Subject: New Flight\n\nPrice: {self.flight.price}\n\n'
                                        f'Departure City Name {self.flight.origin_city}\n\n'
                                        f'Departure Airport IATA Code {self.flight.origin_airport}\n\n'
                                        f'Arrival City Name {self.flight.destination_city}\n\n'
                                        f'Arrival Airport IATA Code {self.flight.destination_airport}\n\n'
                                        f'Outbound Date {self.flight.out_date}\n\n'
                                        f'Inbound Date {self.flight.return_date}'
                                    )