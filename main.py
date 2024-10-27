from __future__ import annotations

import streamlit as st
from typing import List, Dict, Optional, TypedDict, Literal, Final, cast, Union
from dataclasses import dataclass, field
from enum import Enum, auto
import logging
from datetime import datetime
import os
from dotenv import load_dotenv
from pocketgroq import GroqProvider
from pocketgroq.autonomous_agent import AutonomousAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Role(Enum):
    """Valid message roles"""
    USER = auto()
    ASSISTANT = auto()
    SYSTEM = auto()

class MessageDict(TypedDict):
    """Type definition for message dictionary"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: float

@dataclass(frozen=True)
class ModelConfig:
    """Model configuration with strict typing"""
    DEFAULT_MODEL: Final[str] = "llama2-70b-4096"
    AVAILABLE_MODELS: Final[List[str]] = field(default_factory=lambda: ["llama2-70b-4096"])
    MAX_MESSAGES: Final[int] = 100
    MAX_RETRIES: Final[int] = 3

class SessionState:
    """Enhanced session state with strict type checking"""
    messages: List[MessageDict]
    available_models: List[str]
    selected_model: str
    model_selectbox: str
    initialized: bool
    api_key: str

    def __init__(self) -> None:
        """Initialize with default values"""
        self.messages = []
        self.available_models = [ModelConfig.DEFAULT_MODEL]
        self.selected_model = ModelConfig.DEFAULT_MODEL
        self.model_selectbox = ModelConfig.DEFAULT_MODEL
        self.initialized = False
        self.api_key = os.getenv('GROQ_API_KEY', '')

class SessionManager:
    """Strict session state manager with enhanced validation"""
    
    @staticmethod
    def _validate_role(role: str) -> Literal["user", "assistant", "system"]:
        """Validate message role"""
        valid_roles: List[Literal["user", "assistant", "system"]] = ["user", "assistant", "system"]
        if role not in valid_roles:
            raise ValueError(f"Invalid role: {role}. Must be one of {valid_roles}")
        return cast(Literal["user", "assistant", "system"], role)

    @staticmethod
    def _validate_content(content: str) -> str:
        """Validate message content"""
        if not isinstance(content, str):
            raise TypeError("Message content must be string")
        if not content.strip():
            raise ValueError("Message content cannot be empty")
        return content.strip()

    @staticmethod
    def initialize() -> None:
        """Initialize session state with type checking"""
        if not hasattr(st.session_state, "session"):
            st.session_state.session = SessionState()
            st.session_state.session.initialized = True

    @staticmethod
    def get_state() -> SessionState:
        """Get current session state with validation"""
        if not hasattr(st.session_state, "session") or not st.session_state.session.initialized:
            SessionManager.initialize()
        return cast(SessionState, st.session_state.session)

    @classmethod
    def append_message(cls, role: str, content: str) -> None:
        """Append message with strict validation"""
        state = cls.get_state()
        
        validated_role = cls._validate_role(role)
        validated_content = cls._validate_content(content)
        
        new_message: MessageDict = {
            "role": validated_role,
            "content": validated_content,
            "timestamp": datetime.now().timestamp()
        }
        
        if len(state.messages) >= ModelConfig.MAX_MESSAGES:
            state.messages.pop(0)
        
        state.messages.append(new_message)

    @classmethod
    def update_models(cls, models: List[str]) -> None:
        """Update available models with validation"""
        state = cls.get_state()
        
        if not isinstance(models, list) or not all(isinstance(m, str) for m in models):
            raise TypeError("Models must be a list of strings")
            
        if not models:
            logger.warning("Empty model list provided, keeping current models")
            return
            
        state.available_models = models
        
        if state.selected_model not in models:
            state.selected_model = models[0]
            state.model_selectbox = models[0]

    @classmethod
    def set_selected_model(cls, model: str) -> None:
        """Update selected model with validation"""
        state = cls.get_state()
        
        if not isinstance(model, str):
            raise TypeError("Model must be a string")
            
        if model not in state.available_models:
            raise ValueError(f"Model {model} not in available models")
            
        state.selected_model = model
        state.model_selectbox = model

class UI:
    """UI component manager"""
    
    @staticmethod
    def setup_page_config() -> None:
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Apple ][e Chat",
            page_icon="🍎",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    @staticmethod
    def load_css() -> None:
        """Load custom CSS styles"""
        try:
            with open('.streamlit/style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            logger.warning("Style.css not found")

    @staticmethod
    def render_title() -> None:
        """Render application title"""
        st.markdown("""
            <div style='text-align: center; font-family: "Courier New", monospace; color: #33FF33; margin-bottom: 2rem;'>
                <h1 style='text-shadow: 0 0 5px #33FF33;'>
                    APPLE ][ e CHAT INTERFACE
                </h1>
                <p style='color: #33FF33;'>
                    ]READY
                    <span class='blink'>_</span>
                </p>
            </div>
        """, unsafe_allow_html=True)

def setup_ui() -> None:
    """Setup UI components with state management"""
    state = SessionManager.get_state()
    
    if state.available_models:
        try:
            current_index = state.available_models.index(state.selected_model)
        except ValueError:
            current_index = 0
            
        selected = st.selectbox(
            "Select a model:",
            state.available_models,
            index=current_index,
            key="temp_model_select"
        )
        
        if selected != state.selected_model:
            SessionManager.set_selected_model(selected)

def handle_chat(prompt: str, use_cot: bool) -> None:
    """Handle chat interaction with state management"""
    try:
        SessionManager.append_message("user", prompt)
        
        with st.chat_message("user"):
            st.write(prompt)
            
        with st.chat_message("assistant"):
            if use_cot:
                st.write("Processing with chain of thought...")
                
            state = SessionManager.get_state()
            groq = GroqProvider(state.api_key)
            response = groq.generate(prompt, temperature=0, model=state.selected_model)
            
            st.write(response)
            SessionManager.append_message("assistant", response)
            
    except Exception as e:
        logger.error(f"Chat handling error: {str(e)}")
        st.error(f"Error processing message: {str(e)}")

def main() -> None:
    """Main application with enhanced error handling"""
    try:
        load_dotenv()
        UI.setup_page_config()
        UI.load_css()
        UI.render_title()
        
        SessionManager.initialize()
        state = SessionManager.get_state()
        
        api_key: str = st.text_input("Enter your Groq API Key:", type="password")
        if api_key:
            state.api_key = api_key
            groq = GroqProvider(api_key)
            setup_ui()
        
        st.write(f"Current model: {state.selected_model}")
        
        use_cot: bool = st.checkbox("Use Chain of Thought")
        
        for message in state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        if prompt := st.chat_input("What would you like to know?"):
            handle_chat(prompt, use_cot)
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An unexpected error occurred. Please refresh the page.")

if __name__ == "__main__":
    main()