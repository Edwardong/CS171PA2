import socket, threading, time, random
from public import P1PORT, P2PORT, P3PORT, NETWORK_PORT, process_str

# protocol(for easily parsing):
    # ClockreceiveSenderReceiverMsg
    # e.g.: 3receiveP1P2LetsDance


if __name__ == '__main__':

    in_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    in_sock.bind(("localhost", NETWORK_PORT))
    in_sock.listen(5)

    def send(data):
        data_copy = data # not sure if necessary
        clock, sender, receiver, message = process_str(data_copy.decode('utf-8'))
        if receiver == "P1":
            receiver_port = P1PORT
        elif receiver == "P2":
            receiver_port = P2PORT
        elif receiver == "P3":
            receiver_port = P3PORT
        time.sleep(random.random() * 1 + 4)
        out_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out_sock.connect(("localhost", receiver_port)) # safe. can have multi connections
        out_sock.sendall(data)
        out_sock.close
    
    thread_list = []
    while(True):
        stream, addr = in_sock.accept()
        data = stream.recv(1000)
        # print(data)
        #clock, sender, receiver, message = process_str(data.decode('utf-8'))
        sendtime = time.time()
        t = threading.Thread(target=send, args=(data,))
        thread_list.append(t)
        t.start()

    print("Joining all threads")
    for t in thread_list:
        t.join()
        