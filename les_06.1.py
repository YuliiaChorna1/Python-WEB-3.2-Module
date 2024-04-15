# # Shared memory MANAGER example 2

# from multiprocessing import Process, Manager

# def worker(delay, val: Manager):
#     name = current_process().name
#     logger.debug("Started")
#     sleep(delay)
#     val[name] = current_process().pid
#     logger.debug("Done")


# if __name__ == '__main__':
#     with Manager() as manager:
#         m = manager.dict()
#         processes = []
#         for i in range(5):
#             pr = Process(target=worker, args=(randint(1, 3), m))
#             pr.start()
#             processes.append(pr)

#         [pr.join() for pr in processes]
#         print(m)
