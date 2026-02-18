from django.conf import settings
from ..core.gemini_client import client


class AIService:
    MODELS = [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-3-flash-preview",
    ]

    @classmethod
    def generate(cls, prompt: str) -> str:
        last_error = None

        for model_name in cls.MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                return response.text

            except Exception as e:
                last_error = e

        raise RuntimeError(f"All AI models failed: {last_error}")
