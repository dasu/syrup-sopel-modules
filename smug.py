import willie
import random

smuglist = ['MZqGg95.png', 'h6mkYlW.jpg', 'LDhYNOS.png', 'tieHaeH.jpg', 'mfCYU45.jpg', 'kPhNAdN.png', 'zF32B7U.png', 'VM9bNwI.png', 'xP4wLIA.jpg', 'uPhLEtm.jpg', '6ATCxNY.jpg', 'qg5bDnk.jpg', 'kQ5VNMQ.jpg', 'FwStV5K.jpg', 'E0pQiMm.jpg', 'DYH1xb2.jpg', 'IWE4Jin.jpg', 'YXZCvvV.jpg', 'G3ggwxR.jpg', 'mwCpw2y.png', 'iuQEQuP.jpg', 'uNRqsdG.png', '7tK77BS.jpg', 'uTntqMc.jpg', 'bqCgKXU.jpg', '2tiLuyQ.jpg', 'fPCavEd.jpg', 'GlfoGnI.jpg', 'vRxXn30.jpg']

@willie.module.commands('smug')
def smug(bot,trigger):
	bot.say("https://i.imgur.com/%s" % random.choice(smuglist))

@willie.module.commands('smugpoi')
def smugpoi(bot,trigger):
	bot.say("https://i.imgur.com/%s poi" % random.choice(smuglist))
