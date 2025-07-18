# 🧠 My AI Twin — Conversational Portfolio Assistant
[🟢 **Live Demo on Hugging Face**](https://huggingface.co/spaces/rrajaram/My-Professional-AI-Twin)

This app is a conversational AI chatbot that acts as **my digital twin**. It's designed to interact with potential employers or clients on my behalf, answering questions about my **career background**, **projects**, **skills**, and **experience** — *before a formal interview is even scheduled.*

The goal is to **save time** for both sides: the employer gets quick clarity about whether I'm a fit, and I receive only genuinely relevant inquiries.

Built with **Gradio**, it provides a smooth web interface that mimics a professional assistant powered by AI.

Visit the site https://huggingface.co/spaces/rrajaram/My-Professional-AI-Twin
---

## 🚀 Key Features

### 🤖 AI-Powered Chatbot (OpenAI SDK)
- Answers user questions using a system prompt seeded with my **Resume (PDF)** and custom **summary**.
- Uses `gpt-4o-mini` for cost-effective, high-quality responses.

### 💼 Career-focused
- specifically designed to handle professional inquiries


### 🛠️ Function Tools
Defines **custom tools** that are registered using `@function_tool` decorators and used by the agent during conversation:

- `validate_email(text: str)`:  
  Validates whether a given email string is in a valid format.

 - `record_email(text: str)`:  
  Sends a **push notification** via Pushover when a valid email is shared, enabling me to quickly follow up.
  
- `record_question(question: str)`:  
  Logs questions the AI cannot answer — helping me identify gaps or update my portfolio.

### 🛡️ Input Guardrail
To prevent spam or abuse, the app uses an **input guardrail**:

- `guardrail_against_spam_email`:  
  Tracks whether an email has already been recorded in the **session**. If so:
  - Blocks further attempts to register emails.
  - Sends a **friendly fallback message** encouraging users to continue the chat with other questions.

⚠️ **Note:**  
Input guardrails typically run **once** before the agent kicks off.  
However, in this app, the agent is **re-instantiated for every incoming message**, making the input guardrail run **on every turn** — this design is intentional and aligns with the guardrail's intended lifecycle.


### 🤝 Professional Boundaries

- Doesn't share personal contact information
- Redirects contact requests to LinkedIn
- Maintains professional tone throughout conversations

### 🔒 Security & Privacy

- Environment variables keep sensitive data secure
- Email validation prevents malformed submissions
- No personal information (phone, address) is shared
- Professional boundaries are maintained

---

## 🎛️ Gradio User Interface

The app includes a **Gradio-based UI** for real-time chat:

- Simple and intuitive layout
- Maintains session context
- Works in local dev or can be deployed to Hugging Face Spaces or a cloud server

---


## 📦 Tech Stack

| Layer         | Technology                     |
| ------------- | ------------------------------ |
| LLM           | OpenAI (gpt-4o-mini)           |
| PDF Parsing   | `pypdf`                        |
| Notifications | Pushover API                   |
| Guardrails    | `@input_guardrail` decorator   |
| Tools         | `@function_tool` API           |
| Framework     | OpenAI Agent SDK   |
| Deployment    | Flexible (HuggingFace)|

---

## 📋 Prerequisites

Python 3.8+
OpenAI API key
Pushover account (for notifications)
Resume PDF export
Personal summary text file

---

## 🛠️ Installation

- Clone the repository
  bash
  
  git clone <your-repo-url>
  cd my-ai-twin

- Install dependencies
  bash
  
  pip install -r requirements.txt

- Set up environment variables Create a .env file in the root directory:
  
  env
  
  OPENAI_API_KEY=your_openai_api_key
  PUSHOVER_TOKEN=your_pushover_token
  PUSHOVER_USER=your_pushover_user_key
  LINKEDIN_URL=your_linkedin_profile_url

- Prepare your data

  Create an uploads/ directory
  Export your resume as PDF and save as uploads/resume.pdf

---

📁 Project Structure
digital-twin-chatbot/
├── main.py              # Main application entry point
├── openaiagent.py       # Core chatbot logic and agent configuration
├── uploads/
│   ├── resume.pdf       # Your resume export
│   ├── summary.txt      # Your handwritten summary
├── .env                 # Environment variables (not in repo)
├── requirements.txt     # Python dependencies
└── README.md            # This file

---

## 🔧 Dependencies
All required dependencies are listed in the requirements.txt file included in the repository.

---

## 🚀 Usage

- Start the application
  bash
  
  uv run main.py

- Access the interface

  - Open your browser and go to http://localhost:7860
  - Start chatting with your digital twin

  
- Example Chat flow

    User: I'd like to hire you for a freelance AI project.
    AI: That's exciting! Could you tell me a bit more about your project?
    Feel free to leave your email so I can reach out.

    User: john@example.com
    AI: Thanks! I've recorded your email and will reach out soon.
    In the meantime, do you have any questions about my background?

    User: Actually, what projects have you done with CrewAI?
    AI: [Provides summary based on PDF]
    
- Monitor interactions

  - Email addresses and unanswered questions are sent to your Pushover notifications
  - Review these regularly to improve your chatbot's responses

---
  
## 🚧 Future Improvements

- Add support for email verification beyond regex (e.g. via mailbox ping).
- Rate limiting or abuse detection.
- Add scheduling integration for meetings

---

## 🤝 Contact

Want to build something similar or hire me for an AI project?

👉 [Connect with me on LinkedIn](https://www.linkedin.com/in/ramya-rajaram-tech/)  
