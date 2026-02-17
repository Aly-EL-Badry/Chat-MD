import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from google import genai
from dotenv import load_dotenv
from .serializers import TextRequestSerializer

# Load env
load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")
if not apiKey:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

client = genai.Client(api_key=apiKey)


@api_view(['POST'])
def format_description(request):
    serializer = TextRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    text = serializer.validated_data['text']

    prompt = f"""
    You are an expert Technical Editor for a student activity website. Your goal is to convert session descriptions into engaging, structured Markdown.

    ### INPUT:
    You will receive text that might be a rough paragraph OR a list of notes (e.g., "Session Name:", "Topics:", "Resources:").
    Input :{text}

    ### OUTPUT:
    Output ONLY the formatted Markdown code. Do not output code fences (```) or conversational text.

    ### FORMATTING RULES:
    1.  **Title:**
        -   Use the provided "Session Name" or "Title" as an H2 (## Title).
        -   If no title is provided, generate a catchy, professional H2 title based on the content.

    2.  **Summary:**
        -   Write a concise, high-energy opening paragraph (2-3 sentences) summarizing the session's value.
        -   Use the "We" voice (e.g., "In this session, we explored...").

    3.  **Key Topics:**
        -   Create a section header: `### 🚀 Key Topics`
        -   List topics using bullet points.
        -   **Crucial:** Do not just list the keyword. Add a short phrase explaining it.
        -   Format: `- **Topic Name**: Brief explanation of why it matters.`

    4.  **Resources (If present):**
        -   Create a section header: `### 📚 Resources`
        -   Detect any links provided in the text (often formatted as `[Name] [URL]` or just raw URLs).
        -   Convert them into proper clickable Markdown links: `-[Resource Name](URL)`.

    5.  **Styling:**
        -   **Bold** key technologies (e.g., **Python**, **Docker**, **React**).
        -   Fix all grammar, spelling, and capitalization errors.

    ### TONE:
    Professional, energetic, and encouraging. usage of emojis in headers is allowed to make it friendly.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        return Response({"markdown": response.text}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"detail": f"Failed to generate the response, {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def health(request):
    return Response({"status": "OK"})