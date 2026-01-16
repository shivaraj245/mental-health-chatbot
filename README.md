# Mental Health ChatBot Project Overview

This project is a mental health chatbot designed to provide supportive responses to users' mental health concerns. The application uses NLP (Natural Language Processing) techniques to understand user inputs and generate appropriate responses.

## 📚 Interview Preparation

**Preparing for an interview?** Check out the comprehensive [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md) which includes:
- Complete technical explanations of all components
- Common interview questions with detailed answers
- Demo script and presentation tips
- Deep dive into ML/NLP concepts used
- Architecture diagrams and code walkthroughs
- Future improvements and scalability discussions

## Project Architecture

The chatbot consists of two AI components:

1. **Rule-based model**: A neural network trained on predefined intents
2. **Gemini model**: An integration with Google's Gemini AI for more advanced responses

## Prerequisites

- Python 3.7 or higher
- Gemini API key from Google AI Studio
- Internet connection for Gemini API calls
- At least 2GB RAM for TensorFlow model loading

## Technical Stack

- **Backend**: Python, Flask
- **AI/ML**: TensorFlow, Keras, NLTK, Google Generative AI (Gemini)
- **Frontend**: HTML, CSS, JavaScript
- **Development tools**: Logging, Environment variables (dotenv)
- **Data Processing**: NumPy, Pandas, Scikit-learn
## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/shivaraj245/mental-health-chatbot.git
cd mental-health-chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
```

### 5. Train the Model (First Time Setup)
```bash
python train_chatbot.py
```


## Usage

### Training the Model
```bash
python train_chatbot.py
```
This will:
- Process the intents.json file
- Train a neural network model
- Save model files for inference

### Running the Application
```bash
python app.py
```

### Accessing the Interface
1. Open your browser to `http://localhost:5000`
2. Choose between Rule-based or Gemini AI model
3. Start chatting with the mental health support bot

## Key Components

### 1. Backend (Flask Application)

The [app.py](app.py) file is the core of the application, implementing:

- Flask web server with CORS support for cross-origin requests
- Rule-based chatbot using a TensorFlow/Keras model
- Gemini AI integration for more sophisticated responses
- Health check endpoint to monitor system status

### 2. Data and Model

- [intents.json](intents.json): Contains training data with patterns (user inputs) and responses grouped by intent tags
- Neural network model: Trained model saved as [chatbot_model.h5](chatbot_model.h5)
- Supporting files: [words.pkl](words.pkl) and [classes.pkl](classes.pkl) for NLP processing

### 3. Frontend

- HTML/CSS/JS: User interface with chat functionality
- Supports communication with both rule-based and Gemini models

## Working Flow

### Initial Setup

1. The application loads environment variables (especially Gemini API key)
2. It checks for required model files (chatbot_model.h5, words.pkl, classes.pkl, intents.json)
3. Initializes the rule-based model and Gemini chatbot (if possible)

### Request Processing Flow

1. User sends a message through the frontend interface
2. Request reaches Flask server via /chat endpoint
3. Message processing:
   - For rule-based model:
     - Text is tokenized and lemmatized
     - Converted to bag-of-words representation
     - Neural network predicts the intent
     - A response is selected from matching intent
   - For Gemini model:
     - Message is sent to Gemini API
     - Response is received and returned

### Endpoints

- `/`: Serves the main chat interface
- `/chat`: Main endpoint handling chat requests with model selection
- `/gemini-chat`: Dedicated endpoint for Gemini model responses
- `/reset-gemini-chat`: Resets Gemini conversation context
- `/health`: Status endpoint for system monitoring

## Configuration

### Environment Variables
Create a `.env` file in the project root with:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Model Training Configuration
The neural network uses:
- **Architecture**: Dense layers (512 → 256 → 128 neurons)
- **Optimizer**: Adam with learning rate 0.001
- **Early stopping**: Monitors validation accuracy
- **Dropout**: 0.5, 0.3, 0.2 for regularization

### Intent Categories
Current mental health support categories in [intents.json](intents.json):
- Greetings and general conversation
- Anxiety and stress management
- Depression support
- Coping strategies
- Mindfulness techniques
- Crisis support

## Performance Notes

- **Rule-based model**: Fast response (~100-400ms)
- **Gemini model**: Slower response (~2-4 seconds, depends on API)
- **Model accuracy**: Depends on training data quality in intents.json
- **Memory usage**: ~500MB for TensorFlow model loading

## Error Handling

The application includes comprehensive error handling:

- Missing files detection
- API key validation
- Exception handling with detailed logging
- Appropriate HTTP error codes for different failures

## Development and Training

### Adding New Intents
1. Define intents in [intents.json](intents.json)
2. Add patterns (user inputs) and responses
3. Run [train_chatbot.py](train_chatbot.py) to retrain the model
4. Restart the application with `python app.py`

### Model Improvement
- Add more diverse training patterns
- Include edge cases and variations
- Monitor training accuracy and validation loss
- Adjust model architecture if needed


**Note**: This application is for educational and support purposes only. It is not a substitute for professional mental health care. If you're experiencing a mental health crisis, please contact a mental health professional or crisis helpline immediately.

The application provides a dual-model approach, with the rule-based model handling common patterns and the Gemini model providing more advanced, context-aware responses for mental health support.