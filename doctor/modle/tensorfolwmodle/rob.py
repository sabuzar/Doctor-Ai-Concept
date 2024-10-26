import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics.pairwise import cosine_similarity
import joblib

class QuestionAnswerBot:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.data = pd.DataFrame(columns=['questions', 'answers'])
        self.model = None
        self.model_file = 'question_answer_bot_model.h5'

        # Load existing model if available
        if os.path.exists(self.model_file):
            self.load_model()

    def load_model(self):
        self.model = tf.keras.models.load_model(self.model_file)

    def save_model(self):
        self.model.save(self.model_file)

    def load_data(self, csv_file):
        if not os.path.exists(csv_file):
            return
        self.data = pd.read_csv(csv_file)

    def add_example(self, question, answer):
        self.data = self.data.append({'questions': question, 'answers': answer}, ignore_index=True)

    def train(self):
        if len(self.data) == 0:
            print("No data to train the model.")
            return

        self.tokenizer.fit_on_texts(self.data['questions'])
        X = self.tokenizer.texts_to_sequences(self.data['questions'])
        X = pad_sequences(X, padding='post')
        y = self.tokenizer.texts_to_sequences(self.data['answers'])
        y = pad_sequences(y, padding='post')

        input_shape = X.shape[1]
        output_shape = y.shape[1]

        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=len(self.tokenizer.word_index) + 1, output_dim=64, input_length=input_shape),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(output_shape, activation='softmax')
        ])

        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(X, y, epochs=10)

        self.save_model()

    def predict(self, question):
        if self.model is None:
            print("Model is not trained yet.")
            return

        X = self.tokenizer.texts_to_sequences([question])
        X = pad_sequences(X, padding='post', maxlen=X.shape[1])
        prediction = self.model.predict(X)
        predicted_answer_sequence = np.argmax(prediction, axis=-1)
        predicted_answer = self.tokenizer.sequences_to_texts([predicted_answer_sequence])[0]
        return predicted_answer

def main():
    bot = QuestionAnswerBot()
    csv_file = 'text.csv'

    # Load existing data
    bot.load_data(csv_file)

    print("Welcome to the Question-Answer Bot!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        if user_input.lower() == 'train':
            bot.train()
            continue

        # Get the predicted answer
        answer = bot.predict(user_input)
        if answer:
            print("Bot:", answer)
        else:
            print("Bot: I'm sorry, I don't have an answer to that question.")

    print("Exiting...")

if __name__ == "__main__":
    main()
