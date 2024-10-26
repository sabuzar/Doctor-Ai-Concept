import pandas as pd
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get('https://accessmedicine.mhmedical.com/book.aspx?bookid=3095&isMissingChapter=true#259856986')

appending_data = [
    'urls'
]
storing_file = open(f'urls.csv', 'a', newline="")
writer = csv.writer(storing_file)
writer.writerow(appending_data)
storing_file.close()
try:

    subpart_chapters = driver.find_elements(By.CLASS_NAME,'divPartDetail')
    for chapter in subpart_chapters:
        a_tags = chapter.find_elements(By.TAG_NAME,'a')
        for a_tag in a_tags:
            urls=a_tag.get_attribute('href')
            appending_data = [
                urls
            ]
            storing_file = open(f'urls.csv', 'a', newline="")
            writer = csv.writer(storing_file)
            writer.writerow(appending_data)
            storing_file.close()
except:
    print('Failed')