class Request:
    def __init__(self, local_clock, sender_pid):
        self.local_clock = local_clock
        self.sender_pid = sender_pid
        self.local_set = set([self.sender_pid])
        #self.local_amount = amount

    def get_clock(self):
        return self.local_clock

    def init_local_set(self):
        self.local_set = set([self.sender_pid])

    def get_amount(self):
        return self.local_amount

    def get_sender_pid(self):
        return self.sender_pid

    def get_local_set(self):
        return self.local_set

    def update_local_set(self,new_pid):
        self.local_set.add(new_pid)

    def __lt__(self, other):
        if self.local_clock == other.local_clock:
            return self.sender_pid < other.sender_pid
        else:
            return self.local_clock < other.local_clock