from django.urls import path

from . import views

urlpatterns = [
    path("chat/", views.chat),
    path("saveRoom/", views.saveRoom),
    path("getRooms/", views.getRooms.as_view()),
    path("getRoomMessages/", views.getRoomMessages),
    path("editRoom/", views.editRoom),
    path("deleteRoom/", views.deleteRoom)
]
