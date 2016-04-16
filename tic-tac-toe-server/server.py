class Server: 
  ''' Server for playing Tic Tac Toe online

      Includes two methods: start() and kill(), to start and kill the server respectively.

      The server is located at port 12000. When the start method is called, the server
      is initiated and waits for client messages. The following commands are valid:

        - "REG <username>" -> registers new player. Server responds with "REG ok" if
                              the player was able to successfully registered.
                              Otherwise it respondes with "REG nok <error message>".

        - "LST" -> ask for a list of players. The returned list has the format 
                   "LST <username1> <boolean>, <username2> <boolean>, [...]".
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
        game requests from other players.

        One final note is that the server does not save the state of the game between the players.
        It is expected that the players do this. '''

    




