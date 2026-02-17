from rest_framework import serializers

class TextRequestSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=5)