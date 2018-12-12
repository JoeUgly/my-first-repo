import os, traceback, time, os

from multiprocessing import Process, Queue, Lock, Pipe
import queue


num_threads = 26
civfile = open(r'''/home/joepers/code/current/civ_crawl/civil_ny''')


keywordurlset = Queue()


allcivurls = Queue()
for civline in civfile:
    allcivurls.put(civline)

qlength = allcivurls.qsize()
tasks_that_are_done = Queue()



def crawler(allcivurls, tasks_that_are_done):
    while True:
        #lock.acquire()
        try:
            eachcivurl = allcivurls.get_nowait()
            print('here1', eachcivurl, tasks_that_are_done.qsize())
            
        except queue.Empty:
            print('here2')
            #lock.release()
            break

        else:
            keywordurlset.put(eachcivurl)
            print('here4\n\n')
            tasks_that_are_done.put('YYYYYYYYYYYYYYYYYYY' + str(os.getpid()))



if __name__ == '__main__':
    print('xxxxxxxxxxxxx', tasks_that_are_done.qsize(), qlength)

    for ii in range(num_threads):
        worker = Process(target=crawler, args=(allcivurls, tasks_that_are_done))
        worker.start()

        
    while True:
        if tasks_that_are_done.qsize() >= qlength:
            print('done', tasks_that_are_done.qsize(), qlength)
            break
        else:
            print('waiting', tasks_that_are_done.qsize(), qlength)
            time.sleep(1)


    print('YYAAAAYYY\n')

    shared_queue_list = []

    while keywordurlset.qsize() != 0:
        shared_queue_list.append(keywordurlset.get())

for i in shared_queue_list:
    print(i.strip())






















