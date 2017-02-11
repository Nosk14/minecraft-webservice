from flask import Flask
from petitions.server_info import ServerInfo
import os

app = Flask(__name__)
server_info = ServerInfo(os.environ['RCON_PASSWORD'],'sollercraft.gotes.org')
        
@app.route('/info')
def info():
    status = server_info.get_info()
    return status.to_json()
        
if __name__ == '__main__':
   app.run('0.0.0.0',5000)