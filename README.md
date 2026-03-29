# projectAI — AI-Powered Project Planning Assistant

An AI-powered project planning assistant that takes your project idea
and autonomously generates a comprehensive plan using a multi-agent
reflection loop.

## Features
- Multi-agent planning: a Strategist agent drafts a project roadmap,
  a Critic agent reviews and approves it
- Reflection loop: up to 2 planning cycles with critique-based refinement
- Phase modification: modify any phase via natural language chat
- Export to Markdown or .ics calendar file
- Clean web UI served from a single HTML file

## Tech Stack
- Backend: Python, Flask, Flask-CORS
- AI: Groq API (llama-3.3-70b-versatile)
- Frontend: Single-file HTML/CSS/JS

## Setup

1. Clone the repo:
   git clone https://github.com/Hasanthi-Swarna/projectAI

2. Install dependencies:
   pip install -r requirements.txt

3. Set your Groq API key:
   export GROQ_API_KEY=your_key_here

4. Run the app:
   python app.py

5. Open http://localhost:5000 in your browser.

## Usage
- Type your project idea in the chat (e.g. "Build a food delivery app")
- The agents will generate and approve a phased project plan
- Use commands like "modify phase 2" or "add phase for testing"
- Export your plan as Markdown or calendar (.ics)

## Files
- app.py — Flask backend with multi-agent logic
- ai_project_manager_webapp.html — Frontend UI
- requirements.txt — Python dependencies

## Sneak a peek
<img width="1821" height="911" alt="Screenshot from 2026-03-29 18-18-07" src="https://github.com/user-attachments/assets/9f0a1840-8bcd-4405-b9b8-827e8baa9ff7" />
<img width="1821" height="911" alt="Screenshot from 2026-03-29 18-18-34" src="https://github.com/user-attachments/assets/61f7e85f-6934-47b0-ac50-ad50c7309e3f" />
<img width="1821" height="911" alt="Screenshot from 2026-03-29 18-18-41" src="https://github.com/user-attachments/assets/360991b3-0d17-4b99-84ef-6215d07c3244" />
