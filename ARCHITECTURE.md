# System Architecture & Flow Diagrams

This document provides visual representations of the Mental Health Chatbot architecture and data flows.

---

## 1. High-Level System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                           USER LAYER                              │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              Web Browser (Chat Interface)                  │   │
│  │  • HTML/CSS/JavaScript                                     │   │
│  │  • Model Selection (Rule-based / Gemini)                   │   │
│  │  • Real-time Chat Display                                  │   │
│  └─────────────────────────┬─────────────────────────────────┘   │
└────────────────────────────┼──────────────────────────────────────┘
                             │ HTTP POST/GET
                             │ (JSON)
┌────────────────────────────▼──────────────────────────────────────┐
│                      APPLICATION LAYER (Flask)                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                            │  │
│  │  • GET  /          → Serve chat interface                  │  │
│  │  • POST /chat      → Process user messages                 │  │
│  │  • POST /gemini-chat → Gemini-specific endpoint            │  │
│  │  • POST /reset-gemini-chat → Reset conversation            │  │
│  │  • GET  /health    → System health check                   │  │
│  └─────────────────────────┬──────────────────────────────────┘  │
│                             │                                      │
│  ┌─────────────────────────▼──────────────────────────────────┐  │
│  │              Request Processing & Routing                   │  │
│  │  • Parse JSON request body                                  │  │
│  │  • Extract message and model type                           │  │
│  │  • Validate input                                           │  │
│  │  • Route to appropriate model                               │  │
│  │  • Error handling & logging                                 │  │
│  └─────────────────────────┬──────────────────────────────────┘  │
│                             │                                      │
│              ┌──────────────┴──────────────┐                      │
│              │                              │                      │
│              ▼                              ▼                      │
│  ┌───────────────────────┐    ┌───────────────────────────────┐  │
│  │   Rule-Based Model    │    │      Gemini AI Model          │  │
│  │   Processing          │    │      Integration              │  │
│  └───────────────────────┘    └───────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
             │                              │
             │                              │ API Call
             ▼                              ▼
┌───────────────────────┐    ┌──────────────────────────────────┐
│   MODEL/DATA LAYER    │    │   EXTERNAL SERVICE LAYER         │
│  • chatbot_model.h5   │    │  ┌───────────────────────────┐   │
│  • words.pkl          │    │  │   Google Gemini API       │   │
│  • classes.pkl        │    │  │   (Gemini 2.0 Flash)      │   │
│  • intents.json       │    │  │   • Context-aware         │   │
│  • training_history   │    │  │   • Conversation history  │   │
└───────────────────────┘    │  └───────────────────────────┘   │
                              └──────────────────────────────────┘
```

---

## 2. Rule-Based Model Processing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Input: "I feel anxious"                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Tokenization (NLTK word_tokenize)                       │
│  Input:  "I feel anxious"                                        │
│  Output: ["I", "feel", "anxious"]                                │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Lemmatization (WordNetLemmatizer)                       │
│  Input:  ["I", "feel", "anxious"]                                │
│  Process: Convert each word to base form                         │
│  Output: ["i", "feel", "anxious"]                                │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Bag-of-Words Encoding                                   │
│  Vocabulary: ["a", "and", "anxious", "calm", "feel", "happy",   │
│               "i", "sad", "stressed", ...]                       │
│  Encoding:   [0,    0,     1,        0,      1,      0,          │
│               1,    0,     0,        ...]                        │
│  Vector Length: len(vocabulary)                                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Neural Network Prediction                               │
│                                                                   │
│  Input Layer: [0, 0, 1, 0, 1, 0, 1, 0, 0, ...]                   │
│       ↓                                                           │
│  Dense(512) + ReLU + Dropout(0.5)                                │
│       ↓                                                           │
│  Dense(256) + ReLU + Dropout(0.3)                                │
│       ↓                                                           │
│  Dense(128) + ReLU + Dropout(0.2)                                │
│       ↓                                                           │
│  Dense(num_classes) + Softmax                                    │
│       ↓                                                           │
│  Output: [0.02, 0.01, 0.85, 0.03, 0.01, ...]                    │
│           ↑            ↑                                          │
│         greeting    anxiety (85% confidence)                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Filter by Confidence Threshold (0.25)                   │
│  Results: [                                                       │
│    {"intent": "anxiety", "probability": "0.85"},                 │
│    {"intent": "stress", "probability": "0.28"}                   │
│  ]                                                                │
│  Best Match: "anxiety"                                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: Retrieve Intent from intents.json                       │
│  {                                                                │
│    "tag": "anxiety",                                              │
│    "patterns": ["I feel anxious", "I can't stop worrying", ...], │
│    "responses": [                                                 │
│      "Anxiety can feel overwhelming. Try taking slow breaths...",│
│      "You're safe right now. Name 5 things you can see...",      │
│      "Would it help to talk about what's making you anxious?"    │
│    ]                                                              │
│  }                                                                │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 7: Random Response Selection                               │
│  Randomly select one response from the matched intent            │
│  Output: "Anxiety can feel overwhelming. Try taking slow, deep   │
│          breaths—inhale for 4 seconds, hold for 4, exhale for 6"│
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 8: Return JSON Response                                    │
│  {                                                                │
│    "status": "success",                                           │
│    "response": "Anxiety can feel overwhelming...",                │
│    "type": "rule"                                                 │
│  }                                                                │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
              Display in Chat Interface
```

