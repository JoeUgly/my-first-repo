

import os, traceback, time, os

from multiprocessing import Process, Queue, Lock
import queue


num_threads = 26
civfile = open(r'''C:\Users\jschiffler\Desktop\Text_n_Stuff\current\civil_ny.txt''')


allcivurls = Queue()
for civline in civfile:
    allcivurls.put(civline)

qlength = allcivurls.qsize()
tasks_that_are_done = Queue()




def crawler(allcivurls, tasks_that_are_done, lock):
    while True:
        lock.acquire()
        try:
            eachcivurl = allcivurls.get_nowait()
            print('here1', eachcivurl, tasks_that_are_done.qsize())
            
        except queue.Empty:
            print('here2')
            lock.release()
            break

        else:
            print('here3')

            print('here4\n\n')
            tasks_that_are_done.put('YYYYYYYYYYYYYYYYYYY' + str(os.getpid()))
            lock.release()





if __name__ == '__main__':
    lock = Lock()
    print('xxxxxxxxxxxxx', tasks_that_are_done.qsize(), qlength)

    print('join_count')



    for ii in range(num_threads):
        worker = Process(target=crawler, args=(allcivurls, tasks_that_are_done, lock))
        worker.start()



        
    while True:
        if tasks_that_are_done.qsize() >= qlength:
            print('done', tasks_that_are_done.qsize(), qlength)
            break
        else:
            print('waiting', tasks_that_are_done.qsize(), qlength)
            time.sleep(1)


    print('YYAAAAYYY')

























