from flask import Flask

app = Flask(__name__)

# creating our first route
@app.route('/')
def hello():
    return 'Hello, World!'