---

## 3. Gemini AI Processing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  User Input: "I'm overwhelmed with work and can't sleep.         │
│               What should I do?"                                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Initialize Gemini Chatbot (if not already)              │
│  • Load API key from environment variable                        │
│  • Configure Gemini API                                          │
│  • Test API key validity                                         │
│  • Create GenerativeModel instance (gemini-2.0-flash)            │
│  • Set generation parameters:                                    │
│    - temperature: 0.7                                             │
│    - top_p: 0.95                                                  │
│    - top_k: 40                                                    │
│    - max_output_tokens: 1024                                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Start Chat Session with Context                         │
│  System Prompt: "You are a mental health support chatbot. Your   │
│  role is to provide empathetic, supportive, and non-judgmental   │
│  responses to users who may be experiencing stress, anxiety, or  │
│  other mental health challenges. Avoid giving medical advice or  │
│  diagnoses. Instead, encourage users to seek professional help   │
│  if needed. Focus on providing emotional support, coping         │
│  strategies, and mindfulness techniques. Give your suggestion    │
│  in short key points and also use necessary emojis."             │
│                                                                   │
│  Conversation History: [previous messages if any]                │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Send User Message to Gemini API                         │
│  Request:                                                         │
│  • User message: "I'm overwhelmed with work and can't sleep..."  │
│  • Context: Mental health support                                │
│  • History: Previous conversation (if any)                       │
│                                                                   │
│  API Call: chat_session.send_message(user_message)               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Gemini API Processing (External)                        │
│  • Language understanding                                        │
│  • Context analysis                                              │
│  • Emotion detection                                             │
│  • Response generation (using large language model)              │
│  • Safety filtering                                              │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Receive AI-Generated Response                           │
│  Response Text:                                                   │
│  "I understand you're feeling overwhelmed. Here are some steps:  │
│                                                                   │
│  🌙 For Sleep:                                                    │
│  • Try progressive muscle relaxation before bed                  │
│  • Avoid screens 1 hour before sleep                             │
│  • Keep a notepad by your bed to write down worries              │
│                                                                   │
│  💼 For Work Overwhelm:                                           │
│  • Break tasks into smaller, manageable chunks                   │
│  • Prioritize what's truly urgent vs. important                  │
│  • Take short breaks every hour (5-10 minutes)                   │
│                                                                   │
│  🧘 Immediate Relief:                                             │
│  • Practice 4-7-8 breathing (inhale 4s, hold 7s, exhale 8s)     │
│  • Try a 5-minute guided meditation                              │
│                                                                   │
│  If this persists, consider talking to a mental health           │
│  professional. You don't have to handle this alone. 💙"          │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: Post-Processing                                         │
│  • Strip whitespace                                              │
│  • Log response                                                  │
│  • Update conversation history (for context in next message)     │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 7: Return JSON Response                                    │
│  {                                                                │
│    "status": "success",                                           │
│    "response": "I understand you're feeling overwhelmed...",      │
│    "type": "gemini"                                               │
│  }                                                                │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
              Display in Chat Interface
