class GameManager:

  def __init__(self):
    self.clients = {} # addr: name
    self.addrs = {}   # name: (addr, is_occupied)
    self.games = {}   # name: (opponent, in_game, is_turn)

    # self.games: in_game is True if player is involved in game or
    #       has challenged another player for a game. If it is deciding upon a
    #       request made to it or if it isn't involved in a game it is False.
    #             is_turn is True if player is deciding upon a request or if
    #       it is his turn to play in a game. It's False if it's not playing
    #       or if it his not his turn in the game or even if it's requesting
    #       a different player that hasn't yet accepted

  def register(self, name, addr):
    msg = GameManagerMessages.USER_REGISTER
    if name in addrs:
      return msg + " nok " + GameManagerMessages.INVALID_USERNAME
    elif addr in clients:
      return msg + " nok " + GameManagerMessages.USER_ALREADY_REGISTERED
    else:
      self.clients[addr] = name;
      self.addrs[name] = [addr, False]
      self.games[name] = [None, False, False]
      return msg + " ok"

  def list(addr):
    msg = GameManagerMessages.LIST_USERS

    if addr not in clients:
      return msg + GameManagerMessages.USER_NOT_REGISTERED

    # test if user is occupied
    name = clients[addr]

    if addrs[name][1]:
      return msg + GameManagerMessages.USER_OCCUPIED

    for player, values in addrs.iteritems():
      if player != name:
        msg += " " + player + " " + values[1]

    return msg

  def invite(self, invited, addr):
    ''' player: string, name of the player that is being invited
        addr: string, address of the inviting player

        returns [msg, send_addr]
          msg: the msg to be sent to the invited player
          send_addr: the address of the invited player

        In case of error msg will have the error msg and send_addr
        will simply be addr (the addr of the inviting player ''' 

    # Test if user is registered
    if addr not in clients:
      return GameManagerMessages.USER_NOT_REGISTERED + "Please register" +\
        "yourself first. ", addr
    inviting = clients[addr]
    # Test if user is occupied
    inviting_state = addrs[inviting]
    if inviting_state[1]:
      return GameManagerMessages.USER_OCCUPIED + "Please finish your game first",\
        addr
    # Test if player invited exists and is not occupied
    if invited not in addrs:
      return GameManagerMessages.USER_NOT_REGISTERED + "Invited player is" +\
        " not registered.", addr
    invited_state = addrs[invited]
    if invited_state[1]:
      return GameManagerMessages.USER_OCCUPIED + "Invited player is occupied.",\
        addr

    # set both users to occupied
    inviting_state[1] = True
    games[inviting] = [invited, True, False]

    invited_state[1] = True
    games[invited] = [inviting, False, True]

    #return send message to invited player
    return GameManagerMessages.USER_INVITE + " " + inviting,\
      invited_state[0]









