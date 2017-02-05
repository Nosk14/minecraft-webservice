import socket, struct

class Request:
    
    def __init__(self,id,t,payload):
        self.__id = id
        self.__t = t
        self.__payload = payload
    
    def to_bytes(self):
      format_pack = "<ii{}sxx".format(len(self.__payload))
      b = struct.pack(format_pack,self.__id,self.__t,bytes(self.__payload,'ASCII'))
      size_b = len(b)
      b = struct.pack("<i{}s".format(size_b),size_b,b)
        
      return b
      
      
class Response:
    
    def __init__(self,response):
        self.size = struct.unpack('<i',response[0:4])[0]
        data = struct.unpack('<ii{}sxx'.format(self.size-10),response[4:])
        self.id = data[0]
        self.t = data[1]
        print(str(data[2]))
        self.data = data[2].decode('UTF-8')
        
    def __str__(self):
        return "size: {} | id: {} | type: {} \ndata:\n{}".format(self.size,self.id,self.t,self.data)