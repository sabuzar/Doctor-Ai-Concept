import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class QuestionAnswerBot:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = LinearSVC()
        self.data = pd.DataFrame(columns=['questions', 'answers'])
        self.model_file = 'question_answer_bot_model.pkl'

        # Load existing model if available
        if os.path.exists(self.model_file):
            self.load_model()

    def load_model(self):
        self.vectorizer, self.classifier = joblib.load(self.model_file)

    def save_model(self):
        joblib.dump((self.vectorizer, self.classifier), self.model_file)

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

        X = self.vectorizer.fit_transform(self.data['questions'])
        y = self.data['answers']
        self.classifier.fit(X, y)
        self.save_model()
        print("Model trained and saved successfully.")

    def predict(self, question):
        if not os.path.exists(self.model_file):
            self.load_model()
            if not os.path.exists(self.model_file):
                print("Model is not trained yet.")
                return

        X = self.vectorizer.transform([question])
        predicted_answer = self.classifier.predict(X)
        return predicted_answer[0]




question = "how can we find if the patient is suffering"

predicted_answer = QuestionAnswerBot.predict(self=QuestionAnswerBot(),question=question)

print("Predicted Answer:", predicted_answer)

def main():
    bot = QuestionAnswerBot()
    csv_file = 'chapter1.csv'

    # Load existing data
    bot.load_data(csv_file)

    print("Welcome to the Question-Answer Bot!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        # user_input=user_input.upper()
        if user_input.lower() == 'exit':
            break

        if user_input.lower() == 'train':
            bot.train()
            continue

        if user_input.lower() == 'save':
            bot.save_model()
            print("Model saved successfully.")
            continue

        # Check if the question is already in the data
        if user_input in bot.data['questions'].values:
            for i in range(len(bot.data['questions'].values)):
                if bot.data['questions'].values[i] == user_input:
                    answer=bot.data['answers'].values[i]
                    print("Bot:", answer)
                    break
        else:
            def google_search(query):
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)
                driver.get('https://www.google.com')
                search_box = driver.find_element(By.NAME, 'q')
                search_box.send_keys(query)
                search_box.send_keys(Keys.RETURN)
                driver.implicitly_wait(5)
                search_result = driver.find_element(By.CSS_SELECTOR, '#search .g')
                output = search_result.text
                driver.quit()
                return output
            query = user_input
            result = google_search(query)
            print(result)
            if result != None:
                appending_data = [
                    user_input, result
                ]
                storing_file = open('data.csv', 'a', newline="", encoding='utf-8')
                writer = csv.writer(storing_file)
                writer.writerow(appending_data)
                storing_file.close()



    print("Exiting...")
    bot.save_model()

if __name__ == "__main__":
    main()

# # Ask for a new answer and add the question-answer pair to the data
# answer = input("Bot: I'm not sure how to respond to that. Please provide an answer: ")
# appending_data = [
#     user_input, answer
# ]
# storing_file = open('data.csv', 'a', newline="", encoding='utf-8')
# writer = csv.writer(storing_file)
# writer.writerow(appending_data)
# storing_file.close()
# print("Bot: Thanks! I'll remember that.")