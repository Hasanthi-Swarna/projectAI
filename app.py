"""
AI Project Manager - Flask Backend
Integrates the web UI with Groq-powered multi-agent system
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from groq import Groq
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIProjectManager")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Groq client
GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'YOUR_API_KEY_HERE')
client = Groq(api_key=GROQ_API_KEY)

# Project Memory (Session Management)
class ProjectMemory:
    def __init__(self, user_idea: str):
        self.user_idea = user_idea
        self.project_plan = {}
        self.critique_history = []
        self.conversation_history = []
        
    def update_plan(self, new_plan: Dict):
        self.project_plan = new_plan
        
    def add_critique(self, critique: str):
        self.critique_history.append(critique)
        
    def add_message(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})

# Store active sessions
sessions = {}

# Agent Engine
def run_agent(agent_name: str, system_prompt: str, user_prompt: str, model="llama-3.3-70b-versatile"):
    """Run a Groq-powered agent"""
    logger.info(f"🤖 Agent {agent_name} is thinking...")
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Agent {agent_name} error: {e}")
        return None

# Multi-Agent Workflow
def run_strategist_loop(memory: ProjectMemory, max_loops=2):
    """
    Implements the reflection loop: Strategist creates plan, Critic reviews it
    """
    strategist_prompt = """
    You are a Lead Technical Architect and Project Manager.
    Create a high-level project roadmap in JSON format based on the user's idea.
    
    The JSON must have:
    - "project_name": string (creative, professional name)
    - "phases": array of objects with {name, duration_days, description}
    
    Make it realistic, detailed, and professional.
    IMPORTANT: Return ONLY valid JSON, no markdown, no explanations.
    """
    
    critic_prompt = """
    You are a Senior Engineering Critic.
    Review the project plan JSON for:
    1. Realistic timelines
    2. Missing critical steps (testing, deployment, etc.)
    3. Proper sequencing
    
    If GOOD: Reply exactly "APPROVE"
    If BAD: Reply "REJECT: [specific reason]"
    """
    
    for attempt in range(max_loops):
        logger.info(f"Planning cycle {attempt + 1}/{max_loops}")
        
        # Strategist creates plan
        feedback = memory.critique_history[-1] if memory.critique_history else "First draft"
        plan_text = run_agent(
            "Strategist",
            strategist_prompt,
            f"User Idea: {memory.user_idea}\n\nPrevious Feedback: {feedback}"
        )
        
        if not plan_text:
            continue
            
        # Clean JSON
        clean_json = plan_text.replace("```json", "").replace("```", "").strip()
        
        # Critic reviews
        critique = run_agent(
            "Critic",
            critic_prompt,
            f"Review this plan:\n{clean_json}"
        )
        
        if critique and "APPROVE" in critique.upper():
            try:
                plan = json.loads(clean_json)
                memory.update_plan(plan)
                return {"success": True, "plan": plan, "critique": critique}
            except json.JSONDecodeError:
                memory.add_critique("JSON was invalid. Please fix format.")
                continue
        else:
            memory.add_critique(critique if critique else "Plan needs improvement")
    
    # Return last attempt
    try:
        plan = json.loads(clean_json)
        memory.update_plan(plan)
        return {"success": True, "plan": plan, "critique": "Approved after refinement"}
    except:
        return {"success": False, "error": "Failed to generate valid plan"}

# API Routes
@app.route('/')
def index():
    """Serve the web interface"""
    with open('ai_project_manager_webapp.html', 'r') as f:
        return f.read()

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and process with agents"""
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # Create or get session
    if session_id not in sessions:
        sessions[session_id] = ProjectMemory(message)
    
    memory = sessions[session_id]
    memory.add_message('user', message)
    
    # Detect intent
    if 'modify' in message.lower() or 'change' in message.lower():
        return handle_modification(memory, message)
    elif 'add phase' in message.lower():
        return handle_add_phase(memory, message)
    else:
        # New project planning
        result = run_strategist_loop(memory)
        
        if result['success']:
            # Add dates to phases
            plan = result['plan']
            add_dates_to_plan(plan)
            
            return jsonify({
                'success': True,
                'plan': plan,
                'critique': result['critique'],
                'message': 'Plan created and approved!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create plan. Please try again.'
            })

@app.route('/api/modify-phase', methods=['POST'])
def modify_phase():
    """Modify a specific phase"""
    data = request.json
    session_id = data.get('session_id', 'default')
    phase_index = data.get('phase_index')
    modifications = data.get('modifications')
    
    if session_id not in sessions:
        return jsonify({'success': False, 'message': 'No active project'})
    
    memory = sessions[session_id]
    plan = memory.project_plan
    
    if phase_index < len(plan.get('phases', [])):
        # Update phase with modifications
        plan['phases'][phase_index].update(modifications)
        memory.update_plan(plan)
        
        return jsonify({
            'success': True,
            'plan': plan,
            'message': f"Phase {phase_index + 1} updated successfully!"
        })
    
    return jsonify({'success': False, 'message': 'Invalid phase index'})

