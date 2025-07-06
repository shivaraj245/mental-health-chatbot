from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np 
import nltk
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer 
from tensorflow.keras.models import load_model
import json
import pickle
import random
import logging 
import os
import traceback
from dotenv import load_dotenv

# Set up logging with more details
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from multiple possible locations
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
if os.path.exists(env_path):
    logger.info(f"Loading environment variables from {env_path}")
    load_dotenv(env_path)
else:
    logger.warning(f"No .env file found at {env_path}, trying default locations")
    load_dotenv()

# Initialize variables for chatbot instances
gemini_bot = None

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5000", "http://localhost:5000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Initialize chatbot
lemmatizer = WordNetLemmatizer()

# Check if required files exist before loading
required_files = ['chatbot_model.h5', 'words.pkl', 'classes.pkl', 'intents.json']
missing_files = [f for f in required_files if not os.path.exists(f)]

if missing_files:
    logger.error(f"Missing required files: {missing_files}")
    logger.info("Please run train_chatbot.py first to generate model files.")
    model = None
    words = []
    classes = []
    intents = {}
else:
    try:
        model = load_model('chatbot_model.h5')
        with open('words.pkl', 'rb') as f:
            words = pickle.load(f)
        with open('classes.pkl', 'rb') as f:
            classes = pickle.load(f)
        with open('intents.json') as f:
            intents = json.load(f)
        logger.info("Successfully loaded all model files")
        
        # Initialize Gemini chatbot with enhanced error handling
        try:
            # Check if Gemini API is installed before trying to import
            import importlib
            if importlib.util.find_spec("google.generativeai") is None:
                logger.error("Google Generative AI package not installed. Install with: pip install google-generativeai")
                raise ImportError("google-generativeai package not installed")
                
            # Verify if Gemini API key is available
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                logger.error("GEMINI_API_KEY not found in environment variables")
                raise ValueError("GEMINI_API_KEY not set in .env file. Please add your Gemini API key.")
                
            # If key exists, try to initialize the Gemini chatbot
            from gemini_bot import GeminiChatbot
            gemini_bot = GeminiChatbot()
            
            # Check if the model was actually initialized successfully
            if not hasattr(gemini_bot, 'model_initialized') or not gemini_bot.model_initialized:
                logger.error("Gemini chatbot failed to initialize model properly")
                gemini_bot = None
            else:
                logger.info("Gemini chatbot initialized successfully")
                
        except ImportError as e:
            logger.error(f"Import error for Gemini: {str(e)}")
            logger.info("To use Gemini, install required package: pip install google-generativeai")
            gemini_bot = None
        except ValueError as e:
            logger.error(f"Gemini API key error: {str(e)}")
            gemini_bot = None
        except Exception as e:
            logger.error(f"Error initializing Gemini chatbot: {str(e)}")
            logger.error(traceback.format_exc())
            gemini_bot = None
            
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        model = None

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_rule_based_response(ints):
    if not ints:
        return "I'm not sure I understand. Could you rephrase that?"
    tag = ints[0]['intent']
    list_of_intents = intents['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "I'm not sure how to respond to that."

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            logger.error("No data received")
            return jsonify({"status": "error", "message": "No data received"}), 400
            
        message = data.get('message')
        chatbot_type = data.get('type', 'rule')  # Default to rule-based if not specified

        logger.info(f"Processing {chatbot_type} request: {message}")

        if not message:
            return jsonify({"status": "error", "message": "No message provided"}), 400

        # Check if requested model is available
        if chatbot_type == 'gemini' and gemini_bot is None:
            logger.error("Gemini model not initialized")
            return jsonify({
                "status": "error",
                "message": "Gemini model not available"
            }), 503

        try:
            if chatbot_type == 'rule':
                ints = predict_class(message)
                response = get_rule_based_response(ints)
                logger.info(f"Rule-based response generated: {response}")
            elif chatbot_type == 'gemini' and gemini_bot is not None:
                response = gemini_bot.get_response(message)
                logger.info(f"Gemini response generated: {response}")
            else:
                response = "The selected model is not available."
                logger.info(f"Selected model not available")

            return jsonify({
                "status": "success",
                "response": response,
                "type": chatbot_type
            })

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return jsonify({
                "status": "error",
                "message": f"Error processing message: {str(e)}"
            }), 500

    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "rule_based_model": "loaded" if model is not None else "not loaded",
        "gemini_model": "loaded" if gemini_bot is not None else "not loaded",
        "words_loaded": len(words),
        "classes_loaded": len(classes)
    })

@app.route('/gemini-chat', methods=['POST'])
def gemini_chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
        
    try:
        if gemini_bot is None:
            return jsonify({'error': 'Gemini model not initialized'}), 503
            
        # Get response from the Gemini chatbot
        response = gemini_bot.get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error in Gemini chat: {str(e)}")
        return jsonify({'response': "I'm sorry, I'm having trouble processing your request right now. Please try again later."})

@app.route('/reset-gemini-chat', methods=['POST'])
def reset_gemini_chat():
    try:
        if gemini_bot is None:
            return jsonify({'error': 'Gemini model not initialized'}), 503
            
        result = gemini_bot.reset_conversation()
        return jsonify({'message': result})
    except Exception as e:
        logger.error(f"Error resetting Gemini chat: {str(e)}")
        return jsonify({'error': 'Failed to reset conversation'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
