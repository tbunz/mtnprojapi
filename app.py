from flask import Flask

import urllib.parse
import time 

from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By 

app = Flask(__name__)

@app.route("/search/<query>")
def search(query):

    options = webdriver.ChromeOptions() 
    options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability

    # By default, Selenium waits for all resources to download before taking actions.
    # However, we don't need it as the page is populated with dynamically generated JavaScript code.
    options.page_load_strategy = "none"

    # Pass the defined options objects to initialize the web driver 
    driver = Chrome(options=options) 
    # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
    driver.implicitly_wait(5)



    # url_q = urllib.parse.quote(query)
    # full_url = "https://www.mountainproject.com/search?q=" + url_q

    # response = driver.get(full_url)

    
   
    return {
        "response": content
    }