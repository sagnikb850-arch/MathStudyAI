"""
Flask Backend API for Math Study AI Application
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import HOST, PORT, DEBUG, WEBSITES_FILE
from backend.data_handler import MathResourcesManager, create_sample_excel
from agent.math_agent import MathTutorAgent, create_agent_with_resources

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables
resources_manager = None
math_agent = None


def initialize_app():
    """Initialize the application components"""
    global resources_manager, math_agent
    
    try:
        # Initialize resources manager
        if not os.path.exists(WEBSITES_FILE):
            print(f"Creating sample XLSX file at {WEBSITES_FILE}")
            os.makedirs(os.path.dirname(WEBSITES_FILE), exist_ok=True)
            sample_df = create_sample_excel()
            sample_df.to_excel(WEBSITES_FILE, sheet_name='Websites', index=False)
        
        resources_manager = MathResourcesManager(WEBSITES_FILE)
        
        # Get resources context
        resources_context = resources_manager.get_resources_as_context()
        
        # Initialize AI Agent
        math_agent = create_agent_with_resources(resources_context)
        
        print("Application initialized successfully")
    
    except Exception as e:
        print(f"Error initializing app: {e}")
        raise


# Routes
@app.route('/', methods=['GET'])
def home():
    """Serve the frontend HTML"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
        return send_from_directory(frontend_path, 'index.html')
    except Exception as e:
        return jsonify({
            "error": "Frontend not found",
            "message": str(e)
        }), 404


@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    """Serve static files (CSS, JS, etc)"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
        return send_from_directory(frontend_path, filename)
    except Exception as e:
        return jsonify({
            "error": f"File not found: {filename}",
            "message": str(e)
        }), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route('/api/resources', methods=['GET'])
def get_resources():
    """Get all available resources"""
    try:
        resources = resources_manager.get_all_resources()
        return jsonify({
            "success": True,
            "count": len(resources),
            "resources": resources
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/resources/search', methods=['POST'])
def search_resources():
    """Search for resources by topic or keyword"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Query parameter required"
            }), 400
        
        resources = resources_manager.search_resources(query)
        
        return jsonify({
            "success": True,
            "query": query,
            "count": len(resources),
            "resources": resources
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle student queries - Main interaction endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "Message field required"
            }), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Empty message"
            }), 400
        
        # Process the query with the AI agent
        response = math_agent.process_query_simple(user_message)
        
        return jsonify({
            "success": response.get('success', False),
            "message": response.get('response', ''),
            "query": response.get('query', ''),
            "model": response.get('model', ''),
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@app.route('/api/explain', methods=['POST'])
def explain_concept():
    """Dedicated endpoint for concept explanations"""
    try:
        data = request.get_json()
        concept = data.get('concept', '')
        
        if not concept:
            return jsonify({
                "success": False,
                "error": "Concept field required"
            }), 400
        
        prompt = f"Please explain the mathematical concept of '{concept}' in simple terms, with examples."
        response = math_agent.process_query_simple(prompt)
        
        return jsonify({
            "success": response.get('success', False),
            "concept": concept,
            "explanation": response.get('response', ''),
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/solve', methods=['POST'])
def solve_problem():
    """Dedicated endpoint for solving problems"""
    try:
        data = request.get_json()
        problem = data.get('problem', '')
        
        if not problem:
            return jsonify({
                "success": False,
                "error": "Problem field required"
            }), 400
        
        prompt = f"Please solve this math problem step-by-step: {problem}\n\nExplain each step clearly."
        response = math_agent.process_query_simple(prompt)
        
        return jsonify({
            "success": response.get('success', False),
            "problem": problem,
            "solution": response.get('response', ''),
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/resources/<topic>', methods=['GET'])
def get_resources_for_topic(topic):
    """Get resources for a specific topic"""
    try:
        resources = resources_manager.get_resources_for_topic(topic)
        
        return jsonify({
            "success": True,
            "topic": topic,
            "count": len(resources),
            "resources": resources
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/chat/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation history"""
    try:
        math_agent.reset_conversation()
        return jsonify({
            "success": True,
            "message": "Conversation reset successfully"
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


# Initialize app on startup (for production servers like Gunicorn)
try:
    initialize_app()
except Exception as e:
    print(f"Warning during app initialization: {e}")

if __name__ == '__main__':
    try:
        # Initialize app components
        initialize_app()
        
        # Run Flask server
        print(f"Starting Math Study AI Server on {HOST}:{PORT}")
        
        # Use debug mode only in development
        is_production = os.getenv('FLASK_ENV') == 'production'
        app.run(host=HOST, port=PORT, debug=(not is_production))
    
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)
