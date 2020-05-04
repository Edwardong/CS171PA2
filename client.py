from typing import Dict, Any
from collections import OrderedDict
from request import Request
from public import PORTS, NETWORK_PORT, N
import socket

class Client:
    # event_queue: OrderedDict[int, str]
    # transaction: [sender, receiver, amount]

    def __init__(self, pid):
        self.balances = [10] * N
        self.pid = pid
        self.blockchain = []
        self.local_clock = 0
        self.event_queue = OrderedDict()
        self.started = False
        self.one_transaction = None # my pending transaction
        self.one_request = None # my request

    # def get_pid(self):
    #     return self.pid


    """ Mutex request functions """

    def get_request(self):
        return self.one_request

    def set_request(self):
        self.one_request = Request(self.local_clock, self.pid)


    # Block chain functions

    # def get_transaction(self):
    #     return self.one_transaction

    # def set_transaction(self, receiver, amount):
    #     self.one_transaction.append(self.pid)
    #     self.one_transaction.append(receiver)
    #     self.one_transaction.append(amount)

    # def cleanup_one_transaction(self):
    #     self.one_transaction = []

    def check_valid(self, input):
        return (self.balances[self.pid] + input) >= 0

    # def update_balance(self, input):
    #     if self.check_valid(input):
    #         self.local_balance += input
    #         return True
    #     else:
    #         return False

    def print_balance(self):
        # print("P1 ${} | P2 ${} | P3 ${}".format(*self.balances))
        print('${}'.format(self.balances[self.pid]))

    def update_blockchain(self, transaction):
        self.blockchain.append(transaction)
        self.balances[transaction[0]] -= transaction[2]
        self.balances[transaction[1]] += transaction[2]

    def print_blockchain(self):
        print( [ "P{} -> P{} ${}".format(item[0]+1, item[1]+1, item[2]) for item in self.blockchain])


    """ Lamport Clock functions """

    # Why we have to keep track of the events?
    def update_events(self, event):
        self.event_queue[self.local_clock] = event
        self.started = True

    def get_clock(self):
        return self.local_clock

    def update_clock(self, input_counter=1):
        self.local_clock = max(self.local_clock, input_counter) + 1

    def print_clock(self):
        if not self.started:
            print("0")
        else:
            #all_event = [str(i) for i in [*self.event_queue].sort()]
            print("P{} clock:".format(self.pid))
            for e in self.event_queue:
                print("[", e, "]", self.event_queue[e])
        return self.event_queue

    def print_set(self):
        print(self.one_request.get_local_set())


    """ Communication functions """
    
    def send_msg(self, receiver, payload):
        """ General purpose sender """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Communicate without network
        # s.connect(('localhost', PORTS[receiver])) # safe
        # Communicate through network
        s.connect(('localhost', NETWORK_PORT)) # safe

        msg = {
            'clock': self.local_clock,
            'sender': self.pid,
            'receiver': receiver,
            'payload': payload
        }
        import pickle
        s.send(pickle.dumps(msg))
        # print("msg sent", msg)
