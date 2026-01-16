# Mental Health Chatbot - Quick Reference Sheet

**For detailed interview preparation, see [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md)**

---

## 🚀 One-Minute Pitch

> "I built a mental health support chatbot using Flask, TensorFlow, and Google Gemini API. It combines a custom-trained neural network for fast intent classification (40+ mental health categories) with Gemini AI for advanced conversations. The rule-based model achieves 95%+ accuracy with <100ms response time, while Gemini provides context-aware support. Built with Python, it demonstrates full-stack ML development from data preprocessing to deployment."

---

## 🏗️ Architecture at a Glance

```
User Input → Flask API → Model Selection
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
            Rule-Based Model    Gemini API
            (TensorFlow NN)     (Google AI)
                    ↓                   ↓
            Intent → Response   AI Response
                    ↓                   ↓
                    └─────────┬─────────┘
                              ↓
                         User Response
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Flask, Python 3.7+ |
| **ML/AI** | TensorFlow, Keras, Google Gemini |
| **NLP** | NLTK (tokenization, lemmatization) |
| **Frontend** | HTML, CSS, JavaScript |
| **Data** | JSON, Pickle |
| **Deployment** | Gunicorn (recommended) |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Flask app, API endpoints, model loading |
| `train_chatbot.py` | Neural network training script |
| `gemini_bot.py` | Google Gemini API integration |
| `intents.json` | Training data (40+ intent categories) |
| `chatbot_model.h5` | Trained neural network model |
| `words.pkl` | Vocabulary (processed words) |
| `classes.pkl` | Intent class labels |

---

## 🧠 Model Architecture

```
Input: Bag-of-Words Vector (binary, vocab size)
   ↓
Dense(512) + ReLU + Dropout(0.5)
   ↓
Dense(256) + ReLU + Dropout(0.3)
   ↓
Dense(128) + ReLU + Dropout(0.2)
   ↓
Dense(num_classes) + Softmax
   ↓
Output: Intent Probabilities
```

**Training Details:**
- Optimizer: Adam (lr=0.001)
- Loss: Categorical Cross-Entropy
- Early Stopping: Monitors validation accuracy
- Train/Val Split: 80/20
- Epochs: Up to 100 (with early stopping)

---

## 🔄 Data Processing Pipeline

```
User Text: "I feel anxious"
    ↓
1. Tokenization: ["I", "feel", "anxious"]
    ↓
2. Lemmatization: ["i", "feel", "anxious"]
    ↓
3. Bag-of-Words: [0,0,1,0,1,0,...,1,0,0]
    ↓
4. Neural Network Prediction: [0.05, 0.85, 0.02, ...]
    ↓
5. Intent Selection: "anxiety" (85% confidence)
    ↓
6. Response Selection: Random from anxiety responses
    ↓
Output: "Anxiety can feel overwhelming. Try taking slow, deep breaths..."
```

---

## 🎯 Key Features

✅ **Dual AI Models**: Rule-based (fast) + Gemini (intelligent)  
✅ **40+ Mental Health Intents**: Anxiety, depression, stress, self-care, etc.  
✅ **Fast Response**: <100ms for rule-based model  
✅ **Context-Aware**: Gemini maintains conversation history  
✅ **Crisis Detection**: Redirects to professional help  
✅ **Privacy-First**: No user data storage  
✅ **RESTful API**: Clean, documented endpoints  
✅ **Error Handling**: Graceful degradation, logging  

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Training Accuracy** | ~95%+ |
| **Validation Accuracy** | ~90%+ |
| **Response Time (Rule-based)** | <100ms |
| **Response Time (Gemini)** | 2-4 seconds |
| **Model Size** | ~10MB |
| **Memory Usage** | ~500MB (TensorFlow) |
| **Confidence Threshold** | 0.25 (25%) |

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serve chat interface |
| `/chat` | POST | Main chat endpoint (rule/gemini) |
| `/gemini-chat` | POST | Gemini-specific endpoint |
| `/reset-gemini-chat` | POST | Reset conversation history |
| `/health` | GET | System health check |

**Request Format:**
```json
POST /chat
{
  "message": "I feel stressed",
  "type": "rule"  // or "gemini"
}
```

**Response Format:**
```json
{
  "status": "success",
  "response": "Let's try some stress management techniques...",
  "type": "rule"
}
```

---

## ⚙️ Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"

# 3. Train model (first time only)
python train_chatbot.py

# 4. Set up Gemini API key (optional)
echo "GEMINI_API_KEY=your_key_here" > .env

# 5. Run application
python app.py  # Development
# OR
gunicorn app:app  # Production
```

Access at: `http://localhost:5000`

---

## 💡 Demo Script (3 Minutes)

### 1. Introduction (30s)
"Mental health chatbot with dual AI models: custom neural network + Google Gemini"

