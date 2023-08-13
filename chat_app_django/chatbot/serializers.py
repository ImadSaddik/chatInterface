from rest_framework import serializers

from .models import Room, Messages


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id",
            "name"
        ]
        
        
class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = [
            "id",
            "role",
            "message",
            "room"
        ]
