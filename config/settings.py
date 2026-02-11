"""
Configuration settings for Math Study AI Application
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Flask Settings
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# AI Model Settings
# Options: 'openai', 'claude', 'ollama', 'google'
AI_MODEL = os.getenv('AI_MODEL', 'openai')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', '')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')

# Model Configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4-turbo-preview')  # For OpenAI
# MODEL_NAME = 'claude-3-opus-20240229'  # For Claude
# MODEL_NAME = 'llama2'  # For Ollama

# Data Settings
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
WEBSITES_FILE = os.path.join(DATA_DIR, 'math_websites.xlsx')
CONTEXT_SHEET = 'Websites'  # Sheet name in XLSX

# Agent Settings
AGENT_TYPE = 'react'  # Options: 'react', 'zero-shot-react', 'conversational'
MAX_TOKENS = 2048
TEMPERATURE = 0.7
TOP_P = 0.9
