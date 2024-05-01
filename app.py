from flask import Flask
app = Flask(__name__)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@app.route("/search/<query>")
def search(query):

	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(options=chrome_options)

	driver.get("https://www.google.com")

	content = {"hi": "hey"}

	driver.quit()

	return {"response": content}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
