from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ChatMD.urls')),  # FastAPI logic now lives under Django
]
