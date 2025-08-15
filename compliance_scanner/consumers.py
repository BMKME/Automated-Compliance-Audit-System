# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ComplianceStatus

class ComplianceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        self.room_group_name = 'compliance_updates'  # You can change this group name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the WebSocket group when disconnected
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        data = json.loads(text_data)
        ip_address = data['ip_address']

        # Fetch updated compliance status from the database
        compliance_status = ComplianceStatus.objects.filter(ip_address=ip_address).first()
        
        # Send updated compliance data back to the WebSocket
        await self.send(text_data=json.dumps({
            'ip_address': compliance_status.ip_address,
            'status': compliance_status.compliance_status,
            'last_checked': str(compliance_status.last_checked),
        }))
