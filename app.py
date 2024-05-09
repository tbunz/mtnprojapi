from flask import Flask
app = Flask(__name__)

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import urllib.parse
import json

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

@app.route("/climb_info/<climb_list>")
def climb_info(climb_list):
	climbs = json.loads(climb_list)

	# Initialize browser
	chrome_options = Options()
	chrome_options.page_load_strategy = 'eager'
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')

	driver = webdriver.Chrome(options=chrome_options)

	climb_info = []

	# For each climb we've been passed request info from its main page
	for key in climbs:
		url_q = urllib.parse.quote(key + "/" + climbs[key])
		full_url = "https://www.mountainproject.com/route/" + url_q
		driver.get(full_url)

		# Wait at least 1 second for content to render. Earlier if it comes
		driver.implicitly_wait(1)

		try:
			grade = driver.find_element(By.XPATH, '//*[@id="route-page"]/div/div[1]/h2/span[1]')
			type = driver.find_element(By.XPATH, '//*[@id="route-page"]/div/div[3]/div[1]/div[1]/div[1]/table/tbody/tr[1]/td[2]')
			fa = driver.find_element(By.XPATH, '//*[@id="route-page"]/div/div[3]/div[1]/div[1]/div[1]/table/tbody/tr[2]/td[2]')
			description = driver.find_element(By.XPATH, '//*[@id="route-page"]/div/div[3]/div[1]/div[4]/div[2]/div')
			protection = driver.find_element(By.XPATH, '//*[@id="route-page"]/div/div[3]/div[1]/div[4]/div[3]/div')
			img1 = driver.find_element(By.XPATH, '//*[@id="route-page"]/div/div[3]/div[2]/div/div[1]/a/div/img')
			# TODO - add comments. Need to run some script from page to get
			climb_info.append({
		                "name": climbs[key],
		                "uid": key,
		                "grade": grade.text,
		                "type": type.text,
		                "fa": fa.text,
		                "description": description.text,
		                "protection": protection.text,
		                "img1": img1.get_attribute("data-src")
		        })

		# TODO catch missing elements and still return rest of response
		except NoSuchElementException as e:
			print(e)
			climb_info.append({
				"name": climbs[key],
				"uid": key,
				"under_construction": "some elements were not found ... under construction"
			})

	driver.quit()
	return climb_info

if __name__ == "__main__":
    app.run(host='0.0.0.0')
