P1PORT = 5001
P2PORT = 5002
P3PORT = 5003
PORTS = [P1PORT, P2PORT, P3PORT]
N = 3 # number of processes

NETWORK_PORT = 5006
# GLOBALSET = set([1,2,3])

def process_str(msg):
    sender_index = msg.find("P")
    sender = msg[sender_index:sender_index+2]
    receiver = msg[sender_index+2:sender_index+4]
    receive_index = msg.find("receive")
    clock = int(msg[0:receive_index])
    message = msg[sender_index+4:]
    return clock, sender, receiver, message

