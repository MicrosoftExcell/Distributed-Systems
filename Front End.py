# Front End.py
import Pyro4

server1 = Pyro4.Proxy("PYRONAME:example.server1")
server2 = Pyro4.Proxy("PYRONAME:example.server2")
server3 = Pyro4.Proxy("PYRONAME:example.server3")

timestamp = [0,0,0]

def check_status(): #check status of servers
    server = 0
    found = False
    while found == False:
        if server1.status() == "active":
            server = 1
            found = True
        elif server2.status() == "active":
            server = 2
            found = True
        elif server3.status() == "active":
            server = 3
            found = True
    return server

opID = 0

@Pyro4.expose
class obj(object):
    def retrieve(self,movieID): #query active server
        server = check_status()
        if server == 1:
            rating,new_stamp = server1.retrieve(movieID,timestamp)
        elif server == 2:
            rating,new_stamp = server2.retrieve(movieID,timestamp)
        else:
            rating,new_stamp = server3.retrieve(movieID,timestamp)
        for i in range(len(new_stamp)): #merge timestamps
            if timestamp[i]<new_stamp[i]:
                timestamp[i] = new_stamp[i]
        return rating #return to client
    def update(self,movieID,rating):
        global opID
        server = check_status()
        opID += 1 #unique operation ID
        if server == 1:
            done,new_stamp = server1.update(opID,movieID,rating,timestamp)
        elif server == 2:
            done,new_stamp = server2.update(opID,movieID,rating,timestamp)
        else:
            done,new_stamp = server3.update(opID,movieID,rating,timestamp)
        for i in range(len(new_stamp)): #merge timestamps
            if timestamp[i]<new_stamp[i]:
                timestamp[i] = new_stamp[i]
        return done #return to client

daemon = Pyro4.Daemon()        # make a Pyro daemon
ns = Pyro4.locateNS()
uri = daemon.register(obj)  
ns.register("example.front_end", uri)

print("Front End Ready")
daemon.requestLoop()    # start the event loop of the server to wait for calls
