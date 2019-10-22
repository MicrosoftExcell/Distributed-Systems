pip install Pyro4 (if Pyro4 not installed)
to start name server: 
pyro4-ns
in the command prompt. 
Navigate to the folder and use:
python Server1.py
python Server2.py
python Server3.py
python "Front End.py"
to start the servers and front end.
python Client.py
to start the client
Wait for "Connected" to appear for the servers and "Front End Ready" to appear for the front end before entering anything for the client. When ready, select the appropriate option from the menu.
May sometimes take a few seconds to connect/recieve all the updates

Description:
There is a high degree of consistency as the gossip messages are sent between servers when a query is made and the timestamp of the front-end > value timestamp of the server, meaning that there are updates the server hasn’t processed yet. The server receives gossip messages (update logs and replica timestamps) from other servers and processes any stable updates until the front-end timestamp = value timestamp and so the client will always receive the latest version of the ratings. Before updates are added to the update log, they are checked to see whether or not they are already in the update log or have been executed before by comparing the unique operation IDs given to them by the front-end. Updates are stored in the form [server sent to, timestamp, movieID, rating, front-end timestamp, operation ID] for easy comparison between updates. The ordering is sequential as before stable updates are processed, they are sorted so that the happened-before relation is observed. The front-end chooses a server by checking the status of servers in the order 1,2,3,1… and so on until one reports it’s active (status randomly chosen between active, over-loaded and offline). There is high availability as the servers exchange gossip messages only when it’s necessary for the result of a query.
