import socket
import sopel

@sopel.module.commands('ps')
def postscriptum(bot,trigger):
  easy1 = {'ip':'147.135.8.209', 'port':10037}
  easy2 = {'ip':'147.135.8.209', 'port':10067}
  servers = [easy1,easy2]
  out = []
  i=0
  for server in servers:
    i+=1
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    sock.sendto(b'\xff\xff\xff\xffTSource Engine Query\x00', (server['ip'], int(server['port'])))
    data = sock.recvfrom(1400)
    map = data[0].split(b'\x00')[1].decode()
    if len(data[0].split(b'\x00')) == 17:
      players = data[0].split(b'\x00')[6][0]
      maxplayers = data[0].split(b'\x00')[6][1]
    else:
      players = 0
      maxplayers = data[0].split(b'\x00')[7][0]
    out.append("[EASY #{}] Map: {} - Players: {} / {}".format(i, map, players, maxplayers))
    sock.close()
  bot.say(' || '.join(out))
