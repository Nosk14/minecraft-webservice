from petitions.rcon import Request, ConnectionManager
import datetime, json

class Status:
    def __init__(self):
        self.players = []
        self.isOnline = False
        self.lastUpdate = datetime.datetime(datetime.MINYEAR,1,1)
        
    def to_json(self):
        d = dict(self.__dict__)
        d['lastUpdate'] = self.lastUpdate.strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps(d)

class ServerInfo:

    def __init__(self,password,ip,port=25575):
        self.__cm = ConnectionManager(password,ip,port)
        self.__cache = Status()
        self.__UPDATETIME = 60 # in seconds

    def __update_info(self):
        rq = Request(2,'list')
        rs = self.__cm.send_request(rq)
        
        return self.__parse_response(rs)
        
    def __parse_response(self,response):
        status = Status()
        status.lastUpdate = datetime.datetime.utcnow()
        status.isOnline = True
        
        players_raw = response.data.split(':', 1)[1]
        players_raw = players_raw.split(',')
        
        players = []
        for p in players_raw:
            if p.strip():
                players.append(p.strip())
        
        status.players = players
        
        return status
    
    def get_info(self):    
        update_span = datetime.datetime.utcnow() - self.__cache.lastUpdate
        if update_span.seconds > self.__UPDATETIME:
            try:
                self.__cache = self.__update_info()
            except Exception as e:
                print(e)
                status = Status()
                status.lastUpdate = datetime.datetime.utcnow()
                self.__cache = status
        
        return self.__cache
        