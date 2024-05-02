from flask import Flask
app = Flask(__name__)

# Sanity Test for Gunicorn + NGINX
@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
