from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TransactionsConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]
        user_room_name = "user" + str(user.id)
        await self.channel_layer.group_add(
            user_room_name,
            self.channel_name
        )

        await self.accept()

    async def events_transaction(self, event):
        await self.send_json(
            {
                'type': 'events.transaction',
                'content': event['content']
            }
        )


