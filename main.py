import json
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, InputPeerUser, InputPeerChat, InputPeerChannel
from telethon.tl.types.messages import Messages
from telethon.sessions import StringSession
import random
from Vars import Variables,Slovar
from telethon.sync import  TelegramClient, events
import configparser as cfg
import time
config = cfg.ConfigParser()



with open("config.ini", "r") as config_file:
     config.write(config_file)
config.read('config.ini')
Limit = bool(config["BotSettings"]["Limit"])
max_count =int(config["BotSettings"]["Limitcount"])
AutoReply = bool(config["BotSettings"]["AutoReply"])
ProxyUse = bool(config["BotSettings"]["ProxyUse"])
echoall = bool(config["BotSettings"]["echoall"])
echotype = str(config["BotSettings"]["echoType"])
messagetoecho = str(config["BotSettings"]["messagetoecho"])
echobasefile = str(config["BotSettings"]["echobase"])

ProxylistFile = str(config["BotSettings"]["ProxylistFile"])


with open('Acc.json','r') as json_file:
    data = json.load(json_file)
    print(data)


    api_id = [item.get('app_id') for item in data]
    api_hash = [item.get('app_hash') for item in data]
    StringSession = [item.get('StringSession') for item in data]


f = open("answer.txt",encoding="utf-8")

iplist = []
portlist = []


b = f.readlines()
one = 0
while one <1:
    one = one+1
    k = open(ProxylistFile,'r')
    o = k.readlines()
    for j in range(len(o)):
        proxys =o[j]
        ip,port =proxys.split(":")
        print(ip)
        print(port)
        iplist.append(ip)
        portlist.append(port)


for i in range(len(b)):
    b[i] = b[i].strip("\n")

limitcount = True
@events.register(events.NewMessage(incoming=True))
async def handler(event):
   client = event.client
   sender = await event.get_sender()


   if AutoReply ==True:
    if Limit == True:

     for i in range (len(api_hash)):
       user = await Variables[i].get_entity(sender.id)

       for name,count in Slovar[i].items():


          if name == user.first_name:
             print(name)
             print(count)
             if count<max_count:

              await event.reply(b[random.randint(0, len(b))].strip('\n'))
              break;
     else:
      await event.reply(b[random.randint(0, len(b))].strip('\n'))










def countofmessage(client):
    from telethon.tl.functions.messages import GetDialogsRequest
    from telethon.tl.types import InputPeerEmpty

    get_dialogs = GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=30,
        hash=0
    )

    dialogs = client(get_dialogs)



    counts = {}
    chats = {}
    users = {}
    for u in dialogs.users:
        users[u.id] = u

    for c in dialogs.chats:
        chats[c.id] = c

    for d in dialogs.dialogs:
        peer = d.peer
        if isinstance(peer, PeerChannel):
            id = peer.channel_id
            channel = chats[id]
            access_hash = channel.access_hash
            name = channel.title

            input_peer = InputPeerChannel(id, access_hash)
        elif isinstance(peer, PeerChat):
            id = peer.chat_id
            group = chats[id]
            name = group.title

            input_peer = InputPeerChat(id)
        elif isinstance(peer, PeerUser):
            id = peer.user_id
            user = users[id]
            access_hash = user.access_hash
            name = user.first_name

            input_peer = InputPeerUser(id, access_hash)
        else:
            continue

        get_history = GetHistoryRequest(
            peer=input_peer,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=1,
            max_id=0,
            min_id=0,
            hash=0
        )

        history = client(get_history)
        if isinstance(history, Messages):
            count = len(history.messages)
        else:
            count = history.count

        counts[name] = count


    return counts




def getStringsession(api_id,api_hash): # Fuction to get string session
    f = open("Sessionstr.txt","a")

    with TelegramClient(StringSession(), api_id, api_hash) as client:
        StrSession = client.session.save();
    f.write(StrSession + "\n")


def run():




  for i in range(len(api_hash)):

    if ProxyUse == True:

     proxy = ("HTTP",iplist[i],portlist[i]) #proxt type HTTPS,HTTPS,SOCKS.
     Variables[i] = TelegramClient(
        session="None"+str(i),#If you want to use string session print "StringSession()"
        api_id=api_id[i],
        api_hash=api_hash[i],
        proxy=proxy,


     )


    else:
       Variables[i] = TelegramClient(
           session="None" + str(i),
           api_id=api_id[i],
           api_hash=api_hash[i],
           proxy=None,

       )


    Variables[i].start()


    Variables[i].add_event_handler(handler)

run()
def echoallusername(messagetoecho):
    a=[]
    for i in range(len(api_hash)):
        dialogs = Variables[i].get_dialogs()


        for l in range(len(dialogs)):
          if(dialogs[l].id > 0):
            print(dialogs[l].id)
            user = Variables[i].get_entity(dialogs[l].id)
            a.append(user.username )
        for c in range(len(a)):
            try:



                Variables[i].connect()
                Variables[i].send_message(a[c], messagetoecho)
            except:
             continue
    a.clear()

def echoallphone(messagetoecho):
    a=[]
    for i in range(len(api_hash)):
        dialogs = Variables[i].get_dialogs()


        for l in range(len(dialogs)):
          if(dialogs[l].id > 0):

            user = Variables[i].get_entity(dialogs[l].id)
            a.append(user.phone )
        for c in range(len(a)):
            try:



                Variables[i].connect()
                Variables[i].send_message(a[c], messagetoecho)
            except:
               continue
    a.clear()




def echoallid(messagetoecho):
    a=[]
    for i in range(len(api_hash)):
        dialogs = Variables[i].get_dialogs()


        for l in range(len(dialogs)):
          if(dialogs[l].id > 0):
            print(dialogs[l].id)
            a.append(dialogs[l].id)
        for c in range(len(a)):
            try:
                Variables[i].connect()
                Variables[i].send_message(a[c], messagetoecho)
            except:
             continue


    a.clear()

def spamonnumber(text,echobasefile):
   d = open(echobasefile,"r")
   g = d.readlines()
   for i in g:
        for c in range(len(api_hash)):
            Variables[c].send_message(i,text)


def spamusername(text,echobasefile):
    d = open(echobasefile, "r")
    g = d.readlines()
    for i in g:
        for c in range(len(api_hash)):
            Variables[c].send_message(i, text)



def UpdateSlovar():
    for i in range(len(api_hash)):
        Slovar[i] = countofmessage(Variables[i])


if echoall == True:
    if echotype == "id":
        echoallid(messagetoecho)
    if echotype == "username":
        echoallusername(messagetoecho)
    if echotype == "phone":
        echoallphone(messagetoecho)
    if echotype == "phonefromfile":
        spamonnumber(echobasefile,messagetoecho)
    if echotype == "usernamefromfile":
        spamusername(echobasefile,messagetoecho)


p = 0

while p<2:
 p+1

 for i in range(len(api_hash)):
   Slovar[i] = countofmessage(Variables[i])

   Variables[i].connect()
   Variables[i].run_until_disconnected()
timing = time.time()
while True:
    if time.time() - timing > 4.0:
        timing = time.time()
        UpdateSlovar()










