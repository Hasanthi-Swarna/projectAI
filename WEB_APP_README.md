# 🚀 AI Project Manager - Interactive Web Application

## ✨ New Features

Your AI Project Manager is now a **beautiful, interactive web application** with:

✅ **Chat-based Interface** - Natural conversation with AI agents
✅ **Real-time Planning** - Watch agents strategize and critique in real-time  
✅ **Clean, Professional Output** - Organized project plans with dates
✅ **Modification Support** - Edit phases, add tasks, adjust timelines
✅ **Export Functionality** - Download plans as Markdown or Calendar files
✅ **Multi-Agent Visualization** - See Strategist and Critic agents work together
✅ **Stunning UI** - Modern, futuristic design with smooth animations

---

## 📦 What's Included

```
ai-project-manager-webapp/
├── app.py                          # Flask backend with Groq integration
├── ai_project_manager_webapp.html  # Beautiful frontend UI
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🛠️ Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-CORS (for API access)
- Groq (AI agent engine)
- python-dotenv (environment management)

### Step 2: Set Your Groq API Key

**Option A: Environment Variable (Recommended)**
```bash
export GROQ_API_KEY='gsk_your_key_here'
```

**Option B: Edit app.py**
Open `app.py` and replace line 19:
```python
GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'your-groq-api-key-here')
```

### Step 3: Run the Server

```bash
python app.py
```

You should see:
```
🚀 Starting AI Project Manager Server...
📡 Server running at: http://localhost:5000
🔑 Make sure GROQ_API_KEY is set in environment
```

### Step 4: Open in Browser

Navigate to: **http://localhost:5000**

---

## 🎯 How to Use

### 1️⃣ **Describe Your Project**

In the chat interface, describe your project idea:

**Examples:**
- "Build a mobile fitness tracking app with social features"
- "Create an e-commerce website with payment integration"
- "Develop a task management tool for remote teams"

### 2️⃣ **Watch the Agents Work**

The system will:
1. **Strategist Agent** creates a comprehensive project plan
2. **Critic Agent** reviews for completeness and realism  
3. **Final Plan** appears in the right panel with:
   - Project name
   - Timeline with dates
   - Detailed phases
   - Duration estimates

### 3️⃣ **Modify Your Plan**

You can:
- **Modify phases**: "Change Phase 2 duration to 15 days"
- **Add phases**: "Add a marketing phase after development"
- **Ask questions**: "Why is testing so short?"
- **Refine details**: "Add more detail to the deployment phase"

### 4️⃣ **Export Your Plan**

Click the buttons to:
- 📥 **Export Plan** - Download as Markdown (.md)
- 📅 **Export Calendar** - Download as ICS file (import to Google Calendar)

---

## 🎨 UI Features

### Chat Interface
- Natural conversation with AI agents
- Real-time agent status updates
- Clean message bubbles
- Loading animations

### Results Panel
- **Project Overview** with approval badges
- **Timeline View** with start dates
- **Phase Cards** with hover effects
- **Action Buttons** for modifications

### Design Highlights
- 🌌 Animated cyberpunk background
- 🎨 Gradient accents (green/cyan/pink)
- ✨ Smooth animations and transitions
- 📱 Fully responsive design

---

## 🔧 API Endpoints

The Flask backend exposes these REST APIs:

### POST /api/chat
**Description**: Process chat messages and generate plans  
**Request**:
```json
{
  "message": "Build a social media app",
  "session_id": "user123"
}
```

**Response**:
```json
{
  "success": true,
  "plan": {
    "project_name": "Social Media App",
    "phases": [...]
  },
  "critique": "Plan approved!",
  "message": "Plan created and approved!"
}
```

### POST /api/modify-phase
**Description**: Modify a specific project phase  
**Request**:
```json
{
  "session_id": "user123",
  "phase_index": 2,
  "modifications": {
    "duration_days": 14,
    "description": "Updated description"
  }
}
```

### POST /api/export-plan
**Description**: Export plan as Markdown  
**Returns**: Markdown content and filename

### POST /api/export-calendar
**Description**: Export timeline as ICS calendar  
**Returns**: ICS file content

---

## 🤖 Multi-Agent System

### Strategist Agent
- Creates initial project roadmap
- Defines phases, timelines, descriptions
- Generates realistic estimates

### Critic Agent
- Reviews plans for completeness
- Checks timeline realism
- Ensures critical phases aren't missing
- Provides constructive feedback

### Modification Agent
- Understands natural language changes
- Applies updates to existing plans
- Maintains plan consistency

---

## 📊 Example Output

### Project Plan Card:
```
📋 E-Commerce Website