```

---

## 4. Training Process Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Load Training Data (intents.json)                       │
│  {                                                                │
│    "intents": [                                                   │
│      {"tag": "greeting", "patterns": [...], "responses": [...]}, │
│      {"tag": "anxiety", "patterns": [...], "responses": [...]},  │
│      ...                                                          │
│    ]                                                              │
│  }                                                                │
│  Total Intents: 40+                                               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Preprocess Text Data                                    │
│  For each pattern in each intent:                                │
│  • Tokenize: "I feel sad" → ["I", "feel", "sad"]                │
│  • Lemmatize: ["I", "feel", "sad"] → ["i", "feel", "sad"]       │
│  • Build vocabulary (all unique words)                           │
│  • Build classes (all intent tags)                               │
│  • Create documents: (word_list, tag)                            │
│                                                                   │
│  Output:                                                          │
│  • words: Sorted list of unique lemmatized words                 │
│  • classes: Sorted list of intent tags                           │
│  • documents: List of (word_list, tag) tuples                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Create Training Data                                    │
│  For each document:                                               │
│  • Create bag-of-words: binary vector (1 if word in pattern)    │
│  • Create output: one-hot encoded intent tag                     │
│                                                                   │
│  Example:                                                         │
│  Pattern: "I feel anxious"                                       │
│  BoW:     [0, 0, 1, 0, 1, 0, 1, 0, ...]  (len=vocabulary_size)  │
│  Output:  [0, 0, 1, 0, ...]               (len=num_intents)     │
│           ↑                                                       │
│      anxiety intent                                               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Split Data (80% Train, 20% Validation)                  │
│  Using sklearn.train_test_split                                  │
│  • train_x: Training features (BoW vectors)                      │
│  • train_y: Training labels (one-hot encoded intents)            │
│  • val_x:   Validation features                                  │
│  • val_y:   Validation labels                                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Build Neural Network Model                              │
│                                                                   │
│  Input Layer: shape=(vocabulary_size,)                           │
│      ↓                                                            │
│  Dense(512, activation='relu')                                   │
│      ↓                                                            │
│  Dropout(0.5)  ← Regularization                                  │
│      ↓                                                            │
│  Dense(256, activation='relu')                                   │
│      ↓                                                            │
│  Dropout(0.3)                                                    │
│      ↓                                                            │
│  Dense(128, activation='relu')                                   │
│      ↓                                                            │
│  Dropout(0.2)                                                    │
│      ↓                                                            │
│  Output Layer: Dense(num_intents, activation='softmax')          │
│                                                                   │
│  Compile:                                                         │
│  • Optimizer: Adam(learning_rate=0.001)                          │
│  • Loss: categorical_crossentropy                                │
│  • Metrics: accuracy                                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: Train Model with Early Stopping                         │
│  Callbacks:                                                       │
│  • EarlyStopping(monitor='val_accuracy',                         │
│                  patience=15,                                     │
│                  restore_best_weights=True)                       │
│                                                                   │
│  Training Loop (up to 100 epochs):                               │
│  Epoch 1: train_acc=0.45, val_acc=0.43                           │
│  Epoch 2: train_acc=0.67, val_acc=0.65                           │
│  Epoch 3: train_acc=0.82, val_acc=0.79                           │
│  ...                                                              │
│  Epoch 25: train_acc=0.96, val_acc=0.91                          │
│  Epoch 26: train_acc=0.97, val_acc=0.91 (no improvement)         │
│  ...                                                              │
│  Epoch 40: val_acc plateaus → EARLY STOP                         │
│                                                                   │
│  Best Model: Epoch 25 (val_acc=0.91)                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 7: Save Model and Artifacts                                │
│  • chatbot_model.h5     → Trained neural network                 │
│  • words.pkl            → Vocabulary list                         │
│  • classes.pkl          → Intent class list                       │
│  • training_history.pkl → Training metrics                        │
│                                                                   │
│  Model Size: ~10MB                                                │
│  Training Time: ~2-5 minutes (CPU)                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  Request Received at /chat                                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  Validate Request                                                 │
│  • Check if JSON data present → If No → 400 Error                │
│  • Check if 'message' in data → If No → 400 Error                │
│  • Check model type valid    → If No → Default to 'rule'         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  Check Model Availability                                         │
│  If type='gemini':                                                │
│    • Is gemini_bot initialized? → If No → 503 Error              │
│  If type='rule':                                                  │
│    • Is model loaded? → If No → 500 Error                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  Process Message                                                  │
│  Try:                                                             │
│    • Predict intent / Call Gemini API                            │
│    • Generate response                                           │
│  Except:                                                          │
│    • Log error details                                           │
│    • Return 500 error with message                               │
│    • Don't expose internal details to user                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  Low Confidence Handling (Rule-based only)                        │
│  If max_confidence < 0.25:                                        │
│    • Return fallback response:                                   │
│      "I'm not sure I understand. Could you rephrase that?"       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  Return Success Response                                          │
│  {                                                                │
│    "status": "success",                                           │
│    "response": "...",                                             │
│    "type": "rule" or "gemini"                                     │
│  }                                                                │
└─────────────────────────────────────────────────────────────────┘

Error Code Reference:
• 400 Bad Request: Invalid input data
• 500 Internal Server Error: Model processing failure
• 503 Service Unavailable: Requested model not available
```

