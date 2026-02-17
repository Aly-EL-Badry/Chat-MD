from django.urls import path
from .views import format_description, health, format_task

urlpatterns = [
    path('', health , name="Health request"),
    path('format/description/', format_description, name='format-description'),
    path('format/task/',format_task , name='format-task'),
]
