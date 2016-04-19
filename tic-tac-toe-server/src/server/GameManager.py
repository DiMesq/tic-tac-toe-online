import GameManagerMessages

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
    if name in  self.addrs:
      return msg + " nok " + GameManagerMessages.INVALID_USERNAME
    elif addr in self.clients:
      return msg + " nok " + GameManagerMessages.USER_ALREADY_REGISTERED
    else:
      self.clients[addr] = name
      self.addrs[name] = addr
      self.games[name] = [False, None, False, False]
      return msg + " ok"

  def list(self, addr):
    msg = "LST"

    if addr not in self.clients:
      return msg + " " + GameManagerMessages.USER_NOT_REGISTERED

    # check if user is occupied
    name = self.clients[addr]
    if self.games[name][0]:
      return msg + " " + GameManagerMessages.USER_OCCUPIED

    for player, values in self.games.items():
      if player != name:
        msg += " " + player + " " + str(values[0])

    return msg

  def invite(self, invited, addr):
    ''' invited: string, name of the player that is being invited
        addr: string, address of the caller (inviting player)

        returns [msg, send_addr]
          msg: the msg to be sent
          send_addr: to whom the message should be sent. If error, to this caller
            If no error, to the invited player'''

    # check if user is registered
    if addr not in self.clients:
      return GameManagerMessages.USER_NOT_REGISTERED, addr

    # get user info
    inviting = self.clients[addr]
    inviting_state = self.games[inviting]

    # check if user is occupied
    if inviting_state[0]: return GameManagerMessages.USER_OCCUPIED, addr

    # check if player invited exists and is not occupied
    if invited not in self.addrs:
      return GameManagerMessages.OTHER_USER_NOT_REGISTERED, addr

    invited_state = self.games[invited]
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
    return GameManagerMessages.USER_INVITE + " " + inviting, self.addrs[invited]


  def accept(self, other_player, accepted, addr):
    ''' other_player: string, name of the opponent that made the invite
        accepted: string, 'true' if accepts game request. 'false' otherwise.
        addr: string, address of the caller

        returns: [msg, send_addr]
          msg: msg to be sent
          send_addr: to whom the message should be sent. If error, to this caller
            If no error, to the other user (player parameter)'''

    # check if caller is registered
    if addr not in self.clients:
      return GameManagerMessages.USER_NOT_REGISTERED, addr

    # check if accepted has the correct format
    if accepted in ('True', 'False'):
      accepted_bool = True if accepted == 'True' else False
    else:
        return GameManagerMessages.INVALID_COMMAND, addr

    caller = self.clients[addr]
    caller_state = self.games[caller]

    # check if caller is in position to accept a request
    #if not(caller_state[0] and not caller_state[1] and caller_state[2]):
     # return GameManagerMessages.USER_CANT_ACCEPT, addr

    # check if refered player matches the player that made the initial invite
    #if (caller_state[3] != other_player): return GameManagerMessages.REQUEST_PLAYER_MISMATCH, addr

    other_player_state = self.games[other_player]

    # put players in the correct state for game if user accepted
    if accepted_bool:
      caller_state[1] = True
      caller_state[2] = False
    #  other_player[2] = True

    # otherwise put players in begin state
    else:
      self.__default(caller_state)
      self.__default(other_player_state)

    # return message informing the inviter of the decision of his opponent
    return "ACP " + caller + " " + accepted, self.addrs[other_player]

  def play(self, other_player, row, col, is_finito, addr):
    ''' other_player: string, opponent
        row: string, the row of the play (1, 2 or 3)
        col: string, the column of the play (1, 2 or 3)
        is_finito: string, 'true' if play ends the game and 'false' if not

        returns [msg, send_to] '''

    # check if caller is registered
    if addr not in self.clients:
      return GameManagerMessages.USER_NOT_REGISTERED, addr

    # check if accepted has the correct format
    if is_finito in ('True', 'False'):
      is_finito_bool = True if is_finito == 'True' else False
    else:
        return GameManagerMessages.INVALID_COMMAND, addr

    player = self.clients[addr]
    player_state = self.games[player]

    # check if player is in position to make a play
    #if not(player_state[0] and player_state[1] and player_state[2]):
    #  return GameManagerMessages.USER_CANT_PLAY, addr

    # check if the other player is specified correctly
    #if other_player != player_state[3]:
    #  return GameManagerMessages.REQUEST_PLAYER_MISMATCH, addr

    other_player_state = self.games[other_player]

    # check if play has the correct format
    try:
      row = int(row)
      col = int(col)
    except ValueError:
      return GameManagerMessages.INVALID_PLAY, addr

    # check if play is out of bounds
    if row > 3 or row < 1 or col > 3 or col < 1:
      return GameManagerMessages.INVALID_PLAY, addr

    # if game finished return players to default values
    if (is_finito_bool):
      self.__default(player_state)
      self.__default(other_player_state)
    # switch roles if not finished
    else:
      player_state[2] = False
      other_player_state[2] = True

    # return the appropiate message
    return "PLA " + player + " " + str(row) + " " + str(col) + " "\
      + is_finito,\
      self.addrs[other_player]


  def __default(self, state1):
    state1[0] = state1[1] = state1[2] = False
    state1[3] = None
