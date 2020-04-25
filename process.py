import re
import argparse
import threading
import queue
import socket
import time
import sys
from client import Client
from public import P1PORT, P2PORT, P3PORT, NETWORK_PORT, process_str

shared_queue = queue.Queue()
msg_queue = queue.Queue()

""" input format:
    local event_name
    send P_i event_name """


# def process_str(input):
#     rule = re.compile(r"[^a-zA-Z0-9]")
#     message = ''
#     if input[:5] == "local":
#         input_list = input.strip().split()
#         event = input[6:]
#         for i in range(len(input_list)):
#             input_list[i] = rule.sub('',input_list[i])
#         return ("local", event, message)
#     else:
#         receiver = input[5:7]
#         message = input[8:]
#         return ("send", receiver, message)

def start_listen(port, stop_signal):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = socket.gethostname()
    s.bind(('', port))
    s.listen(5)
    print("start listening")
    while True:
        if shared_queue.empty():
            if stop_signal():
                print("listen thread exiting")
                break
        s.settimeout(2.0)
        try:
            c, addr = s.accept()
            data = c.recv(1024)
            # print("can I receive data? Data: {}".format(data)) # debug
            # print(data)
            shared_queue.put("recv " + data.decode('utf-8'))
            c.close()
            # else:
            #     print("should stop listening2")
            #     #c.close()
            #     break
        except Exception:
            pass
    return


# Finished with no deadlock
def start_process(this_client, stop_signal):
    while True:
        while shared_queue.empty():
            if stop_signal():
                #print("process exiting from 1")
                break
            else:
                pass
        if not shared_queue.empty():
            one_event = shared_queue.get()
        else:
            #print("process exiting from 2")
            break
        # for debugging
        # print("{} has poped from the shared queue: {}\n".format(one_event,shared_queue.queue))

        if one_event[:5] == "local":  # e.g. local Wakeup
            # where = "local"
            event = one_event[6:]
            this_client.update_clock(0)
            this_client.update_events("local: " + event)
        elif one_event[:4] == "send":
            # where = "remote"
            receiver = one_event[5:7]
            message = one_event[8:]
            this_client.update_clock(0)
            this_client.update_events("send " + receiver + ": " + message)
            send_msg("localhost", NETWORK_PORT, this_client.get_clock(), message, this_client.get_pid(), receiver)
        elif one_event[:4] == "recv":
            clock, sender, receiver, message = process_str(one_event[5:])
            this_client.update_clock(clock)
            this_client.update_events("receive " + sender + ": " + message)
            

def send_msg(host, port, local_clock, msg, sender, receiver):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # time.sleep(5)
    # communication process needs these
    # if receiver == "P1" or receiver == "p1":
    #     port = P1PORT
    # elif receiver == "P2" or receiver == "p2":
    #     port = P2PORT
    # elif receiver == "P3" or receiver == "p3":
    #     port = P3PORT
    # else:
    #     print("error receiver id")
    #     return
    s.connect((host, port))
    # protocol(for easily parsing):
    # ClockreceiveSenderReceiverMsg
    # e.g.: 3receiveP1P2LetsDance
    payload = str(local_clock) + "receiveP" +  str(sender) + str(receiver) + msg
    s.send(payload.encode('utf-8'))
    print("sent.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('port',type=int)
    parser.add_argument('pid', type=int)
    arg = parser.parse_args()
    # port = arg.port
    this_pid = arg.pid
    process_stop = False
    listen_stop = False

    # we might not need these here
    if this_pid == 1:
        port = P1PORT
    elif this_pid == 2:
        port = P2PORT
    elif this_pid == 3:
        port = P3PORT
    else:
        print("this program doesn't support more than 3 clients. Exiting")
        exit()

    this_client = Client(this_pid)
    process_thread = threading.Thread(target=start_process, args=(this_client, lambda: process_stop))
    process_thread.start()
    listen_thread = threading.Thread(target=start_listen, args=(port, lambda: listen_stop))
    listen_thread.start()

    while True:
        one_event = input()
        if one_event[:5] == "print":
            this_client.print_clock()
        elif one_event[:4] == "send" and int(one_event[6]) > 3:
            print("Invalid receiver! Please enter a valid receiver(1~3) again")
        elif one_event[:4] == "quit":
            break
        else:
            shared_queue.put(one_event)
            # for debugging
            # print("{} has appended in the shared queue: {}\n".format(one_event,shared_queue.queue))
    # for debugging
    print("stop tracking keyboard input, trying to join process_thread")
    process_stop = True
    process_thread.join()

    listen_stop = True
    print("trying to join listen_thread")
    listen_thread.join()
    exit()

