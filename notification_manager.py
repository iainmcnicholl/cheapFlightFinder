import data_manager
from twilio.rest import Client
import os

data_manager = data_manager.DataManager()

#TODO add API key and token/sid details as env variables

endpoint = "https://api.openweathermap.org/data/2.5/onecall?"
api_key = "0ee5c89fe6ded7887763ab208588f3cc"
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


class NotificationManager:
    def __init__(self):
        self.sheet_data = data_manager.get_data()

    def send_notification(self, data_list, count):
        """sends message with information about flights passed in as data_list"""
        message = client.messages.create(
            body=f"Low price alert! Only £{data_list[count]['price']} to fly from {data_list[count]['departCity']}-"
                 f"{data_list[count]['departIATA']} to {data_list[count]['arriveCity']}-"
                 f"{data_list[count]['arriveIATA']}, "
                 f"from {data_list[count]['outboundDate']} to {data_list[count]['returnDate']}",
            from_='++17652759137',
            to='+4407903890096'
        )
        print(message.sid)

