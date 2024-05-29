import socket
import threading
import signal
import sys
import time

class tcpchat:
    def __init__(self, connect_to_ip: str, callback, port: int = 44785):
        self.server_address = (self.get_local_ip(), port)
        self.client_address = (connect_to_ip, port)
        self.callback = callback
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket = None
        self.server_thread = None
        self.client_ready_event = threading.Event()
        self.connected_event = threading.Event()
        self.stop_event = threading.Event()
        self.retry_connection_interval = 5

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception as e:
            print(f"Unable to get local IP address: {e}")
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    def handle_client_connection(self, connection, client_address):
        print(f"Connection from {client_address}")
        try:
            while not self.stop_event.is_set():
                data = connection.recv(1024)
                if data:
                    self.callback(data.decode())
                else:
                    break
        except Exception as e:
            if not self.stop_event.is_set():
                print(f"An error occurred with client {client_address}: {e}")
        finally:
            connection.close()
            print(f"Connection from {client_address} closed")

    def start_server(self):
        print(f"Starting server on {self.server_address}")
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(5)
        self.client_ready_event.set()

        while not self.stop_event.is_set():
            try:
                connection, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client_connection, args=(connection, client_address))
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if not self.stop_event.is_set():
                    print(f"Server socket accept failed: {e}")
                break

    def run_server(self):
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def connect_to_server(self):
        self.client_ready_event.wait()
        while not self.connected_event.is_set() and not self.stop_event.is_set():
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print(f"Connecting to {self.client_address}")
                self.client_socket.connect(self.client_address)
                self.connected_event.set()
            except ConnectionRefusedError:
                print(f"Connection refused, retrying...")
                self.client_socket.close()
                self.client_socket = None
                time.sleep(self.retry_connection_interval)
            except Exception as e:
                if not self.stop_event.is_set():
                    print(f"An error occurred while connecting to server: {e}")
                break

    def send_message(self, message: str):
        if self.client_socket:
            try:
                self.client_socket.sendall(message.encode())
            except Exception as e:
                print(f"An error occurred while sending message: {e}")

    def close_connections(self):
        self.stop_event.set()
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()

    def signal_handler(self, sig, frame):
        print('Exiting gracefully...')
        self.close_connections()
        sys.exit(0)

    def start(self):
        self.run_server()
        self.connect_to_server()
