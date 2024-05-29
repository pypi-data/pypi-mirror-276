# tcpChat

tcpChat is a simple Python module for creating a TCP chat connection between two computers to send commands or information.

GitHub: [tcpChat](https://github.com/clevrthings/tcpChat)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install tcpChat.

```bash
pip install clevrthings-tcpChat
```

## Usage
```python
from tcpChat import tcpchat

def callback_function(message):
    print(f"Received message: {message}")

connect_to_ip = "10.0.0.142" # Enter the IP Address from the other computer
on_port = 44785 # Choose a port for the connection. (Optional. Default = 44785)

connection = tcpchat(connect_to_ip, callback_function, on_port)
connection.start()

# Example of sending a message from the main thread
connection.send_message("Hello from server")
```
### Extra functions
```python
tcpchat.get_local_ip() # Returns own IP Address

tcpchat.close_connections() # Closes all the connections

tcpchat.retry_connection_interval = 2 # Set the retry interval (Default = 5 seconds)
```


## License
MIT