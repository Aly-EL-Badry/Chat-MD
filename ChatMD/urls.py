from django.urls import path
from .views import format_description, health

urlpatterns = [
    path('', health , name="Health request"),
    path('format/description/', format_description, name='format-description'),
]
