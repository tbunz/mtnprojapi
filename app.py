from flask import Flask
app = Flask(__name__)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import urllib.parse

@app.route("/")
def sanity():
	return {"sane?": "yes"}

@app.route("/search/<query>")
def search(query):
	# Selenium browser to run JS from mountainproject.com page
	chrome_options = Options()
	chrome_options.page_load_strategy = 'eager'
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')

	driver = webdriver.Chrome(options=chrome_options)

	url_q = urllib.parse.quote(query)
	full_url = "https://www.mountainproject.com/search?q=" + url_q
	driver.get(full_url)

	# Wait at least 1 second for content to render. Earlier if it comes
	driver.implicitly_wait(1)

	# All climbs pulled up from search
	# XPATH to parse through rendered HTML ... whole thang goes down if they change this layout
	elements = driver.find_elements(By.XPATH, '//*[@id="onx-search"]/div/div/div/div[2]/div[1]/div[2]/a')

	climbs =  []
	for index, e in enumerate(elements):
		link = e.get_attribute("href")
		name = e.find_element(By.TAG_NAME, "h3")
		rating = e.find_element(By.XPATH, '//*[@id="onx-search"]/div/div/div/div[2]/div[1]/div[2]/a[' + str(index + 1) + ']/div[1]/div[1]/div')
		location = e.find_element(By.XPATH, '//*[@id="onx-search"]/div/div/div/div[2]/div[1]/div[2]/a[' + str(index + 1) + ']/div[3]/div')
		climb_info = {
			"link": link,
			"name": name.text,
			"rating": rating.text,
			"location": location.text
		}
		climbs.append(climb_info)

	driver.quit()

	return {
		"length": len(climbs),
		"climbs": climbs
		}

if __name__ == "__main__":
    app.run(host='0.0.0.0')
