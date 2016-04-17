class GameManager:

  def __init__(self):
    self.clients = {} # addr: name
    self.addrs = {}   # name: addr
    self.games = {}   # name: (is_occupied, opponent, in_game, is_turn)

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
          msg: the msg to be sent to the invited player
          send_addr: the address of the invited player

        In case of error msg will have the error msg and send_addr
        will simply be addr (the addr of the inviting player ''' 

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
    inviting_state[0] = inviting_state[2] = True
    inviting_state[3] = False
    inviting_state[1] = invited

    # set invited user to occupied and as needing to respond
    inviting_state[0] = inviting_state[3] = True
    inviting_state[2] = False
    inviting_state[1] = inviting

    #return send message to invited player
    return GameManagerMessages.USER_INVITE + " " + inviting, addrs[invited]


  