🎯 Project Overview
Build an online store with payment processing and inventory management

✓ Approved by Critic Agent
📊 5 Phases
⏳ 50 Days Total

🗓️ Project Timeline

Phase 1: Planning & Requirements
📅 Mar 18, 2026 | ⏱️ 7 days
Define project scope, gather requirements...

Phase 2: Design & Architecture
📅 Mar 25, 2026 | ⏱️ 10 days
Create system architecture, database schema...

[More phases...]
```

---

## 💡 Pro Tips

### 1. **Be Specific**
Instead of: "Build a website"  
Try: "Build a recipe-sharing website with user profiles and ratings"

### 2. **Iterate and Refine**
After getting initial plan:
- Ask for more detail on specific phases
- Request timeline adjustments
- Add missing phases

### 3. **Use Export Features**
- Export to Markdown for documentation
- Import calendar to track milestones
- Share plans with stakeholders

### 4. **Modify Freely**
The system supports:
- Natural language modifications
- Adding/removing phases
- Adjusting timelines
- Updating descriptions

---

## 🔥 Advanced Features

### Session Management
Each user gets their own session:
- Plans persist during conversation
- Full modification history
- Conversation context maintained

### Smart Modifications
The system understands:
- "Make phase 3 longer" → Increases duration
- "Add testing before deployment" → Inserts new phase
- "Swap phases 2 and 3" → Reorders phases

### Calendar Integration
Generated ICS files include:
- All phases as events
- Proper date sequencing
- Full descriptions
- Import into any calendar app

---

## 🐛 Troubleshooting

### "No active project" error
**Solution**: Start a new conversation by describing a project

### Agents not responding
**Check**:
1. Groq API key is set correctly
2. Internet connection is active
3. Check Flask console for errors

### Export not working
**Solution**: Make sure you've generated a plan first

### UI not loading
**Check**:
1. Flask server is running (`python app.py`)
2. Navigate to `http://localhost:5000` (not file://)
3. Check browser console for errors

---

## 🚀 Deployment Options

### Local Development
```bash
python app.py
# Access at http://localhost:5000
```

### Production Deployment

**Option 1: Heroku**
```bash
# Add Procfile
web: gunicorn app:app

# Deploy
heroku create your-app-name
git push heroku main
```

**Option 2: Render/Railway**
1. Connect GitHub repo
2. Set `GROQ_API_KEY` environment variable
3. Auto-deploys on push

**Option 3: Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## 📈 Future Enhancements

Ideas for extending the app:

- [ ] User authentication
- [ ] Save multiple projects
- [ ] Team collaboration features
- [ ] Gantt chart visualization
- [ ] Resource allocation
- [ ] Budget estimation
- [ ] Risk assessment
- [ ] Integration with Jira/Asana
- [ ] PDF export
- [ ] Email notifications

---

## 🎓 How It Works

### Frontend → Backend Flow

1. **User types message** → Chat interface
2. **POST to /api/chat** → Flask backend
3. **Groq API calls** → Strategist & Critic agents
4. **Plan generation** → JSON structure
5. **Response to frontend** → Displayed in UI
6. **User modifies** → New API call
7. **Plan updated** → Displayed in UI

### Multi-Agent Architecture

```
User Input
    ↓
Strategist Agent (Groq)
    ↓
Project Plan JSON
    ↓
Critic Agent (Groq)
    ↓
Feedback Loop (if rejected)
    ↓
Final Approved Plan
    ↓
Beautiful UI Display
```

---

## 🎉 You're Ready!

Your AI Project Manager web app is now:
- ✅ Fully functional
- ✅ Beautiful and modern
- ✅ Interactive and conversational
- ✅ Exportable and shareable
- ✅ Modifiable and flexible

**Start planning amazing projects!** 🚀

---

## 📞 Support

Need help?
1. Check this README
2. Review Flask console logs
3. Test with simple project first
4. Verify Groq API key is valid

---

**Built with ❤️ using Flask, Groq, and modern web technologies**
