import socket
import sys
import select

import server_constants
from GameManager import GameManager

class ServerEndpoint: 
  ''' ServerEndpoint for playing Tic Tac Toe online

      Includes two methods: start() and kill(), to start and kill the server respectively.

      The server is located at port 12000. When the start method is called, the server
      is initiated and waits for client messages. The following commands are valid:

        - "REG <username>" -> registers new player. Server responds with "REG ok" if
                              the player was able to successfully registered.
                              Otherwise it respondes with "REG nok <error message>".

        - "LST" -> ask for a list of players. The returned list has the format 
                   "LST <username1> <boolean> <username2> <boolean> [...]".
                   Where <usernamex> represents another registered user. The <boolean>
                   field is True for the users that are available to play a game or False 
                   otherwise. 

        - "INV <username>" -> invites a user <username> to play a game. The response has the
                              format "ACP <username> <boolean>" where <username> is the name of
                              the requested player and <boolean> is True if the invite was accepted
                              and False if not.

        - "ACP <username> <boolean>" -> responds to a match request. This command should only be used
                                        if requested for a game. <username> indicates the player
                                        that made the invite and <boolean> should be True if the
                                        request is accepted and false otherwise.
 
        - "PLA <username> <row> <column> <boolean>" -> makes a play. This command should be used
                                                       during game play when it's the player's turn
                                                       to make a play. Here <username> represents the
                                                       opponent in the game. <boolean> should only be
                                                       true if the play ends the game.

        The server always responds with an "OK" message if the command was received. This is independent
        of the command that was given, meaning that the client should always expect it everytime it 
        sends a message to the server.

        A registered user should also be listening to the server in order to be able to receive
        game requests from other players. These request will have the format "INV <username>", 
        where username is the player making the invite. The response is has specified above.

        Also the players in game must be listening for the other player's moves. The server communicates 
        a move from the opponent with "PLA <row> <column> <boolean>", where boolean indicates if the play
        terminates the game or not.

        One final note is that the server does not save the state of the game between the players.
        It is expected that the players do this. '''

  def __init__(self, port):
    self.port = port
    self.server = socket.socket(server_constants.SOCKET_TYPE, server_constants.SOCKET_PROTOCOL)
    self.game_manager = GameManager()

  def start(self):
    self.server.bind(('',self.port))

  def get_messages(self):
    ''' Returns when user enters something in stdin '''
    inputs = [self.server, sys.stdin]

    while True:
      ins, outs, exs = select.select(inputs,[],[])
      
      for i in ins:
        if i == sys.stdin:
          return
        elif i == self.server:
          (msg,addr) = self.server.recvfrom(1024)

          # Message receival confirmation
          self.send_message(server_constants.MESSAGE_RECEIVED, addr)

          # Deal with message
          self.game_manager.resolve_command(msg, addr);

  def resolve_command(self, command, addr):
    cmds = command.decode().split()
    
    msg = server_constants.INVALID_COMMAND

    if (cmds is None): 
      pass
    elif(cmds[0]=="REG"):
      if (len(cmds) == 2): msg = self.game_manager.register(cmds[1],addr)
    elif(cmds[0]=="LST"):
      if (len(cmds) == 1): msg = self.game_manager.list(addr)
    elif(cmds[0]=="INV"):
      if (len(cmds) == 2): msg, addr = self.game_manager.invite(cmds[1], addr)
    elif(cmds[0]=="ACP"):
      if (len(cmds) == 3): msg, addr = self.game_manager.accept(cmds[1], cmds[2], addr)
    elif(cmds[0]=="PLA"):
      if (len(cmds) == 5): msg, addr = self.game_manager.play(cmds[1], cmds[2], cmds[3], cmds[4], addr)      
    
    self.send_message(msg, addr)
    
  def send_message(self, msg, addr):
    sock.sendto(msg.encode(), addr)

  def kill(self):
    self.server.close()

