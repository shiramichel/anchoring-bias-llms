from typing import Dict, List
import requests
import json
import sys

class OpenRouterLLM:
    """Custom LangChain-compatible LLM for OpenRouter"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
    
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate response using OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",  # Streamlit default
            "X-Title": "Dual-Mode Research Assistant"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        except requests.exceptions.RequestException as e:
            return f"I'm having trouble connecting right now. Please try again."
        except (KeyError, IndexError) as e:
            return f"Sorry, I encountered an error processing your request."
        except Exception as e:
            return f"Something went wrong. Please try again."
        

class ChatbotMode:
    """Enhanced chatbot mode with LangChain conversation management"""
    
    def __init__(self, llm: OpenRouterLLM):
        self.llm = llm
        self.history = []

    def format_conversation_context(self) -> List[Dict[str, str]]:
        """Format conversation history for LLM"""
        messages = [
            {
                "role": "system",
                "content": """You are a helpful, knowledgeable assistant engaged in a natural conversation. 
                Maintain context from previous messages and provide thoughtful, relevant responses. 
                Be conversational but informative."""
            }
        ]
        
        # Add conversation history
        for msg in self.history:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        return messages
    
    def generate_response(self, history: List[Dict[str, str]], prompt: str) -> str:
        """Generate contextual response using conversation history"""

        # Keep only last 20 messages to manage context length
        
        if len(history) > 20:
            self.history = history[-20:]
        else:
            self.history = history
        # Format context for LLM
        messages = self.format_conversation_context()

        try:
            # Generate response
            response = self.llm.generate_response(messages)
            
            return response
        
        except Exception as e:
            error_msg = "Sorry, I encountered an error. Please try again."
            self.add_to_memory('assistant', error_msg)
            return error_msg