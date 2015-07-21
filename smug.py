import willie
import random

smuglist = ['MZqGg95.png', 'h6mkYlW.jpg', 'LDhYNOS.png', 'tieHaeH.jpg', 'mfCYU45.jpg', 'kPhNAdN.png', 'zF32B7U.png',
            'VM9bNwI.png', 'xP4wLIA.jpg', 'uPhLEtm.jpg', '6ATCxNY.jpg', 'qg5bDnk.jpg', 'kQ5VNMQ.jpg', 'FwStV5K.jpg',
            'E0pQiMm.jpg', 'DYH1xb2.jpg', 'IWE4Jin.jpg', 'YXZCvvV.jpg', 'G3ggwxR.jpg', 'mwCpw2y.png', 'iuQEQuP.jpg',
            'uNRqsdG.png', '7tK77BS.jpg', 'uTntqMc.jpg', 'bqCgKXU.jpg', '2tiLuyQ.jpg', 'fPCavEd.jpg', 'GlfoGnI.jpg',
            'vRxXn30.jpg', 'wsxBNXS.png', 'SMGrifX.jpg', 'pyHUAt8.png', 'IuCuxAE.jpg', 'SZXTjje.jpg', 'S1rjrZi.jpg',
            'p4YDQOv.png', 'agxAcMO.png', 'kKGxv6W.jpg', 'mi83eAk.jpg', 'mOqwYkv.jpg', 'GQaHsu7.jpg', 'v1P0LOD.jpg',
            'GIhBth1.jpg', 'kbhIWb4.jpg', 'X5q12M7.jpg', 'U5sNuXo.jpg', 'o634Afu.jpg', 'pRKGkN3.jpg', '7wf2c98.jpg',
            'e79YOdg.jpg', '0fXuTyN.jpg', 'fJlQFwW.jpg', 'S8rDYrO.jpg', 'LAH8qUx.png', '1rJlvU2.png', '2kDuhjz.png',
            'c1cgjRG.png', '3IWuedb.jpg', 'pkixlEB.png', 'L4Xz2qh.jpg', 'HvrL7LG.jpg', 'FaCVdjx.jpg', 'Be1S4S1.jpg',
            'A8ZPA9m.jpg', 'jgVXLuG.jpg', 'zfulnbC.jpg', 'wcfZJ0m.jpg', 'ysSF9DJ.jpg', 'vTEGZZv.jpg', 'lwkvwpA.jpg',
            'AaBqzfi.jpg']

@willie.module.commands('smug')
def smug(bot,trigger):
        bot.say("https://i.imgur.com/%s" % random.choice(smuglist))

@willie.module.commands('smugpoi')
def smugpoi(bot,trigger):
        bot.say("https://i.imgur.com/%s poi" % random.choice(smuglist))
