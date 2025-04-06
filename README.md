# 🏥 AI Health Assistant Chatbot

A **Flask-based web application** that uses **Google Gemini (Generative AI)** and **Hugging Face FLAN-T5** to:

- 🩺 Answer medical queries in a structured and easy-to-understand format.
- 🧑‍⚕️ Generate personalized health and wellness recommendations based on user inputs.

---
![image](https://github.com/user-attachments/assets/ec6da17b-43b4-409d-9cad-e1feb058b928)

## 🚀 Features

### 🩺 Medical Chatbot
- Answers health-related queries with:
  - Brief explanation of the condition
  - Remedies and treatments
  - When to seek medical attention
- Powered by **Google Gemini Pro 1.5**

### 🧘 Health Recommendation Generator
- Generates a personalized health plan using:
  - Age, height, weight, activity level, conditions, and goals
- Provides:
  - BMI calculation and interpretation
  - Diet and exercise plans
  - Lifestyle improvement suggestions

### 🔁 Alternate Model Option
- Utilizes **Hugging Face FLAN-T5** for medical Q&A when Gemini is unavailable or for local testing.

---

## 🧰 Tech Stack

| Component        | Description                                |
|------------------|--------------------------------------------|
| **Backend**      | Flask (Python)                             |
| **Frontend**     | HTML, CSS, JavaScript                      |
| **AI APIs**      | Google Gemini Pro, Hugging Face FLAN-T5    |
| **Env Mgmt**     | python-dotenv for API key management       |

---


---

## ⚙️ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-health-assistant.git
cd ai-health-assistant
```
```
pip install -r requirements.txt
```
#### create '.env' 
```
GOOGLE_API_KEY=your_google_gemini_api_key
```
### Run the FLask App
```
python app.py
```
