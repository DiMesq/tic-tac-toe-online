class GameManager:

  def __init__(self):
    self.clients = {} # addr: name
    self.addrs = {}   # name: addr
    self.games = {}   # name: (is_occupied, in_game, is_turn, opponent)

    # self.games: in_game | is_turn  | player_state                         |
    #             --------+----------+--------------------------------------|
    #              False  |  False   | not occupied (**)                    |
    #             --------+----------+--------------------------------------|
    #              False  |  True    | deciding upon request to play (*)    |
    #             --------+----------+--------------------------------------|
    #              True   |  False   | requested another player for game or |
    #                                | is waiting for turn to play (*)      |
    #             --------+----------+--------------------------------------|
    #              True   |  True    | his turn to play (*)                 |
    #
    #                 (*)  -> is_occupied = True
    #                 (**) -> is_occupied = False

  def register(self, name, addr):
    msg = GameManagerMessages.USER_REGISTER
    if name in addrs:
      return msg + " nok " + GameManagerMessages.INVALID_USERNAME
    elif addr in clients:
      return msg + " nok " + GameManagerMessages.USER_ALREADY_REGISTERED
    else:
      self.clients[addr] = name
      self.addrs[name] = addr
      self.games[name] = [False, None, False, False]
      return msg + " ok"

  def list(addr):
    msg = GameManagerMessages.LIST_USERS

    if addr not in clients:
      return msg + GameManagerMessages.USER_NOT_REGISTERED

    # check if user is occupied
    name = clients[addr]
    if games[name][0]:
      return msg + GameManagerMessages.USER_OCCUPIED

    for player, values in games.iteritems():
      if player != name:
        msg += " " + player + " " + values[0]

    return msg

  def invite(self, invited, addr):
    ''' invited: string, name of the player that is being invited
        addr: string, address of the caller (inviting player)

        returns [msg, send_addr]
          msg: the msg to be sent
          send_addr: to whom the message should be sent. If error, to this caller
            If no error, to the invited player''' 

    # check if user is registered
    if addr not in clients:
      return GameManagerMessages.USER_NOT_REGISTERED, addr

    # get user info
    inviting = clients[addr]
    inviting_state = games[inviting]

    # check if user is occupied
    if inviting_state[0]:
      return GameManagerMessages.USER_OCCUPIED, addr

    # check if player invited exists and is not occupied
    if invited not in addrs:
      return GameManagerMessages.OTHER_USER_NOT_REGISTERED, addr
    invited_state = clients[invited]
    if invited_state[0]:
      return GameManagerMessages.OTHER_USER_OCCUPIED, addr

    # set inviting user to occupied and as requesting turn
    inviting_state[0] = inviting_state[1] = True
    inviting_state[2] = False
    inviting_state[3] = invited

    # set invited user to occupied and as needing to respond
    inviting_state[0] = inviting_state[2] = True
    inviting_state[1] = False
    inviting_state[3] = inviting

    #return send message to invited player
    return GameManagerMessages.USER_INVITE + " " + inviting, addrs[invited]


  def accept(self, other_player, accepted, addr):
    ''' other_player: string, name of the opponent that made the invite
        accepts: string, True if accepts game request. False otherwise.
          valid formats for True: 'True'; 'true'; 't'; '1'
          valid formats for False: 'False'; 'false'; 'f'; '0'
        addr: string, address of the caller

        returns: [msg, send_addr]
          msg: msg to be sent
          send_addr: to whom the message should be sent. If error, to this caller
            If no error, to the other user (player parameter)'''

    # check if accepted has the correct format
    if   accepted in ('True', 'true', 't', '1'): accepted = True 
    elif accepted in ('False', 'false', 'f', '0'): accepted = False
    else: return GameManagerMessages.INVALID_COMMAND

    # check if caller is registered
    if addr not in clients:
      return GameManagerMessages.USER_NOT_REGISTERED, addr

    caller = clients[addr]
    caller_state = games[caller]

    # check if caller is in position to accept a request
    if not(caller_state[0] and caller_state[3]):
      return USER_CANT_ACCEPT, addr

    # check if refered player matches the player that made the initial invite
    if (caller_state[3] != other_player):
      return REQUEST_PLAYER_MISMATCH, addr

    other_player_state = games[other_player]

    # put players in the correct state for game if user accepted
    if accepted:
      caller_state[1] = True, caller_state[2] = False
      other_player[2] = True 

    # otherwise put players in begin state
    else:
      caller_state[0] = caller_state[1] = caller_state[2] = False
      other_player_state[0] = other_player_state[1] = other_player_state[2] = False

    # return message informing the inviter of the decision of his opponent
    return "ACP " + caller + " " + accepted, addrs[other_player]

def play(self, other_player, row, col, is_finito):
  ''' other_player: string, opponent
      row: string,







