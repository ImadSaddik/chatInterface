import os
import json
from dotenv import load_dotenv

import google.generativeai as palm

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room, Messages
from .serializers import RoomSerializer, MessagesSerializer


@api_view(['POST'])
def chat(request):
  setUpPalmAPI()
  data = json.loads(request.body)
  prompt = data['prompt']
  selectedModel = data['model'] # use this to select a model from the list of models
  
  completion = palm.generate_text(
    model=getModel(),
    prompt=prompt,
    temperature=0,
    max_output_tokens=800,
  )
  
  response = completion.result or 'Sorry, I don\'t understand.'
  
  return JsonResponse({'response': response})


def setUpPalmAPI():
  load_dotenv()
  
  api_key = os.getenv('API_KEY')
  palm.configure(api_key=api_key)


def getModel():
  models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
  model = models[0].name
  
  return model
 
  
@api_view(['POST'])
def saveRoom(request):
  data = json.loads(request.body)
  roomName = data['roomName']
  messages = data['messages']
  
  room = Room.objects.create(name=roomName)
  
  for message in messages:
    role = message['role']
    message = message['message']
    Messages.objects.create(room=room, role=role, message=message)
    
  return JsonResponse({'success': True})


class getRooms(APIView):
  def get(self, request, format=None):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)
  
  
def getRoomMessages(request):
  id = request.GET.get('id')
  room = Room.objects.get(id=id)
  
  messages = Messages.objects.filter(room=room)
  serializer = MessagesSerializer(messages, many=True)
  return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def editRoom(request):
  data = json.loads(request.body)
  
  room = Room.objects.get(id=data['id'])
  room.name = data['newName']
  room.save()
  
  return JsonResponse({'success': True})


@api_view(['POST'])
def deleteRoom(request):
  data = json.loads(request.body)
  
  room = Room.objects.get(id=data['id'])
  room.delete()
  
  return JsonResponse({'success': True})


@api_view(['POST'])
def updateRoomMessages(request):
  data = json.loads(request.body)
  room = Room.objects.get(id=data['id'])
  
  oldMessages = Messages.objects.filter(room=room)
  newMessages = data['messages']
  
  for i in range(len(oldMessages), len(newMessages)):
    Messages.objects.create(room=room, role=newMessages[i]['role'], message=newMessages[i]['message'])
    
  return JsonResponse({'success': True})