@app.route('/api/export-plan', methods=['POST'])
def export_plan():
    """Export plan as Markdown"""
    data = request.json
    session_id = data.get('session_id', 'default')
    
    if session_id not in sessions:
        return jsonify({'success': False, 'message': 'No active project'})
    
    memory = sessions[session_id]
    plan = memory.project_plan
    
    markdown = generate_markdown(plan)
    
    return jsonify({
        'success': True,
        'markdown': markdown,
        'filename': f"{plan.get('project_name', 'project')}_plan.md"
    })

@app.route('/api/export-calendar', methods=['POST'])
def export_calendar():
    """Export calendar as ICS"""
    data = request.json
    session_id = data.get('session_id', 'default')
    
    if session_id not in sessions:
        return jsonify({'success': False, 'message': 'No active project'})
    
    memory = sessions[session_id]
    plan = memory.project_plan
    
    ics = generate_ics(plan)
    
    return jsonify({
        'success': True,
        'ics': ics,
        'filename': f"{plan.get('project_name', 'project')}_timeline.ics"
    })

# Helper Functions
def handle_modification(memory: ProjectMemory, message: str):
    """Handle phase modification requests"""
    # Use LLM to understand modification intent
    prompt = f"""
    User wants to modify their project plan. Their message: "{message}"
    Current plan: {json.dumps(memory.project_plan)}
    
    Extract:
    1. Which phase to modify (number or name)
    2. What to change
    
    Return JSON: {{"phase_index": 0, "modifications": {{"duration_days": 10}}}}
    """
    
    response = run_agent("ModificationAgent", "You extract modification requests.", prompt)
    
    try:
        mod_data = json.loads(response.replace("```json", "").replace("```", "").strip())
        phase_index = mod_data.get('phase_index', 0)
        
        if phase_index < len(memory.project_plan.get('phases', [])):
            memory.project_plan['phases'][phase_index].update(mod_data.get('modifications', {}))
            
        return jsonify({
            'success': True,
            'plan': memory.project_plan,
            'message': 'Modifications applied!'
        })
    except:
        return jsonify({
            'success': False,
            'message': 'Could not understand modification request. Please be more specific.'
        })

def handle_add_phase(memory: ProjectMemory, message: str):
    """Handle adding new phases"""
    prompt = f"""
    User wants to add a phase to their project. Message: "{message}"
    
    Create a new phase with:
    - name: string
    - duration_days: number
    - description: string
    
    Return ONLY JSON.
    """
    
    response = run_agent("PhaseCreator", "You create project phases.", prompt)
    
    try:
        new_phase = json.loads(response.replace("```json", "").replace("```", "").strip())
        memory.project_plan.get('phases', []).append(new_phase)
        
        return jsonify({
            'success': True,
            'plan': memory.project_plan,
            'message': 'New phase added!'
        })
    except:
        return jsonify({
            'success': False,
            'message': 'Could not create new phase. Please provide: name, duration, description'
        })

def add_dates_to_plan(plan: Dict):
    """Add start dates to each phase"""
    current_date = datetime.now()
    
    for phase in plan.get('phases', []):
        phase['start_date'] = current_date.strftime('%b %d, %Y')
        current_date += timedelta(days=phase.get('duration_days', 7))

def generate_markdown(plan: Dict) -> str:
    """Generate Markdown documentation"""
    md = f"# {plan.get('project_name', 'Project Plan')}\n\n"
    md += f"**Generated:** {datetime.now().strftime('%B %d, %Y')}\n\n"
    md += f"## Overview\n{plan.get('user_idea', 'N/A')}\n\n"
    md += f"## Project Timeline\n\n"
    
    for i, phase in enumerate(plan.get('phases', []), 1):
        md += f"### Phase {i}: {phase.get('name')}\n"
        md += f"- **Start Date:** {phase.get('start_date', 'TBD')}\n"
        md += f"- **Duration:** {phase.get('duration_days')} days\n"
        md += f"- **Description:** {phase.get('description')}\n\n"
    
    return md

def generate_ics(plan: Dict) -> str:
    """Generate ICS calendar file"""
    ics = "BEGIN:VCALENDAR\n"
    ics += "VERSION:2.0\n"
    ics += "PRODID:-//AI Project Manager//EN\n"
    
    for phase in plan.get('phases', []):
        ics += "BEGIN:VEVENT\n"
        ics += f"SUMMARY:{phase.get('name')}\n"
        
        # Convert date
        date_str = phase.get('start_date', datetime.now().strftime('%b %d, %Y'))
        date_obj = datetime.strptime(date_str, '%b %d, %Y')
        ics += f"DTSTART;VALUE=DATE:{date_obj.strftime('%Y%m%d')}\n"
        ics += f"DESCRIPTION:{phase.get('description')}\n"
        ics += "END:VEVENT\n"
    
    ics += "END:VCALENDAR"
    return ics

if __name__ == '__main__':
    print("🚀 Starting AI Project Manager Server...")
    print("📡 Server running at: http://localhost:5000")
    print("🔑 Make sure GROQ_API_KEY is set in environment")
    app.run(debug=True, host='0.0.0.0', port=5000)
