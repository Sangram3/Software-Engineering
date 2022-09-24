import requests
from flask import Flask, Response

app = Flask(__name__)

success_code = Response(status=200)
failure_code = Response(status=500)

SENDER_PORT = 4444
SENDER_HOST = '127.0.0.1'
ROUTER_URL = "http://127.0.0.1:5050/"

xml = 0

@app.route('/')
def sender_home():
    #send message to the router
    print(xml)
    resp = requests.post(url = ROUTER_URL, data = xml)
    print(resp.status_code)
    # if status_code is 200 then success 500 failure
    return str(resp.status_code)
def main():
    app.secret_key='secret123'  
    app.run(host = SENDER_HOST, port = SENDER_PORT, debug=True)