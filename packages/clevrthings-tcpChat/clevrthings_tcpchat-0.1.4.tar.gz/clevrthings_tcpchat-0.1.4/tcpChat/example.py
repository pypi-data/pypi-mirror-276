from tcpChat import tcpchat

def callback_function(message):
    print(f"Received message: {message}")

connect_to_ip = "10.0.0.142" # Enter the IP Address from the other computer
on_port = 44785 # Choose a port for the connection. (Optional. Default = 44785)

connection = tcpchat(connect_to_ip, callback_function, on_port)
connection.start()

# Example of sending a message from the main thread for testing
try:
    while True:
        message = input("Message: ")
        if message:
            connection.send_message(message)
except (EOFError, KeyboardInterrupt):
    connection.signal_handler(None, None)

tcpchat.retry_connection_interval = 2