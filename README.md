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
