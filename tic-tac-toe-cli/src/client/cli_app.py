import socket
import sys
import select

import cli_constants

sock = socket.socket(cli_constants.SOCKET_TYPE,cli_constants.SOCKET_PROTOCOL)

# o select quer ficar a espera de ler o socket e ler do stdin (consola)
inputs = [sock, sys.stdin]
flag = True

while True:
  if flag: print("Input message to server below.")
  ins, outs, exs = select.select(inputs,[],[])
  #select devolve para a lista ins quem esta a espera de ler
  for i in ins:
    # i == sys.stdin - alguem escreveu na consola, vamos ler e enviar
    if i == sys.stdin:
      # sys.stdin.readline() le da consola
      msg = sys.stdin.readline()
      # envia mensagem da consola para o servidor
      sock.sendto(msg.encode(),(cli_constants.SERVER_IP, cli_constants.SERVER_PORT))
      flag = False
    # i == sock - o servidor enviou uma mensagem para o socket
    elif i == sock:
      (msg,addr) = sock.recvfrom(1024)
      resp = msg.decode()
      flag = False if resp == 'OK' else True
      print("Message received from server:", resp)