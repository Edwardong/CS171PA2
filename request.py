class Request:
    def __init__(self, local_clock, sender_pid):
        self.local_clock = local_clock
        self.sender_pid = sender_pid

    def __lt__(self, other):
        if self.local_clock == other.local_clock:
            return self.sender_pid < other.sender_pid
        else:
            return self.local_clock < other.local_clock