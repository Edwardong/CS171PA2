from client import Client
from request import Request
import queue


if __name__ == '__main__':
    # test_client = Client(3)
    # if test_client.update_balance(30):
    #     print("success")
    #     test_client.print_balance()
    # else:
    #     print("fail")
    #     test_client.print_balance()

    # test = (1, 2, 3, 4, 5)
    # p = [tuple("P" + str(test[i]) for i in range(len(test)))]
    # test2 = [(1, 2, 5), (2, 3, 7)]
    # p = [tuple("P" + str(item[i]) if i < 2 else "$" + str(item[i]) for i in range(len(item)))  for item in test2]
    # print(p)

    request1 = Request(1,3)
    request2 = Request(1,1)
    request3 = Request(2,3)
    request4 = Request(3,1)
    PQueue = queue.PriorityQueue()
    PQueue.put(request4)
    PQueue.put(request2)
    PQueue.put(request3)
    PQueue.put(request1)
    print('clock: {}, sender pid: {}'.format(PQueue.queue[0].local_clock, PQueue.queue[0].sender))
    #
    # while not PQueue.empty():
    #     next = PQueue.get()
    #     print('clock: {}, sender pid: {}'.format(next.local_clock, next.sender))

    # seta = set()
    # seta.add(1)
    # seta.add(3)
    # seta.add(2)
    #
    # setb = set()
    # setb.add(2)
    # setb.add(3)
    # setb.add(1)
    #
    # print(seta == setb)

    # queue = queue.Queue()
    # request1 = Request(2,1)
    # request2 = Request(4,1)
    # queue.put(request1)
    # queue.put(request2)
    #
    # queue.queue[0].update_local_set(2)
    # queue.queue[0].update_local_set(3)
    #
    # print(queue.queue[0].get_local_set())

    # client = Client(1)
    # client.update_clock(0)
    # print(client.local_clock)
    # client.get_request().update_local_set(2)
    # print(client.get_request().get_local_set())
    # client.get_request().init_local_set()
    # print(client.get_request().get_local_set())
    #client.print_clock()