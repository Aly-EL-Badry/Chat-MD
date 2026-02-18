# 🌟 Chat MD - All Star Union Content Engine

**Chat MD** is an intelligent backend service designed to automate and standardize content creation for the **All Star Union** community.

It leverages **Google Gemini (Generative AI)** to transform raw, unstructured notes into professionally formatted Markdown for:
1.  **Public Session Recaps** (Web-ready, engaging summaries).
2.  **Internal Task Assignments** (Actionable, clear checklists).

---

## 🚀 Key Features

* **Dual-Persona AI:** Automatically switches between an "Energetic Editor" tone for public content and a "Direct Project Lead" tone for internal tasks.
* **Multilingual Normalization:** Instantly translates **Arabic** and **Franco-Arab** input into professional English.
* **Smart Formatting:**
    * Detects image URLs and renders them as banners.
    * Converts raw links into descriptive hyperlinks.
    * Strips transient logistics (dates/rooms) to keep content evergreen.
* **Brand Consistency:** Enforces the "All Star" voice and signature (*"Reach for the stars! 🌟"*).

---

## 🛠️ Tech Stack

* **Framework:** Django & Django REST Framework (DRF)
* **AI Model:** Google Gemini Pro
* **Language:** Python 3.10+
* **Format:** JSON / Markdown

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/chat-md.git](https://github.com/YOUR_USERNAME/chat-md.git)
cd chat-md
```
### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
This project requires sensitive API keys. We have provided a template file.

1. Copy `.env.example` to a new file named `.env`:
   ```bash
   cp .env.example .env
   # Or manually rename the file
   ```

2. Open `.env` and fill in your keys:
   ```ini
   # .env
   DEBUG=True
   DJANGO_SECRET_KEY=your_django_secret_key_here
   GOOGLE_API_KEY=AIzaSy_YOUR_GEMINI_API_KEY_here
   ```

### 5. Run the Server
```bash
python manage.py migrate
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

---

## 🔌 API Reference

### 1. Format Session Description
Generates a high-energy, public-facing summary for the website.

* **Endpoint:** `POST /api/format-description/` (Check your specific URL config)
* **Content-Type:** `application/json`

**Request:**
```json
{
  "text": "We had a workshop about Flutter. Covered Widgets and State. Here is the banner: [https://example.com/flutter.png](https://example.com/flutter.png)"
}
```

**Response:**
```json
{
  "markdown": "## Flutter Workshop: Building Interactive UIs\n\n![Session Banner](https://example.com/flutter.png)\n\nIn this session, we dove deep into..."
}
```

### 2. Format Task Description
Generates an internal, actionable task checklist.

* **Endpoint:** `POST /api/format-task/`
* **Content-Type:** `application/json`

**Request:**
```json
{
  "text": "Fix the login button. It needs to be blue #0055FF and 50px height."
}
```

**Response:**
```json
{
  "markdown": "## Task: Refactor Login Component\n\n### 📋 Requirements\n- [ ] Update button color to **#0055FF**.\n- [ ] Set height to **50px**."
}
```

---

## 📂 Project Architecture

The system follows a **Service-Oriented Architecture** using Django REST Framework:

1.  **View Layer:** Receives the POST request and validates data using Serializers.
2.  **Service Layer:**
    * `PromptService`: Selects the correct "Persona" (Editor vs. Manager) and builds the system prompt.
    * `AIService`: Handles the communication with Google Gemini API.
3.  **Response:** Returns a raw JSON payload containing the Markdown string.

---

## 🛡️ Security

* **Secrets:** All API keys are managed via `.env`. **Never** commit your `.env` file.
* **Validation:** Input is sanitized to prevent prompt injection or empty requests.

---

## 🤝 Contributing

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request
