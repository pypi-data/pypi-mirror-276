from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory
import asyncio
import json
import os
from websockets.sync.client import connect
from websockets.server import serve
from websocket import WebSocket
import time
import sys
import numpy as np
from threading import Thread

    
# Redirect sys.stdout to the custom stream

class XClient:
    def __init__(self,funcs,mode: str, ip=None, portOrInfo=None):
        '''
        init a ComClient with AI functions
        funcs: a list of AI functions
        '''
        self.cloudClient = None


        self.clients = {}
        self.blockbuffers = {}
        
        #tasks folder is for placing incoming commands
        if not os.path.exists("tasks"):
            os.mkdir("tasks")
        tasks = os.listdir("tasks")
        for task in tasks:
            os.remove(f"tasks/{task}")

        #results folder is for placing results from various AI functions, no matter binded to XClient or not
        if not os.path.exists("results"):
            os.mkdir("results")
        results = os.listdir("results")
        for result in results:
            os.remove(f"results/{result}")

        #for functions registered with XClient, create a process for each processor that will automatically listen according to there function name
        #e.g. if there is a function named "i2i" in the list, a process will be created to listen for "i2i" header tasks in the tasks folder
        for func in funcs:
            Process(target=add_listener, args=(func,)).start()
        #sending
        asyncio.get_event_loop().create_task(self.global_send())

        #listening
        if(mode == "server"):
            print("\033[93m Server started on "+ip+":"+str(portOrInfo)+" \033[0m")
            asyncio.get_event_loop().run_until_complete(serve(self.asServer_onRecv, ip, portOrInfo))

        #for client mode, connect to the cloud server, use sync websocket, async one is not working well for now
        elif(mode == "client"):
            print("\033[93m Client started \033[0m")
            self.cloudClient = WebSocket()
            self.cloudClient.connect(ip)
            self.cloudClient.send_bytes(("login     "+"0000000000"+portOrInfo).encode("utf-8"))
            login_res = self.cloudClient.recv()
            if login_res == b"login success":
                print("\033[95m===========         Login Success         ============\033[0m")
            
            Thread(target=self.connect_cloud, args=()).start()
            #asyncio.get_event_loop().create_task(self.connect_cloud(ip,portOrInfo))
        
        asyncio.get_event_loop().run_forever()




    def connect_cloud(self):
        try:
            while True:
                message = self.cloudClient.recv()
                ###### -1 should be client id, change it later
                self.global_onRecv(-1, message)
        except Exception as e:
            print("Connection closed by the server")


    async def asServer_onRecv(self, websocket):

        client_id = id(websocket)
        print(f"Client {client_id} connected")
        try:
            async for message in websocket:
                self.clients[client_id] = websocket
                self.global_onRecv(client_id, message)

        except Exception as e:
            print(f"Error in websocket communication: {e}")

    def global_onRecv(self, client_id, message):
        '''
        WebSocket Object should NOT go inside here, only client_id and message
        
        '''
        print(
            "\033[93mheader:"+
            message[:10].replace(b" ", b"").decode()+
            "   id:"+
            message[10:20].decode()+
            "   length:"+
            str(len(message[20:]))+
            "\033[0m"
        )
        # connect client and save client id

        header = message[:10].replace(b" ", b"").decode()
        task_id = message[10:20]

        if client_id not in self.blockbuffers:
            self.blockbuffers[client_id] = []

        content = message[20:]
        
        try:
            if header == "check":
                print("connect check received")
                return

            if header == "block":
                # if block, save it to buffer
                self.blockbuffers[client_id].append(content)
                print(len(self.blockbuffers[client_id]), "blocks received")
                return

            if client_id in self.blockbuffers:
                # if there is a block buffer, concat it
                self.blockbuffers[client_id].append(content)
                content = b"".join(self.blockbuffers[client_id])

                #finally write the file to tasks folder for processing from other processes
                with open(f"tasks/{client_id}.{task_id.decode()}.{header}", "wb") as f:
                    print("place task: "+f"{client_id}.{task_id.decode()}.{header}")
                    f.write(content)
                del self.blockbuffers[client_id] # clean buffer

        except Exception as e:
            print(f"Error in websocket communication: {e}")
            return

    async def global_send(self, blocksize=100000):
        print("start result->sender loop")
        loopCount = 0
        while True:
            loopCount += 1
            if loopCount % 50 == 0 and self.cloudClient is not None:
                self.cloudClient.send_bytes("check     0000000000")
                print("check to cloud")

            if len(os.listdir("results")) > 0:
                for file in os.listdir("results"):
                    try:
                        with open(f"results/{file}", "rb") as f:
                            result_data = f.read()
                        os.remove(f"results/{file}")
                        content = result_data
                        client_id, task_id, header = file.split(".")
                        client_id = int(client_id)
                
                        header = (header + " " * (10 - len(header))).encode("utf-8")
                        if isinstance(task_id, str):
                            task_id = task_id.encode("utf-8")
                        if isinstance(header, str):
                            header = header.encode("utf-8")
                        if isinstance(content, str):
                            content = content.encode("utf-8")
                        if client_id == -1:
                            print("start sending to cloud")
                            count = 0
                            totalblocks = len(content) // blocksize
                            while len(content) > blocksize:
                                Thread(target=self.cloudClient.send_bytes, args=(b"block     " + task_id + content[0:blocksize],)).start()
                                time.sleep(0.01)
                                #self.cloudClient.send_bytes(b"block     " + task_id + content[0:blocksize])
                                content = content[blocksize:]
                                print(f"sent block {count}/{totalblocks}")
                                count += 1

                            self.cloudClient.send_bytes(header + task_id + content)
                            print("sent to cloud")
                        else:
                            await self.asServer_send(client_id, header, task_id, content)

                        break # only send one result at a time
                    except Exception as e:
                        print(f"Error in sending message to websocket: {e}")
            else:
                await asyncio.sleep(0.1)

    async def asServer_send(self, client_id, header, task_id, content):
        websocket = self.clients.get(client_id)
        while len(content) > 0:
            if len(content) > 100000:
                await websocket.send(b"block     " + task_id + content[0:100000])
                content = content[100000:]
            else:
                await websocket.send(header + task_id + content)
                content = b""
            await asyncio.sleep(0.01)
        await asyncio.sleep(0.01)



def add_listener(callback, interval=0.1):
    while True:
        taskfiles = os.listdir("tasks")
        time.sleep(interval)
        found = False
        try:
            for file in taskfiles:
                client_id, task_id, header = file.split(".")
                if header == callback.__name__:
                    found = True
                    res=callback("tasks/"+file)
                    assert type(res) == bytes, "Return type must be bytes"
                    if res is not None:
                        with open("results/"+file,"wb") as f:
                            f.write(res)
                    os.remove("tasks/"+file)
        except Exception as e:
            print(f"Error in interpreting task of {callback.__name__}: {e}")



def i2i(file):
    print("i2i task received, file:",file)
    return b"i2i"

def config(file):
    print("config task received, file:",file)
    return b"hello from com test"

if __name__ == "__main__":
    
    XClient([i2i,config],"client", "wss://xing.art/com/","testuser.testuser")