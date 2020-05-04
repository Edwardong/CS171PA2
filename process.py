import re
import argparse
import threading
import queue
import socket
import time
import sys
import pickle
from client import Client
from public import P1PORT, P2PORT, P3PORT, PORTS, N, NETWORK_PORT, process_str
from request import Request

shared_queue = queue.Queue() # event queue
P_queue = queue.PriorityQueue() # mutex queue
# request_queue = queue.Queue()
# transaction_queue = queue.Queue()

""" input format:
    local event_name
    send P_i event_name """

def start_listen(port, stop_signal):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            # Read data
            msg = pickle.loads(data)
            # print("msg received", msg)
            event = {
                'type': msg['payload']['type'],
                'sender': msg['sender'],
                'foreign_clock': msg['clock'],
                'transaction': msg['payload'].get('transaction', None)
            }
            shared_queue.put(event)
            c.close()
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


        if one_event['type'] == "transfer":  # e.g. transfer 1 3
            this_client.update_clock(0)
            this_client.update_events("transfer")
            
            # Read args: receiver and amount
            arg_receiver = one_event['args'][0]
            if len(arg_receiver) == 1: # pid 0 format
                receiver = int(arg_receiver)
            else: # P1 format
                receiver = int(arg_receiver[1:]) - 1
            amount = int(one_event['args'][1])

            # Check pending transaction
            if this_client.one_transaction:
                this_client.update_events("failed to transfer")
                print('Failure: There is a pending transaction.')
                continue

            # Check balance
            if not this_client.check_valid(-amount):
                this_client.update_events("failed to transfer")
                print("Failure: You don't have enough balance")
                continue
        
            
            this_client.one_transaction = [this_client.pid, receiver, amount]

            # Create request
            print("Requesting.")
            this_client.update_clock(0)
            this_client.update_events("sending request")
            #request = Request(this_client.local_clock,this_client.pid)
            this_client.set_request()

            # Add request to my P_queue
            P_queue.put(this_client.get_request())

            # Broadcast request
            for receiver_pid in range(N):
                if receiver_pid != this_client.pid:
                    this_client.send_msg(receiver_pid, {
                        'type': 'request',
                    })



        elif one_event['type'] == "reply":
            # 这里是我收到了 "reply", 我是原本发 "request" 的人
            # Record this reply
            sender = one_event['sender']
            this_client.update_clock(one_event['foreign_clock'])
            this_client.update_events("receive reply from " + str(sender))
            this_client.get_request().update_local_set(sender)

            # Try visit mutex
            try_visit_mutex(this_client)


        elif one_event['type'] == "request":
            requester_pid = one_event['sender']
            requester_clock = one_event['foreign_clock']
            this_client.update_clock(requester_clock)
            this_client.update_events("receive request from " + str(requester_pid))

            new_request = Request(requester_clock, requester_pid)
            P_queue.put(new_request)

            # Send "reply" msg back to the requester
            this_client.update_clock(0)
            this_client.update_events("send back one reply to " + str(requester_pid))
            this_client.send_msg(requester_pid, {'type': 'reply'})


        elif one_event['type'] == "release":
            this_client.update_clock(one_event['foreign_clock'])
            this_client.update_events("receive release")
            
            P_queue.get()
            this_client.update_blockchain(one_event['transaction'])
        
            try_visit_mutex(this_client)

            
        elif one_event['type'] == "looptest":
            this_client.update_clock(0)
            this_client.update_events("looptest")
            this_client.send_msg(this_client.pid, {'type': 'test'})


def try_visit_mutex(this_client):
    if this_client.one_request \
    and all(this_client.one_request.local_set) \
    and P_queue.queue[0] \
    and P_queue.queue[0].sender == this_client.pid:
        print('Releasing. Visiting mutex.')
        this_client.update_clock(0)
        this_client.update_events("release and visit mutex")
        # Release
        for receiver_pid in range(N):
            if receiver_pid != this_client.pid:
                this_client.send_msg(receiver_pid, {
                    'type': 'release',
                    'transaction': this_client.one_transaction
                })
        this_client.update_blockchain(this_client.one_transaction)
        # Clean up
        P_queue.get()
        this_client.one_transaction = None
        this_client.one_request = None



def parse_command(input):
    args = input.split()
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', type=int)
    arg = parser.parse_args()
    this_pid = arg.pid
    process_stop = False
    listen_stop = False


    # we might not need these here
    try:
        port = PORTS[this_pid]
    except:
        print("this program doesn't support more than 3 clients. Exiting")
        exit()
    

    this_client = Client(this_pid)
    process_thread = threading.Thread(target=start_process, args=(this_client, lambda: process_stop))
    process_thread.start()
    listen_thread = threading.Thread(target=start_listen, args=(port, lambda: listen_stop))
    listen_thread.start()


    while True:
        one_event = input().split()
        if len(one_event) == 0:
            pass
        elif one_event[0] == "print":
            if one_event[1] == "blockchain":
                this_client.print_blockchain()
            elif one_event[1] == "clock":
                this_client.print_clock()
            elif one_event[1] == "balance":
                this_client.print_balance()
            elif one_event[1] == "set":
                this_client.print_set()
            elif one_event[1] == "pqueue":
                print(P_queue.queue[0].local_clock, P_queue.queue[0].sender)
        # elif one_event[:4] == "send" and int(one_event[6]) > 3:
        #     print("Invalid receiver! Please enter a valid receiver(1~3) again")
        elif one_event[0] == "quit":
            break
        else:
            shared_queue.put({
                'type': one_event[0],
                'args': one_event[1:]
            })
            # for debugging
            # print("{} has appended in the shared queue: {}\n".format(one_event,shared_queue.queue))
    
    print("stop tracking keyboard input, trying to join process_thread")
    process_stop = True
    process_thread.join()
    print("trying to join listen_thread")
    listen_stop = True
    listen_thread.join()
    exit()

