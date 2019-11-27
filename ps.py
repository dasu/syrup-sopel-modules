import socket
import sopel

@sopel.module.commands('ps')
def postscriptum(bot,trigger):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.settimeout(5)
  ip = "147.135.104.72"
  port = 10037
  sock.sendto(b'\xff\xff\xff\xffTSource Engine Query\x00', (ip, int(port)))
  data = sock.recvfrom(1400)
  map = data[0].split(b'\x00')[1].decode()
  players = data[0].split(b'\x00')[6][0]
  maxplayers = data[0].split(b'\x00')[6][1]
  sock.close()
  bot.say("Map: {} | Players: {} / {} ".format(map, players, maxplayers))
