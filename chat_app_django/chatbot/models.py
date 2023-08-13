from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Messages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.message
