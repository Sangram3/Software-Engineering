from flask import Flask, request, Response

app = Flask(__name__)

success_code = Response(status=200)
failiure_code = Response(status=500)

RECEIVER_PORT = 8090
RECEIVER_HOST = '127.0.0.1'
ROUTER_URL = "http://127.0.0.1:5050/"

@app.route('/' , methods = ['GET' , 'POST'])
def receiver_home():
    data = request.data
    print("RECEIVER: " , data)
    return str(success_code)
    
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(host = RECEIVER_HOST, port = RECEIVER_PORT, debug=True)