# your_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Player

class MatchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Add the WebSocket consumer to a group
        await self.channel_layer.group_add('match_group', self.channel_name)

    async def disconnect(self, close_code):
        # Remove the WebSocket consumer from the group
        await self.channel_layer.group_discard('match_group', self.channel_name)

    async def receive(self, text_data):
        # Receive a message from the WebSocket
        message = json.loads(text_data)
        player_name = message.get('player_name')

        # Add the player to the group and check for matches
        await self.add_player_to_group(player_name)

    @sync_to_async
    def add_player_to_group(self, player_name):
        # Add the player to the group
        player = Player.objects.get(name=player_name)
        self.channel_layer.group_add('match_group', self.channel_name)

        # Check for matches when a player is added
        self.check_for_matches()

    @sync_to_async
    def check_for_matches(self):
        # Check for matches and notify the players
        waiting_players = Player.objects.filter(is_waiting=True)[:2]

        if len(waiting_players) == 2:
            # Update the status of the matched players
            for player in waiting_players:
                player.is_waiting = False
                player.save()

            # Notify the matched players about the match
            self.send_message_to_group({'matched': True})

    async def send_message_to_group(self, content):
        # Send a message to the group
        await self.channel_layer.group_send(
            'match_group',
            {
                'type': 'send_message',
                'message': content,
            }
        )

    async def send_message(self, event):
        # Send a message to the WebSocket
        message = event['message']
        await self.send(text_data=json.dumps(message))
