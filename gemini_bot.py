import google.generativeai as genai
import os
import logging
from dotenv import load_dotenv
import pathlib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GeminiChatbot:
    def __init__(self):
        # Try multiple ways to load the API key 
        self._load_api_key()
        
        if not self.api_key:
            raise ValueError("Gemini API key is not set. Please set the GEMINI_API_KEY environment variable in your .env file.")
        
        # Configure the Gemini API
        try:
            genai.configure(api_key=self.api_key)
            logger.info("Successfully configured the Gemini API")
            
            # Test the API key by making a simple request
            self._test_api_key()
            
            # Set up the model with Gemini 2.0 Flash
            try:
                logger.info("Initializing Gemini 2.0 Flash model")
                
                # Set generation parameters for faster responses
                generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 1024,
                }
                
                # Configure the model with generation parameters
                self.model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash",
                    generation_config=generation_config
                )
                
                # Initialize conversation history
                self.chat_session = self.model.start_chat(history=[])
                
                # Set the context for mental health support
                self._initialize_chat_context()
                logger.info("Successfully initialized Gemini 2.0 Flash model")
                self.model_initialized = True
                
            except Exception as e:
                logger.error(f"Failed to initialize Gemini 2.0 Flash model: {str(e)}")
                self.model_initialized = False
            
        except Exception as e:
            logger.error(f"Error during Gemini configuration: {str(e)}")
            self.model_initialized = False
    
    def _load_api_key(self):
        """Try multiple methods to load the API key"""
        # Method 1: Try loading from .env in the current directory
        current_dir = pathlib.Path(__file__).parent.resolve()
        env_path = current_dir / '.env'
        logger.info(f"Looking for .env file at: {env_path}")
        
        if env_path.exists():
            logger.info(".env file found in the current directory")
            load_dotenv(env_path)
        else:
            # Method 2: Try loading from project root directory
            project_root = current_dir  # Start with current dir
            env_path = project_root / '.env'
            logger.info(f"Looking for .env file at project root: {env_path}")
            
            if env_path.exists():
                logger.info(".env file found in the project root")
                load_dotenv(env_path)
            else:
                logger.warning(".env file not found in specific locations. Trying to load from default locations...")
                # Method 3: Try loading from the default location
                load_dotenv()
            
        # Get the API key from environment variables
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # Log the result (safely)
        if self.api_key:
            key_preview = self.api_key[:5] + '...' + self.api_key[-3:] if len(self.api_key) > 8 else "***"
            logger.info(f"API key found: {key_preview}")
        else:
            logger.error("GEMINI_API_KEY not found in environment variables")
    
    def _test_api_key(self):
        """Make a simple API call to test if the key is valid"""
        try:
            # Create a simple test model
            test_model = genai.GenerativeModel('gemini-2.0-flash')
            # Try a simple completion to test the API key
            response = test_model.generate_content("Say hello")
            logger.info("API key test successful")
            return True
        except Exception as e:
            logger.error(f"API key test failed: {str(e)}")
            raise ValueError(f"Invalid Gemini API key or API connection issue: {str(e)}")
        
    def _initialize_chat_context(self):
        """Initialize the chat with mental health support context"""
        system_prompt = """You are a mental health support chatbot. Your role is to provide empathetic, 
        supportive, and non-judgmental responses to users who may be experiencing stress, anxiety, 
        or other mental health challenges. Avoid giving medical advice or diagnoses. 
        Instead, encourage users to seek professional help if needed. Focus on providing emotional support,
        coping strategies, and mindfulness techniques.Give ypour suggestion in short key point and also use neeccesry emojis."""
        
        try:
            self.chat_session.send_message(system_prompt)
            logger.info("Mental health context initialized for Gemini chatbot")
        except Exception as e:
            logger.error(f"Error initializing Gemini chat context: {str(e)}")
    
    def get_response(self, message):
        """Generate a response using the Gemini API focused on mental health support"""
        try:
            # Check if model is initialized
            if not hasattr(self, 'model_initialized') or not self.model_initialized:
                logger.error("Cannot generate response: Gemini model not initialized")
                return "I'm sorry, but I'm currently having technical difficulties. Please try again later or use another model."
                
            logger.info(f"Sending message to Gemini API: {message}")
            
            # Get response from Gemini
            response = self.chat_session.send_message(message)
            reply = response.text.strip()
            
            logger.info(f"Received response from Gemini API: {reply}")
            return reply
            
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            return "I'm sorry, I couldn't process your request at the moment. Please try again later."
    
    def reset_conversation(self):
        """Reset the conversation history"""
        try:
            # Re-initialize the chat session
            self.chat_session = self.model.start_chat(history=[])
            self._initialize_chat_context()
            return "Conversation has been reset."
        except Exception as e:
            logger.error(f"Error resetting Gemini conversation: {str(e)}")
            return "Failed to reset the conversation."