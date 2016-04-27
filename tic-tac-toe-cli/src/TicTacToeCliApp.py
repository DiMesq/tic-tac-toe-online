import sys

sys.path.insert(0, 'client')
from Client import Client
import client_constants

### SERVER APPLICATION ###
if __name__ == "__main__":
    print("Enter the port for this client")
    port = int(sys.stdin.readline())
    client = Client(port, client_constants.SERVER_IP, client_constants.SERVER_PORT)

    print("Starting the client ...")
    client.start()

    print("Enter your username")
    username = sys.stdin.readline()

    while not (client.register(username)):
        print("Please insert another username")
        username = sys.stdin.readline()

    print("Successfully registered")

    client.get_messages()
    
    print("Shutting down...")
    client.kill()
    print("Shut down with success.")
