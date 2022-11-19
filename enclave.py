
import socket

class VsockListener:
    """Server"""
    def __init__(self, conn_backlog=128):
        self.conn_backlog = conn_backlog

    def bind(self, port):
        """Bind and listen for connections on the specified port"""
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.bind((socket.VMADDR_CID_ANY, port))
        self.sock.listen(self.conn_backlog)

    def recv_data(self):
        """Receive data from a remote endpoint"""
        while True:
            (from_client, (remote_cid, remote_port)) = self.sock.accept()
            # Read 1024 bytes at a time
            while True:
                try:
                    data = from_client.recv(1024).decode()
                except socket.error:
                    break
                if not data:
                    break
                self.proccess_data(data)
            print()
            from_client.close()

    def send_data(self, data):
        """Send data to a renote endpoint"""
        while True:
            (to_client, (remote_cid, remote_port)) = self.sock.accept()
            to_client.sendall(data)
            to_client.close()

    def proccess_data(self, data):
        print("recived: ", data)
        print("decrypted: ", data[::-1])
def main():
    server = VsockListener()
    server.bind(5000)
    server.recv_data()


if __name__ == "__main__":
    main()