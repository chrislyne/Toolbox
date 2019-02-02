from urllib2 import Request,urlopen
import json

class send_message_to_slack():
    
    tex = 'Icecream?'
    username = 'Icecream Bot'
    icon_emoji = ':icecream:'
    channel = '#general'
    
    def send(self):
        
        self.post = {"text": "{0}".format(self.tex),"username": self.username,"icon_emoji": self.icon_emoji,"channel" : self.channel}
        
        try:
            json_data = json.dumps(self.post)
            file = open("toSlack","r") 
            slackHook = file.read() 
            req = Request(slackHook,
                                  data=json_data.encode('ascii'),
                                  headers={'Content-Type': 'application/json'}) 
            resp = urlopen(req)
        except Exception as em:
            print("EXCEPTION: " + str(em))
 
 def icecreamBot():
    newBot = send_message_to_slack()
    newBot.icon_emoji = ':icecream:'
    newBot.username = 'Icecream Bot'
    newBot.tex = 'Icecream?'
    newBot.channel = '#dev'
    newBot.send()

'''
newBot = send_message_to_slack()
newBot.icon_emoji = ':icecream:'
newBot.username = 'Icecream Bot'
newBot.tex = 'Icecream?'
newBot.channel = '#standup'
newBot.send()
'''
