from typing import Dict, Any
from collections import OrderedDict

class Client:
    #event_queue: OrderedDict[int, str]

    def __init__(self, id):
        self.local_balance = 10
        self.client_id = id
        self.blockchain = []
        # self.local_clock = 0
        # self.event_queue = OrderedDict()
        # self.started = False

    def get_pid(self):
        return self.client_id

    def check_valid(self, input):
        return (self.local_balance + input) >= 0

    def update_balance(self, input):
        if self.check_valid(input):
            self.local_balance += input
            return True
        else:
            return False

    def print_balance(self):
        print("${}".format(self.local_balance))

    def update_blockchain(self, transaction):
        self.blockchain.append(transaction)

    def print_blocakchain(self):
        p = [tuple("P" + str(item[i]) if i < 2 else "$" + str(item[i]) for i in range(len(item))) for item in self.blockchain]
        print(p)

    # def update_events(self, event):
    #     self.event_queue[self.local_clock] = event
    #     self.started = True

    # def update_clock(self, input_counter=1):
    #     self.local_clock = max(self.local_clock, input_counter) + 1

    # def print_clock(self):
    #     if not self.started:
    #         print("0")
    #     else:
    #         #all_event = [str(i) for i in [*self.event_queue].sort()]
    #         print("P{} clock:".format(self.client_id))
    #         for e in self.event_queue:
    #             print("[", e, "]", self.event_queue[e])
    #     return self.event_queue