---

## 6. Deployment Architecture (Production)

```
┌─────────────────────────────────────────────────────────────────┐
│                          INTERNET                                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTPS
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LOAD BALANCER (AWS ALB)                        │
│  • SSL/TLS Termination                                            │
│  • Health Checks                                                  │
│  • Request Distribution                                           │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Instance 1 │  │   Instance 2 │  │   Instance 3 │
│ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │
│ │ Gunicorn │ │  │ │ Gunicorn │ │  │ │ Gunicorn │ │
│ │  Flask   │ │  │ │  Flask   │ │  │ │  Flask   │ │
│ │   App    │ │  │ │   App    │ │  │ │   App    │ │
│ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │
│ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │
│ │  Model   │ │  │ │  Model   │ │  │ │  Model   │ │
│ │  Cache   │ │  │ │  Cache   │ │  │ │  Cache   │ │
│ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
┌─────────────┐  ┌──────────────┐  ┌────────────────┐
│   Redis     │  │   Database   │  │  Gemini API    │
│   Cache     │  │  (Optional)  │  │  (External)    │
│             │  │              │  │                │
│ • Responses │  │ • User Data  │  │ • AI Model     │
│ • Sessions  │  │ • Analytics  │  │ • Generation   │
└─────────────┘  └──────────────┘  └────────────────┘
       │                 │
       └─────────┬───────┘
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING & LOGGING                           │
│  • CloudWatch / Datadog                                           │
│  • Error Tracking (Sentry)                                        │
│  • Performance Metrics                                            │
│  • Log Aggregation (ELK Stack)                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Model Decision Tree

```
                User Sends Message
                        │
                        ▼
              ┌─────────────────┐
              │ Which Model to  │
              │     Use?        │
              └────────┬────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌──────────────┐              ┌──────────────┐
│  Rule-Based  │              │    Gemini    │
│    Model     │              │      AI      │
└──────┬───────┘              └──────┬───────┘
       │                             │
       ▼                             ▼
Simple/Common Query?          Complex/Novel Query?
Fast Response Needed?         Context Matters?
Offline Mode?                 Natural Conversation?
       │                             │
       ▼                             ▼
┌──────────────┐              ┌──────────────┐
│ Tokenize &   │              │  Send to     │
│ Lemmatize    │              │ Gemini API   │
└──────┬───────┘              └──────┬───────┘
       │                             │
       ▼                             ▼
┌──────────────┐              ┌──────────────┐
│ Bag-of-Words │              │ AI Generated │
│  Encoding    │              │   Response   │
└──────┬───────┘              └──────┬───────┘
       │                             │
       ▼                             │
┌──────────────┐                     │
│   Neural     │                     │
│   Network    │                     │
│  Prediction  │                     │
└──────┬───────┘                     │
       │                             │
       ▼                             │
┌──────────────┐                     │
│ Confidence   │                     │
│   Check      │                     │
│  (>= 0.25?)  │                     │
└──────┬───────┘                     │
       │                             │
   ┌───┴───┐                         │
   │       │                         │
  Yes     No                         │
   │       │                         │
   │       ▼                         │
   │  ┌──────────┐                  │
   │  │ Fallback │                  │
   │  │ Response │                  │
   │  └────┬─────┘                  │
   │       │                         │
   └───────┴─────────────────────────┘
           │
           ▼
    Return Response to User
```

---

## 8. Data Format Examples

### Input Request
```json
POST /chat HTTP/1.1
Content-Type: application/json

{
  "message": "I'm feeling stressed about work",
  "type": "rule"
}
```

### Success Response
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "response": "Stress can be overwhelming. Try some deep breathing exercises or meditation to help calm your mind.",
  "type": "rule"
}
```

### Error Response (Model Not Available)
```json
HTTP/1.1 503 Service Unavailable
Content-Type: application/json

{
  "status": "error",
  "message": "Gemini model not available"
}
```

### Health Check Response
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "online",
  "rule_based_model": "loaded",
  "gemini_model": "loaded",
  "words_loaded": 856,
  "classes_loaded": 42
}
```

---

## Summary

This architecture demonstrates:
- **Modular Design**: Clear separation of concerns
- **Dual-Model Strategy**: Flexibility and redundancy
- **Scalability**: Horizontal scaling capability
- **Error Resilience**: Multiple layers of error handling
- **Production-Ready**: Health checks, logging, monitoring considerations

For detailed code explanations, see [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md)  
For quick reference, see [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