### 2. Rule-based Demo (1m)
- Type: "Hi" → Greeting
- Type: "I feel anxious" → Anxiety support
- Type: "I'm stressed" → Stress management

### 3. Gemini Demo (30s)
- Type complex query: "I'm overwhelmed with work and can't sleep"
- Show contextual, detailed response

### 4. Code Highlight (1m)
- Show `predict_class()` function
- Show model architecture in `train_chatbot.py`
- Show intent examples in `intents.json`

---

## ❓ Top 5 Interview Questions

### Q1: "Explain how your model works"
**Answer:** "It's a multi-layer neural network that classifies user text into mental health intents. The pipeline: tokenize → lemmatize → bag-of-words → neural network → intent prediction → response selection. The model uses 3 dense layers with dropout for regularization and is trained on 40+ intent categories with corresponding response templates."

### Q2: "Why two models?"
**Answer:** "Trade-offs. Rule-based is fast (<100ms), predictable, cost-free, works offline. Gemini is context-aware, handles complex queries, more natural, but slower and requires API calls. This gives users flexibility and demonstrates understanding of different AI approaches."

### Q3: "How do you prevent overfitting?"
**Answer:** "Multiple strategies: Dropout layers (0.5, 0.3, 0.2), early stopping monitoring validation accuracy, train/validation split (80/20), and regularization through the Adam optimizer. These ensure the model generalizes well to unseen inputs."

### Q4: "How would you improve accuracy?"
**Answer:** "Several approaches: (1) Add more diverse training patterns per intent, (2) Use word embeddings instead of bag-of-words for semantic understanding, (3) Try LSTM/GRU for sequence modeling, (4) Fine-tune BERT on mental health data, (5) Implement active learning to collect and learn from misclassified examples, (6) Add data augmentation."

### Q5: "How would you deploy this?"
**Answer:** "Containerize with Docker, deploy to cloud (AWS/GCP/Azure), use Gunicorn as WSGI server, implement auto-scaling, add Redis caching for common queries, use cloud secret manager for API keys, set up monitoring with CloudWatch/Datadog, implement rate limiting, and ensure HTTPS. For scale, consider Kubernetes orchestration and CDN for static assets."

---

## 🎓 Key Concepts to Explain

### NLP Terms
- **Tokenization**: Splitting text into words
- **Lemmatization**: Reducing words to base form ("running" → "run")
- **Bag-of-Words**: Binary vector representation of text (word present=1, absent=0)

### ML Terms
- **Intent Classification**: Categorizing text into predefined classes
- **Softmax**: Converts logits to probability distribution (output layer)
- **Dropout**: Randomly disables neurons during training to prevent overfitting
- **Early Stopping**: Stops training when validation performance plateaus

### Architecture Terms
- **REST API**: Stateless HTTP interface for client-server communication
- **CORS**: Cross-Origin Resource Sharing for frontend-backend communication
- **WSGI**: Web Server Gateway Interface for production Python apps

---

## 🚨 Common Pitfalls to Avoid

❌ Don't say "It just works" - explain HOW  
❌ Don't claim 100% accuracy - be realistic  
❌ Don't ignore ethical considerations in mental health  
❌ Don't skip error handling discussion  
❌ Don't forget to mention limitations  

✅ Do explain trade-offs and design decisions  
✅ Do acknowledge areas for improvement  
✅ Do emphasize ethical AI and safety features  
✅ Do show enthusiasm and passion  
✅ Do prepare for "How would you scale?" questions  

---

## 🔮 Future Improvements (Brief Mention)

**Short-term**: User feedback, conversation history, mobile-responsive UI  
**Medium-term**: Database integration, multi-language support, analytics  
**Long-term**: BERT fine-tuning, emotion detection, professional integration  

---

## 📈 Project Highlights to Emphasize

1. **Full-Stack ML**: Data prep → Training → Deployment → API
2. **Dual-Model Architecture**: Demonstrates strategic thinking
3. **Real-World Application**: Addresses important social issue
4. **Production-Ready Features**: Error handling, logging, health checks
5. **Scalability Considerations**: Modular design, easy to extend
6. **Ethical AI**: Crisis detection, professional help redirection
7. **Modern Tech Stack**: TensorFlow, Gemini API, Flask

---

## 🎯 Closing Statement

> "This project showcases my ability to build end-to-end ML solutions, from data processing and model training to API development and deployment. It demonstrates understanding of NLP, neural networks, web development, and ethical AI considerations - all applied to a meaningful problem in mental health support."

---

## 📚 Resources

- **Full Guide**: [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md) - Comprehensive preparation
- **Project Code**: All files in repository
- **README**: [README.md](README.md) - Setup and usage instructions

---

**Good luck! Remember: Understand the WHY behind every decision, show enthusiasm, and think about scalability!** 🚀
