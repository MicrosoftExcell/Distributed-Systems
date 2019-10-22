# Server3.py
import Pyro4
import random
import csv

server2 = Pyro4.Proxy("PYRONAME:example.server2")
server1 = Pyro4.Proxy("PYRONAME:example.server1")

with open("ratings.csv") as file: #read in ratings
    reader = csv.reader(file,delimiter=',')
    lines = 0
    entries = []
    for row in reader:
        if lines == 0:
            lines+=1
        else:
            entries.append([])
            entries[-1].append(row[1])
            entries[-1].append(row[2])
            lines+=1
file.close()

value_timestamp = [0,0,0]
update_log = []
replica_timestamp = [0,0,0]
executed_op_table = []
timestamp_table = [[0,0,0],[0,0,0],[0,0,0]]

def checkID(x):
    return x[-1]

def process_updates():
    print("processing")
    stable = []
    for i in range(len(update_log)): # check which updates are stable
        if update_log[i][4][0]<=value_timestamp[0]:
            if update_log[i][4][1]<=value_timestamp[1]:
                if update_log[i][4][2]<=value_timestamp[2]:
                    found = False
                    for j in range(len(executed_op_table)): #check not already applied
                        if update_log[i][-1] == executed_op_table[j]:
                            found = True
                    if found == False:
                        stable.append(update_log[i])
    stable = sorted(stable,key=checkID) # sort into order of update
    for i in range(len(stable)):
        found = False
        for j in range(len(entries)): # if updating rating
            if entries[j][0] == stable[i][2]:
                entries[j][1] = stable[i][3]
                value_timestamp[stable[i][0]]+=1
                executed_op_table.append(stable[i][-1])
                found = True
        if found == False: # if new rating
            entries.append([stable[i][2],stable[i][3]])
            value_timestamp[stable[i][0]]+=1
            executed_op_table.append(stable[i][-1])
    
@Pyro4.expose
class obj(object):
    def status(self): #report status
        self.num = random.randint(0,2)
        if self.num == 0:
            print("active")
            return "active"
        elif self.num == 1:
            print("over-loaded")
            return "over-loaded"
        else:
            print("offline")
            return "offline"
    def get_updates(self): #send updates to another server
        return replica_timestamp,update_log
    def check_updates(self,server): # add new updates to update log if not there or executed
        if server == 0:
            new_timestamp,new_updates = server1.get_updates()
        elif server == 1:
            new_timestamp,new_updates = server2.get_updates()
        else:
            new_timestamp,new_updates = server3.get_updates()
        timestamp_table[server] = new_timestamp
        for k in range(len(new_updates)):
            found = False
            for l in range(len(update_log)):
                if new_updates[k][-1] == update_log[l][-1]:
                    found = True
                    break
            for l in range(len(executed_op_table)):
                if new_updates[k][-1] == executed_op_table[l]:
                    found = True
                    break
            if found == False:
                update_log.append(new_updates[k])
                replica_timestamp[server]+=1
    def retrieve(self,movieID,timestamp):
        server = 2
        if timestamp[2]<=value_timestamp[2]: #check value has all previous updates from client
            if timestamp[1]<=value_timestamp[1]:
                if timestamp[0]<=value_timestamp[0]:
                    found = False
                    for j in range(len(entries)):
                        if entries[j][0] == movieID:
                            rating = entries[j][1]
                            found = True
                            break
                    if found == False:
                        return "0",value_timestamp 
                    else:
                        return rating,value_timestamp
                else:
                    self.check_updates(0)
            else:
                self.check_updates(1)
                self.check_updates(0)
        else:
            self.check_updates(1)
            self.check_updates(0)
        process_updates()
        return self.retrieve(movieID,timestamp)
    def update(self,opID,movieID,rating,timestamp):
        print("updating")
        server = 2
        for i in range(len(executed_op_table)): #if not already executed or in update log
            if executed_op_table[i] == opID:
                return True,timestamp 
        for i in range(len(update_log)):
            if update_log[i][-1] == opID:
                return True,timestamp
        replica_timestamp[server]+=1
        ts = [timestamp[0],timestamp[1],replica_timestamp[2]]
        update_log.append([server,ts,movieID,rating,timestamp,opID])
        process_updates()
        return True,ts
        

daemon = Pyro4.Daemon()        # make a Pyro daemon
ns = Pyro4.locateNS()
uri = daemon.register(obj)   # register the object as a Pyro object
ns.register("example.server3", uri)

print("Connected")
daemon.requestLoop()

        
