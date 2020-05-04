import socket, threading, time, random
from public import P1PORT, P2PORT, P3PORT, PORTS, NETWORK_PORT, process_str
import pickle

# protocol(for easily parsing):
    # ClockreceiveSenderReceiverMsg
    # e.g.: 3receiveP1P2LetsDance


if __name__ == '__main__':

    in_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    in_sock.bind(("localhost", NETWORK_PORT))
    in_sock.listen(5)

    def send(data):
        data_copy = data # not sure if necessary
        msg = pickle.loads(data)
        receiver_port = PORTS[msg['receiver']]
        time.sleep(1)
        out_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out_sock.connect(("localhost", receiver_port)) # safe. can have multi connections
        out_sock.sendall(data_copy)
        out_sock.close
    
    thread_list = []
    while(True):
        stream, addr = in_sock.accept()
        data = stream.recv(1024)
        t = threading.Thread(target=send, args=(data,))
        thread_list.append(t)
        t.start()

    print("Joining all threads")
    for t in thread_list:
        t.join()
        