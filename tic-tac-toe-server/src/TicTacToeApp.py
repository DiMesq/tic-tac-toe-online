import sys

sys.path.insert(0, 'server')
from ServerEndpoint import ServerEndpoint
import server_constants

### SERVER APPLICATION ###
if __name__ == "__main__":
  server_app = ServerEndpoint(server_constants.SERVER_PORT)

  print("Starting the server ...")
  server_app.start()

  print("Enter a key to shutdown")
  server_app.get_messages()

  print("Shutting down...")
  server_app.kill()
  print("Shut down with success.")






