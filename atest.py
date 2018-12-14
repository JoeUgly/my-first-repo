from multiprocessing import Process, Queue, Lock, Manager








with Manager() as manager:
    errorurls_man_list = manager.dict()

    eachcivurl = 'nystate.com'
    errex = '404 not found'


    errorurls_man_list[eachcivurl] = 'error 1: ' + str(errex)

    errorurls_list = {}




    for k, v in errorurls_man_list.items():
        vk = str((v, '::', k))
        errorurls_list[v] = k




print(errorurls_list.items())




