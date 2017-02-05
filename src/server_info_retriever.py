import rcon, socket, json
from datetime import datetime

class ServerStatus:
    def __init__(self,ip='localhost',port=25575):
        self.__ip = ip
        self.__port = port
        self.players = []
        self.isOnline = False
        self.lastUpdate = '-1'
        
    def update_info(self):
        self.lastUpdate = datetime.utcnow().isoformat()
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.__ip,self.__port))
            
            #login
            login = rcon.Request(0,3,'mcrcon123')
            s.send(login.to_bytes())
            r = s.recv(4096)
            
            #player list
            command = rcon.Request(0,2,'list')
            s.send(command.to_bytes())
            response = rcon.Response(s.recv(4096))

            self.__parseResponse(response)
        
        except TimeoutError as e:
            self.isOnline = False
            self.players = []
        finally:
            s.close()
            
    def __parseResponse(self,response):
        self.isOnline = True
        
        players_raw = response.data.split(':', 1)[1]
        players_raw = players_raw.split(',')
        
        players = []
        for p in players_raw:
            players.append(p.strip())
        
        self.players = players
        
    def to_json(self):
        d = dict(self.__dict__)
        d.pop('_ServerStatus__ip',None)
        d.pop('_ServerStatus__port',None)
        return json.dumps(d)

        
if __name__ == "__main__":
    ss = ServerStatus('92.222.81.25')
    ss.update_info()
    print(ss.to_json())