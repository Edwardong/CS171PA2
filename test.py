from client import Client
from request import Request
from queue import PriorityQueue

if __name__ == '__main__':
    # test_client = Client(3)
    # if test_client.update_balance(30):
    #     print("success")
    #     test_client.print_balance()
    # else:
    #     print("fail")
    #     test_client.print_balance()

    #test = (1, 2, 3, 4, 5)
    #p = [tuple("P" + str(test[i]) for i in range(len(test)))]
    # test2 = [(1, 2, 5), (2, 3, 7)]
    # p = [tuple("P" + str(item[i]) if i < 2 else "$" + str(item[i]) for i in range(len(item)))  for item in test2]
    # print(p)

    # request1 = Request(1,3)
    # request2 = Request(1,1)
    # request3 = Request(2,3)
    # request4 = Request(3,1)
    # PQueue = PriorityQueue()
    # PQueue.put(request4)
    # PQueue.put(request2)
    # PQueue.put(request3)
    # PQueue.put(request1)
    #
    # while not PQueue.empty():
    #     next = PQueue.get()
    #     print('clock: {}, sender pid: {}'.format(next.local_clock, next.sender_pid))
