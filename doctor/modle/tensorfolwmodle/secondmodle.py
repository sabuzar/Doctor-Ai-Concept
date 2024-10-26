import pandas as pd
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
import numpy as np
import os



class IncrementalChatbot:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.model = self.create_model()
        self.data = pd.DataFrame(columns=['questions', 'answers'])

    def load_data(self, csv_file):
        if os.path.exists(csv_file):
            self.data = pd.read_csv(csv_file)

    def add_example(self, question, answer):
        self.data = self.data.append({'questions': question, 'answers': answer}, ignore_index=True)

    def train(self):
        self.tokenizer.fit_on_texts(self.data['questions'])
        input_sequences = self.tokenizer.texts_to_sequences(self.data['questions'])
        input_sequences = np.array(pad_sequences(input_sequences, padding='post'))

        self.model.fit(input_sequences, self.data['answers'], epochs=1, verbose=0)

    def create_model(self):
        model = Sequential([
            Embedding(len(self.tokenizer.word_index)+1, 64),
            LSTM(128),
            Dense(len(self.tokenizer.word_index)+1, activation='softmax')
        ])
        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def predict(self, question):
        question_sequence = self.tokenizer.texts_to_sequences([question])
        question_sequence = np.array(pad_sequences(question_sequence, maxlen=20, padding='post'))
        predicted_index = np.argmax(self.model.predict(question_sequence), axis=-1)[0]
        predicted_answer = self.tokenizer.index_word[predicted_index]
        return predicted_answer

    def save_data(self, csv_file):
        self.data.to_csv(csv_file, index=False)

def main():
    chatbot = IncrementalChatbot()
    csv_file = '../sklearnmodel/data.csv'

    # Load existing data
    chatbot.load_data(csv_file)

    print("Welcome to the chatbot! Type 'exit' to quit.")

    while True:
        question = input("You: ")
        if question.lower() == 'exit':
            break

        # Check if the question is already in the data
        if question in chatbot.data['questions'].values:
            answer = chatbot.data.loc[chatbot.data['questions'] == question, 'answers'].values[0]
            print("Doctor:", answer)
        else:
            pass



if __name__ == "__main__":
    main()
