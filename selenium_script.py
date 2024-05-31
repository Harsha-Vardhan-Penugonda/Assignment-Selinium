import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient

#Iam not mentioning my Useranes and passwords forSecurity Concerns. 
PROXYMESH_USERNAME = 'my proxy name'
PROXYMESH_PASSWORD = '****'
PROXYMESH_SERVER = 'us-wa.proxymesh.com:31280'


TWITTER_USERNAME = 'Twitter My id'
TWITTER_PASSWORD = '****'


client = MongoClient('mongodb+srv://penugondaharshavardhan:02sUz4zgwxatll1Z@cluster0.cgqgami.mongodb.net/')
db = client['twitter_trends']
collection = db['trends']

options = webdriver.ChromeOptions()
proxy_address = f'http://{PROXYMESH_USERNAME}:{PROXYMESH_PASSWORD}@{PROXYMESH_SERVER}'
options.add_argument(f'--proxy-server={proxy_address}')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_trending_topics():
    driver.get('https://x.com/explore/tabs/keyword')
    
    
    username_input = driver.find_element(By.NAME, 'session[username_or_email]')
    password_input = driver.find_element(By.NAME, 'session[password]')
    username_input.send_keys(TWITTER_USERNAME)
    password_input.send_keys(TWITTER_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(10) 

   
    trends = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[3]/div/div/div/div/div[2]/span/span")
    trending_topics = [trend.text for trend in trends[:5] if trend.text]
    return trending_topics

def save_to_mongo(trending_topics):
    unique_id = str(time.time())
    data = {
        '_id': unique_id,
        'trends': trending_topics,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'ip_address': PROXYMESH_SERVER
    }
    collection.insert_one(data)
    return data

if __name__ == "__main__":
    trending_topics = get_trending_topics()
    record = save_to_mongo(trending_topics)
    driver.quit()
    print(json.dumps(record, indent=4))
