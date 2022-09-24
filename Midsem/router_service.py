import sqlite3, json, xmltodict, requests
from flask import Flask, request, Response
import xml.etree.ElementTree as ET
from time import gmtime, strftime

class sparseJSon:
    def __init__(self, json_url):
        self.json_url = json_url

    def sparse(self):
        f = open(self.json_url)
        data = json.load(f)
        return data

app = Flask(__name__)
success_code = Response(status=200)
failiure_code = Response(status=500)

config_json = sparseJSon('config.json').sparse()
DB_URL = config_json["db_url"]

class File:
    def __init__(self,file_path) -> None:
        self.file = open(file_path,'w+')
    
    def write_to_file(self,data):
        self.file.write(data)

log_file = File(config_json['log_file'])

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        
    def non_commit(self, query):        
        cursor = self.conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    # def commit(self, query):
    #     cursor = self.conn.cursor()
    #     cursor.execute(query)
    #     self.conn.commit()
    
class XMLParser:
    data = ""
    def __init__(self, req_data):
        self.data = req_data
    
    def sparse(self):
        tree = ET.ElementTree(ET.fromstring(self.data))
        xml_data = tree.getroot()
        xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')
        dic = dict(xmltodict.parse(xmlstr))
        return dic

PK = 1
@app.route('/', methods=["GET","POST"])
def home(): 
    global PK
    xml_parser = XMLParser(request.data)
    xml_msg =  xml_parser.sparse()
    msg = xml_msg['Message']

    #to fetch destination
    query = "select routeid,destination from routing_table where sender = '%s' and messagetype = '%s'" % (msg['Sender'], msg['MessageType'])
    DB = Database(DB_URL)
    tmp = DB.non_commit(query)
    destination = tmp[0][1]
    routeid = tmp[0][0]
    print(destination,"\n====================\n\n\n")
    #make change to log file
    cur_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    received_msg = '< {} > < {} > < {} > < {} >\n'.format(PK,routeid,'RECEIVED',cur_time)
    log_file.write_to_file(received_msg)
    PK+=1
    send_message = {'message': msg['Body']}
    
    resp = requests.post(destination, json = send_message)
    print('------------------',destination)
    if resp.status_code == success_code.status_code:
        print('\n\n--------------------------------\nAcknowledged & Received\n--------------------------------\n\n')
        cur_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        sent_msg = '< {} > < {} > < {} > < {} >\n'.format(PK,routeid,'SENT',cur_time)
        log_file.write_to_file(sent_msg)
        PK+=1
    else:
        print('\n\n--------------------------------\nNot Received\n--------------------------------\n\n')
    return str(resp.status_code)
if __name__ == '__main__':
    app.run(host = config_json["host"], port = int(config_json["port"]), debug = 1)


# database queries
    # query = 'PRAGMA table_info([routing_table])'
    # query = "insert into routing_table values(1, 'http://127.0.0.1:4444','type1','http://127.0.0.1:8090');"
