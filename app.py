from flask import Flask

import requests
import urllib.parse

app = Flask(__name__)

@app.route("/search/<query>")
def search(query):
    url_q = urllib.parse.quote(query)
    full_url = "https://www.mountainproject.com/search?q=" + url_q

    response = requests.get(full_url)
    status = response.status_code
    content = response.content

    return {
        "response": content
    }