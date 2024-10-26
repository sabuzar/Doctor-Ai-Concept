from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
def google_search(query):
    driver = webdriver.Chrome()
    driver.get('https://www.google.com')
    search_box = driver.find_element(By.NAME,'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)
    search_result = driver.find_element(By.CSS_SELECTOR,'#search .g')
    output = search_result.text
    driver.quit()
    return output


query = input("Enter your search query: ")
result = google_search(query)
print("Brief output:")
print(result)
