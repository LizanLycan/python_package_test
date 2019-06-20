import requests
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Ticker


# Handler for pair ticker sockets
class PairTickerConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = '_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        raw_data = requests.get("https://api.tidex.com/api/3/ticker/{}".
                                format(self.room_name)).json()

        if "error" in raw_data:
            self.close()

        else:
            self.handling_request_data()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        self.handling_request_data()

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message + ' (send from chat message)'
        }))

    def ticker(self, event):
        data = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'data': data
        }))

    def handling_request_data(self):
        raw_data = requests.get(
            "https://api.tidex.com/api/3/ticker/{}".
            format(self.room_name)).json()

        Ticker.objects.create(
            pair=self.room_name,
            high=raw_data[self.room_name]['high'],
            low=raw_data[self.room_name]['low'],
            avg=raw_data[self.room_name]['avg'],
            vol=raw_data[self.room_name]['vol'],
            vol_cur=raw_data[self.room_name]['vol_cur'],
            last=raw_data[self.room_name]['last'],
            buy=raw_data[self.room_name]['buy'],
            sell=raw_data[self.room_name]['sell'],
            updated=raw_data[self.room_name]['updated']
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'ticker',
                'message': raw_data[self.room_name]
            }
        )
