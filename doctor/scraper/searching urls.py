import pandas as pd
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
data=pd.read_csv('urls.csv')
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
appending_data = [
    'text'
]
storing_file = open(f'text.csv', 'a', newline="", encoding ="utf-8")
writer = csv.writer(storing_file)
writer.writerow(appending_data)
storing_file.close()
x=[]
for test in range(0,len(data)):
    urls=data['urls'][test]
    x.append(urls)


#pageContent_dvexcerpt
#pageContent_dvexcerpt
for search in x:
    driver.get(search)

    try:
        time.sleep(2)
        data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'pageContent_dvexcerpt')))
        text = data.text
        time.sleep(5)
        print(text)
        appending_data = [
            text
        ]
        storing_file = open(f'text.csv', 'a', newline="", encoding="utf-8")
        writer = csv.writer(storing_file)
        writer.writerow(appending_data)
        storing_file.close()


    except:
        print('Failed')