
import socket
from flask import Flask, request

app = Flask(__name__)

@app.route("/token")
def hello_world():

    card_token = request.args.get("card_token")
    send_to_enclave(card_token)
    return "It works!\n"

def send_to_enclave(card_token):
    client = VsockStream()
    client.connect((5, 5000))
    client.send_data(card_token.encode())
    client.disconnect()

class VsockStream:
    """Client"""
    def __init__(self, conn_tmo=5):
        self.conn_tmo = conn_tmo

    def connect(self, endpoint):
        """Connect to the remote endpoint"""
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.settimeout(self.conn_tmo)
        self.sock.connect(endpoint)

    def send_data(self, data):
        """Send data to a remote endpoint"""
        self.sock.sendall(data)

    def recv_data(self):
        """Receive data from a remote endpoint"""
        while True:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            print(data, end='', flush=True)
        print()

    def disconnect(self):
        """Close the client socket"""
        self.sock.close()