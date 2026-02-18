from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import TextRequestSerializer
from .services.ai_service import AIService
from .services.prompt_service import PromptService


@api_view(['GET'])
def health(request):
    return Response({"status": "OK"})


@api_view(['POST'])
def format_description(request):
    serializer = TextRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    text = serializer.validated_data["text"]

    try:
        prompt = PromptService.build_description_prompt(text)
        result = AIService.generate(prompt)

        return Response({"markdown": result})

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def format_task(request):
    serializer = TextRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    text = serializer.validated_data["text"]

    try:
        prompt = PromptService.build_task_prompt(text)
        result = AIService.generate(prompt)

        return Response({"markdown": result})

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
