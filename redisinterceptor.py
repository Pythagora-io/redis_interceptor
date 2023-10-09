import socket
import redis_protocol

# Set the listen port and target port
listen_port = 16379
target_port = 6379

# Create a socket to listen for incoming connections
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the listen port
listen_socket.bind(('', listen_port))

# Start listening for incoming connections
listen_socket.listen(1)

# Loop indefinitely
while True:
    # Accept an incoming connection
    connection, address = listen_socket.accept()

    # Receive data from the connection
    data = connection.recv(4096)

    # If the data contains the string "brija", return 5 packets with the content "yoyobrija"
    if b"brija" in data:
        # Set the chunk size
        chunk_size = 1024

        # Split the string into chunks
        chunks = [b"yoyobrija"[i:i + chunk_size] for i in range(0, len(b"yoyobrija"), chunk_size)]

        # Build the Redis protocol response for each chunk
        responses = [redis_protocol.encode(chunk.decode('utf-8')) for chunk in chunks]

        # Send the responses to the client
        for response in responses:
            connection.send(response.encode('utf-8'))
    # Otherwise, forward the data to the target port
    else:
        # Create a socket to connect to the target port
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the target port
        target_socket.connect(('localhost', target_port))

        # Send the data to the target port
        target_socket.send(data)

        # Receive the response from the target port
        response = target_socket.recv(4096)

        # Forward the response back to the source
        connection.send(response)

        # Close the connection to the target port
        target_socket.close()
        #Commenting_Just_Like that
    # Close the connection
    connection.close()
