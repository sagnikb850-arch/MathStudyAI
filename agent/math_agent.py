"""
AI Agent for Math Study - Handles queries using LangChain
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict, Any, List
import json
from config.settings import (
    OPENAI_API_KEY, MODEL_NAME, AI_MODEL, MAX_TOKENS, TEMPERATURE
)


class MathTutorAgent:
    """
    AI Agent for teaching mathematics to students
    Uses LangChain with OpenAI GPT-4 or alternative models
    """
    
    SYSTEM_PROMPT = """You are an expert mathematics tutor AI assistant designed to help students learn and understand mathematical concepts. Your role is to:

1. **Explain Concepts**: Break down complex mathematical topics into simple, understandable steps
2. **Solve Problems**: Walk through problem-solving step-by-step, explaining the reasoning
3. **Provide Resources**: Suggest relevant learning resources from the provided list
4. **Encourage Learning**: Be supportive and encouraging, adapting to the student's level
5. **Check Understanding**: Ask clarifying questions to ensure the student understands

Your teaching approach:
- Start with the fundamentals if the student seems confused
- Use real-world examples when possible
- Show multiple ways to solve problems
- Identify common mistakes and help students avoid them
- Encourage students to try solving problems themselves
- Adapt your explanation complexity based on their responses

When answering:
- Be clear and concise
- Use mathematical notation properly
- Break complex problems into manageable steps
- Suggest relevant resources from the available list
- Always verify understanding with follow-up questions

Available Topics: Calculus, Linear Algebra, Algebra, Geometry, Trigonometry, Statistics, Probability, Pre-Calculus, Discrete Math, Number Theory

If a student asks about a topic not in your knowledge base or available resources, acknowledge this and suggest they explore broader resources or textbooks.
"""
    
    def __init__(self, resources_context: str = ""):
        """
        Initialize the Math Tutor Agent
        
        Args:
            resources_context: Available resources as formatted string
        """
        self.resources_context = resources_context
        self.chat_history: List[Dict[str, str]] = []
        self.llm = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the LangChain LLM for tutoring"""
        try:
            # Initialize LLM
            if AI_MODEL == 'openai':
                self.llm = ChatOpenAI(
                    api_key=OPENAI_API_KEY,
                    model_name=MODEL_NAME,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS
                )
            else:
                # Fallback to OpenAI if other models not configured
                print("Warning: Using OpenAI as default. Configure other models in settings.")
                self.llm = ChatOpenAI(
                    api_key=OPENAI_API_KEY,
                    model_name="gpt-3.5-turbo",
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS
                )
            
            print("Math Tutor Agent initialized successfully")
        
        except Exception as e:
            print(f"Error initializing agent: {e}")
            raise
    
    def _create_tools(self) -> List:
        """
        Create helper methods for the tutor (not actively used in current implementation)
        These are here for future extensibility
        
        Returns:
            Empty list (tools not needed for current LLM-based approach)
        """
        return []
    
    def _explain_concept(self, concept: str) -> str:
        """Helper method to explain a mathematical concept"""
        return f"I'll explain the concept of {concept} in detail, breaking it down into understandable parts."
    
    def _solve_problem(self, problem: str) -> str:
        """Helper method to solve a mathematical problem"""
        return f"I'll solve this problem step-by-step: {problem}"
    
    def _find_resources(self, topic: str) -> str:
        """Helper method to find resources"""
        if self.resources_context:
            return f"Here are resources for {topic}:\n{self.resources_context}"
        return f"No resources found for {topic}. Please check available resources."
    
    def _check_understanding(self, topic: str) -> str:
        """Helper method to check understanding"""
        return f"Let me verify your understanding of {topic}. Can you explain it back to me with an example?"
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process a user query and return the tutor's response
        
        Args:
            user_query: The student's question or request
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Build the full prompt with system instructions and context
            system_prompt = self.SYSTEM_PROMPT
            resources_context = self.resources_context if self.resources_context else "No specific resources available"
            
            full_prompt = f"""{system_prompt}

Available Resources:
{resources_context}

Student Question: {user_query}

Tutor (provide a detailed, step-by-step explanation):"""
            
            # Get response from LLM
            message = HumanMessage(content=full_prompt)
            response = self.llm.invoke([message])
            
            # Store in chat history
            self.chat_history.append({"role": "user", "content": user_query})
            self.chat_history.append({"role": "assistant", "content": response.content})
            
            return {
                "success": True,
                "response": response.content,
                "query": user_query,
                "model": MODEL_NAME,
                "chat_history": self.chat_history
            }
        
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "success": False,
                "response": f"I encountered an error processing your question: {str(e)}",
                "query": user_query,
                "error": str(e)
            }
    
    def process_query_simple(self, user_query: str) -> Dict[str, Any]:
        """
        Process a user query using the same LLM response
        
        Args:
            user_query: The student's question
            
        Returns:
            Dictionary with response
        """
        try:
            system_prompt = self.SYSTEM_PROMPT
            resources_context = self.resources_context if self.resources_context else "No specific resources available"
            
            full_prompt = f"""{system_prompt}

Available Resources:
{resources_context}

Student: {user_query}

Tutor:"""
            
            # Get response from LLM
            message = HumanMessage(content=full_prompt)
            response = self.llm.invoke([message])
            
            return {
                "success": True,
                "response": response.content,
                "query": user_query,
                "model": MODEL_NAME
            }
        
        except Exception as e:
            print(f"Error: {e}")
            return {
                "success": False,
                "response": f"Error: {str(e)}",
                "query": user_query
            }
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.chat_history = []
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the current chat history"""
        return self.chat_history


def create_agent_with_resources(resources_context: str) -> MathTutorAgent:
    """
    Factory function to create a Math Tutor Agent with resources
    
    Args:
        resources_context: The available resources as string
        
    Returns:
        Initialized MathTutorAgent instance
    """
    agent = MathTutorAgent(resources_context=resources_context)
    return agent
