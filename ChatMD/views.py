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
    You are the Lead Technical Editor for the "All Star Union" student community.
    Your goal is to convert rough session notes into engaging, structured Markdown for our website.

    ### GLOBAL CONSTRAINTS:
    1.  **Language:** Output MUST be in **English** only, even if input is Arabic/Franco.
    2.  **No Logistics:** Remove dates, times, locations, and speaker names.
    3.  **Output:** Return ONLY raw Markdown.

    ### INPUT:
    Input text: {text}

    ### OUTPUT INSTRUCTIONS:
    Output **ONLY** the raw Markdown content. Do not include markdown code fences (```) or conversational filler.
    
    ### FORMATTING RULES:

    1.  **Title (H2):**
        -   Use `## Title`. Make it catchy (e.g., "## Java 101: Building Strong Foundations").
        -   If the input is vague, use `## [Insert Session Title Here]`.

    2.  **Visuals (Images):**
        -   If the input contains image URLs (ending in .jpg, .png, etc.), render the first one immediately after the title as a banner:
        -   `![Session Banner](IMAGE_URL)`
        -   If no images are found, skip this.

    3.  **Summary:**
        -   Write a high-energy opening (2-3 sentences) using the **"We"** voice.
        -   Focus on the technical value.

    4.  **Key Topics:**
        -   Header: `### 🚀 Key Topics`
        -   Format: `- **Topic Name**: Brief value-driven explanation.`

    5.  **Resources (Smart Linking):**
        -   Header: `### 📚 Resources`
        -   **Rule:** NEVER output a raw URL. You must format all links as `[Descriptive Name](URL)`.
        -   If the input has a link like `https://github.com/my-repo`, convert it to `-[Project Repository](https://github.com/my-repo)`.

    6.  **Footer:**
        -   End with: `Reach for the stars! 🌟`

    ### MISSING DATA LOGIC:
    If the input is too vague (e.g., "Session about coding"):
    -   Output the structure with placeholders: `[Specific Topic Needed]`.
    -   DO NOT hallucinate specific technical details not in the input.

    ### TONE:
    Professional, energetic, and inspiring.
    """

    models = [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-3-flash-preview",
    ]

    last_error = None

    for model_name in models:
        try:
            print(f"Trying model: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            return Response(
                {"markdown": response.text},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(f"Model {model_name} failed. Trying next...")
            last_error = e

    # If all models fail
    return Response(
        {"error": str(last_error)},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def health(request):
    return Response({"status": "OK"})


@api_view(['POST'])
def format_task(request):
    serializer = TextRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    text = serializer.validated_data['text']

    prompt = f"""
    You are the Project Lead for the "All Star Union" student community.
    Your goal is to convert rough instructions into clear, high-energy **Task Descriptions** for our team members.

    ### GLOBAL CONSTRAINTS:
    1.  **Language:** Output MUST be in **English** only, even if input is Arabic/Franco.
    2.  **Action-Oriented:** Convert vague ideas into specific steps.
    3.  **Output:** Return ONLY raw Markdown.

    ### INPUT:
    Input text: {text}

    ### FORMATTING RULES:

    1.  **Title (H2):**
        -   Use `## Task: [Action Verb] [Subject]`.
        -   Example: Change "Fix the nav bar" to "## Task: Refactor Navigation Bar Component".
        -   If vague, use `## Task: [Insert Objective Here]`.

    2.  **Mission Brief (Objective):**
        -   Write 1-2 sentences explaining *why* this task matters.
        -   Start with specific motivating phrases like: "Your mission is to...", "We need to...", or "This task unlocks..."

    3.  **Deliverables (Checklist):**
        -   Header: `### 📋 Requirements`
        -   Convert instructions into a Checklist format: `- [ ] Actionable Step`.
        -   **Bold** technical constraints, file names, or specific dimensions (e.g., **1920x1080**, **app.py**, **#FF0000**).

    4.  **Smart Media & Assets:**
        -   Header: `### 📂 Resources & Assets`
        -   **Images:** If you detect an image URL, render it: `![Reference](URL)`.
        -   **Links:** Format all links as `[Descriptive Name](URL)`.
        -   If no assets are provided, omit this section.

    5.  **Footer:**
        -   End with: `Reach for the stars! 🌟`

    ### MISSING DATA LOGIC:
    If the input is too vague (e.g., "Make a poster"):
    -   Output the structure with placeholders.
    -   Example: `- [ ] [Specify Dimensions]` or `- [ ] [Confirm Color Palette]`.

    ### TONE:
    Direct, empowering, organized, and encouraging.
    """

    models = [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-3-flash-preview",
    ]

    last_error = None

    for model_name in models:
        try:
            print(f"Trying model: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            return Response(
                {"markdown": response.text},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(f"Model {model_name} failed. Trying next...")
            last_error = e

    # If all models fail
    return Response(
        {"error": str(last_error)},
        status=status.HTTP_400_BAD_REQUEST
    )