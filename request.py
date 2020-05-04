from public import N
class Request:
    def __init__(self, local_clock, sender):
        self.local_clock = local_clock
        self.sender = sender
        self.local_set = [False] * N # reply collected 
        self.local_set[sender] = True
        #self.local_amount = amount

    # def get_clock(self):
    #     return self.local_clock

    # def init_local_set(self):
    #     self.local_set = set([self.sender])

    # def get_amount(self):
    #    return self.local_amount

    # def get_sender_pid(self):
    #     return self.sender

    # def get_local_set(self):
    #     return self.local_set

    def update_local_set(self, new_pid):
        self.local_set[new_pid] = True

    def __lt__(self, other):
        if self.local_clock == other.local_clock:
            return self.sender < other.sender
        else:
            return self.local_clock < other.local_clock