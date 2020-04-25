from client import Client

if __name__ == '__main__':
    test_client = Client(3)
    if test_client.update_balance(30):
        print("success")
        test_client.print_balance()
    else:
        print("fail")
        test_client.print_balance()
    #test = (1, 2, 3, 4, 5)
    #p = [tuple("P" + str(test[i]) for i in range(len(test)))]
    # test2 = [(1, 2, 5), (2, 3, 7)]
    # p = [tuple("P" + str(item[i]) if i < 2 else "$" + str(item[i]) for i in range(len(item)))  for item in test2]
    # print(p)