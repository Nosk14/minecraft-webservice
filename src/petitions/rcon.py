import socket, struct, time, logging

class Request:
    
    def __init__(self,t,payload,id=0):
        self.id = id
        self.__t = t
        self.__payload = payload
    
    def to_bytes(self):
      format_pack = "<ii{}sxx".format(len(self.__payload))
      b = struct.pack(format_pack,self.id,self.__t,bytes(self.__payload,'ASCII'))
      size_b = len(b)
      b = struct.pack("<i{}s".format(size_b),size_b,b)
        
      return b
      
      
class Response:
    
    def __init__(self,response):
        self.size = struct.unpack('<i',response[0:4])[0]
        data = struct.unpack('<ii{}sxx'.format(self.size-10),response[4:])
        self.id = data[0]
        self.t = data[1]
        self.data = data[2].decode('UTF-8')
        
    def __str__(self):
        return "size: {} | id: {} | type: {} \ndata:\n{}".format(self.size,self.id,self.t,self.data)
        
        
class ConnectionManager:
    
    def __init__(self,password,ip='localhost',port=25575):
        self.__ip = ip
        self.__port = port
        self.__password = password
        self.__id = 0

    def __get_id(self):
        self.__id +=1
        return self.__id
        
    def __send_request(self, request, sock):
        request.id = self.__get_id()
        
        sock.send(request.to_bytes())
        
        r = Response(sock.recv(4096))
        
        return r
    
    def __login(self):
        rq = Request(3,self.__password)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__ip,self.__port))
        
        rs = self.__send_request(rq,sock)
        
        if (rs.t == 2 and rq.id == rs.id):
            return sock
        else:
            sock.close()
            raise Exception("Login error")
    
    def send_request(self,request):
        sock = self.__login()
        
        rs = self.__send_request(request,sock)
        sock.close()

        return rs