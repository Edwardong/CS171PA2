import re
import argparse
import threading
import queue
import socket
import time
import sys
from client import Client
from public import P1PORT, P2PORT, P3PORT, PORTS, N, GLOBALSET, NETWORK_PORT, process_str
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
            # shared_queue.put("recv " + data.decode('utf-8'))
            # Read data
            import pickle
            msg = pickle.loads(data)
            print("msg received", msg)
            event = {
                'type': msg['payload']['type'],
                'sender': msg['sender'],
                'foreign_clock': msg['clock'],
                'transaction': msg['payload'].get('transaction', None)
            }
            print("event", event)
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

        #this part ↓ has been tested
        if one_event['type'] == "transfer":  # e.g. transfer 1 3
            this_client.update_clock(0)
            this_client.update_events("transfer")
            receiver = int(one_event['args'][0])
            amount = int(one_event['args'][1])

            # Check pending transaction
            # TODO

            # Check balance
            if not this_client.check_valid(-amount):
                this_client.update_events("failed to transfer")
                print("You don't have enough balance")
                continue
        
            #this part ↑ has been tested
            
            this_client.set_transaction(receiver,amount)

            # Create request
            print("requesting")
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

            #request_queue.put(this_client.get_request())

            # TO-DO: send the request to Network node and Network node would broadcast
            # TO-DO: send_request(request)

        # this part ↓ has been tested
        elif one_event['type'] == "reply":
            # 这里是我收到了 "reply", 我是原本发 "request" 的人
            # format: reply Pn Pm Clock (Pn is the one receives "request" and sends back "reply")
            # Record this reply
            from_pid = one_event['sender']
            this_client.update_clock(one_event['foreign_clock'])
            this_client.update_events("receive reply from " + str(from_pid))
            this_client.get_request().update_local_set(from_pid)
            print('local_set', this_client.one_request.local_set)
        # this part ↑ has been tested

            # Try visit mutex
            # TODO
            if all(this_client.one_request.local_set) and P_queue.queue[0].sender == this_client.pid:
                print('all collected')
                # Release
                for receiver_pid in range(N):
                    if receiver_pid != this_client.pid:
                        this_client.send_msg(receiver_pid, {
                            'type': 'release',
                            'transaction': this_client.one_transaction
                        })
                

            # If there's a held-reply for that process, sent it 
            # TODO


        # this part ↓ has been tested
        elif one_event['type'] == "request":
            # format: request Pn Clock
            requester_pid = one_event['sender']
            requester_clock = one_event['foreign_clock']
            this_client.update_clock(requester_clock)
            this_client.update_events("receive request from " + str(requester_pid))

            new_request = Request(requester_clock, requester_pid)
            P_queue.put(new_request)

            # Check time, compare with my request
            # TODO

        # this part ↑ has been tested

            # TODO: send "reply" msg back to the sender
            this_client.update_clock(0)
            this_client.update_events("send back one reply to " + str(requester_pid))
            this_client.send_msg(requester_pid, {'type': 'reply'})


        # this part ↓ has been tested
        elif one_event['type'] == "release":
            # format: release sender receiver Clock Amount
            this_client.update_clock(one_event['foreign_clock'])
            this_client.update_events("receive release from")
            
            # Pop P_queue
            P_queue.get()

            # Update blockchain
            this_client.update_blockchain(one_event['transaction'])
            if one_event['transaction'][1] == this_client.pid:
                this_client.update_balance(one_event['transaction'][2])
        
        # this part ↑ has been tested
            
            # Try visit mutex
            # TODO
            
        elif one_event['type'] == "looptest":
            this_client.update_clock(0)
            this_client.update_events("looptest")
            this_client.send_msg(this_client.pid, {'type': 'test'})


# TO-DO
def send_request(request):
    return

# TO-DO
def send_reply(local_clock, local_pid):
    return

def add_block(this_client,stop_signal):
    while True:
        if stop_signal():
            break
        else:
            pass
        if P_queue.empty():
            continue
        if not P_queue.queue[0].sender == this_client.pid or not this_client.get_request().get_local_set() == GLOBALSET:
            continue
        else:
            # this part ↓ has been tested
            request = P_queue.get()
            print("After popping out the first element in P_queue: clock: {}, pid:{}".format(request.local_clock,request.sender))
            this_client.get_request().init_local_set()
            transaction = this_client.get_transaction()
            print("before consuming the transaction: {}".format(transaction))
            sender = transaction[0]
            receiver = transaction[1]
            amount = int(transaction[2])
            this_client.cleanup_one_transaction()
            print("cleanup the transaction: {}".format(this_client.get_transaction()))
            if this_client.update_balance(-amount):
                this_client.update_blockchain(transaction)
            else:
                print("invalid transaction")
            msg = "release p" + str(sender)+ " " + str(receiver) + " " + str(amount)
            print("broadcasting message: " + msg)
            # this part ↑ has been tested
            # TO-DO: broadcast msg: "release sender_pid receiver_pid amount"



def parse_command(input):
    args = input.split()
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', type=int)
    arg = parser.parse_args()
    this_pid = arg.pid
    process_stop = False
    listen_stop = False

    #for testing:
    #P_queue.put(Request(1,"p1"))
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
    # add_block_thread = threading.Thread(target=add_block, args=(this_client, lambda: process_stop))
    # add_block_thread.start()

    while True:
        one_event = input().split()
        if one_event[0] == "print":
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
    # for debugging
    print("stop tracking keyboard input, trying to join process_thread")
    process_stop = True
    process_thread.join()
    add_block_thread.join()

    listen_stop = True
    print("trying to join listen_thread")
    listen_thread.join()
    exit()

