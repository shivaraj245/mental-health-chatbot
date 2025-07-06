import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping  # Add this import
import random
import pickle
from sklearn.model_selection import train_test_split

lemmatizer = WordNetLemmatizer()

# Load intents file 
intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignore_words = ['?', '!']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

print(f"{len(documents)} documents")
print(f"{len(classes)} classes: {classes}")
print(f"{len(words)} unique lemmatized words: {words}")

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    word_patterns = doc[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# Convert training data to numpy arrays
training = np.array(training, dtype=object)

train_x = np.array(list(training[:, 0]), dtype=np.float32)
train_y = np.array(list(training[:, 1]), dtype=np.float32)

# Split data into train/validation sets
train_x, val_x, train_y, val_y = train_test_split(
    train_x, train_y, 
    test_size=0.2, 
    random_state=42
)

# Modify the model architecture
model = Sequential([
    Dense(512, input_shape=(len(train_x[0]),), activation='relu'),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(len(train_y[0]), activation='softmax')
])

# Use Adam optimizer instead of SGD for better convergence
optimizer = Adam(learning_rate=0.001)

# Compile with improved settings
model.compile(
    loss='categorical_crossentropy',
    optimizer=optimizer,
    metrics=['accuracy']
)

# Add validation monitoring
early_stopping = EarlyStopping(
    monitor='val_accuracy',  # Changed to monitor validation accuracy
    patience=15,
    min_delta=0.001,
    restore_best_weights=True,
    verbose=1  # Add verbose to see when early stopping occurs
)

# Train with validation split
history = model.fit(
    train_x, train_y,
    validation_data=(val_x, val_y),
    epochs=100,
    batch_size=16,
    verbose=1,
    callbacks=[early_stopping]
)

# Save the model and history
model.save('chatbot_model.h5')
with open('training_history.pkl', 'wb') as f:
    pickle.dump(history.history, f)

print("Model created and training history saved")
