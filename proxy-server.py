#!/usr/bin/env python
from flask import Flask 
from request import requests

app = Flask(__name__)


@app.route('/')
def welcome():
    url = request.args.get('url')
    response = '<title>Welcome to a Simple Test Proxy Server</title><body>Welcome to the Server Homepage! This is the default page.</body>'
    if url:
        response = requests.get(url).content
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')


