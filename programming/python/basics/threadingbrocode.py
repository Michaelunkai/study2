# # # threading
# # # Threading in Python allows
# # # concurrent execution of tasks,
# # # improving performance by running
# # # multiple threads simultaneously 
# # # within a single process.

# # # CPU-bound: Task limited by processor speed, computation-heavy,
# # # minimal I/O operations.

# # # I/O-bound: Task constrained by input/output operations, frequent data access,
# # #  waiting for external resources.

# # import threading
# # import time
# # print(threading.active_count())
# # # output: 1

# import threading
# import time

# print(threading.active_count())
# print(threading.enumerate())
# # output : 1
# # [<_MainThread(MainThread, started 140042503404416)>]

# with multithreathing

# import threading
# import time

# def eat_breakfast():
#     time.sleep(3)
#     print("you eat breakfast")

# def drink_coffee():
#     time.sleep(4)
#     print("You drank coffee")

# def study():
#     time.sleep(5)
#     print("You study")

# print(threading.active_count())
# print(threading.enumerate())

# output: 1
# [<_MainThread(MainThread, started 140313416461184)>]


# import threading
# import time

# def eat_breakfast():
#     time.sleep(3)
#     print("you eat breakfast")

# def drink_coffee():
#     time.sleep(4)
#     print("You drank coffee")

# def study():
#     time.sleep(5)
#     print("You study")

# eat_breakfast()
# drink_coffee()
# study()

# print(threading.active_count())
# print(threading.enumerate())

# output: you eat breakfast
# You drank coffee
# You study
# 1
# [<_MainThread(MainThread, started 140029643234176)>]

# create additional thread:

import threading
import time

def eat_breakfast():
    time.sleep(3)
    print("you eat breakfast")

def drink_coffee():
    time.sleep(4)
    print("You drank coffee")

def study():
    time.sleep(5)
    print("You study")

x = threading.Thread(target=eat_breakfast,args=())
x.start()
# this thead in charge of eating breakfast
# second thread, for coffee:

y = threading.Thread(target=drink_coffee,args=())
y.start()

#for study:

z = threading.Thread(target=study,args=())
z.start()

# eat_breakfast()
# drink_coffee()
# study()

print(threading.active_count())
print(threading.enumerate())

# output:
# 4
# [<_MainThread(MainThread, started 140539890830208)>, <Thread(Thread-1, started 140539888481984)>, <Thread(Thread-2, started 140539880089280)>, <Thread(Thread-3, started 140539871696576)>]
# you eat breakfast
# You drank coffee
# You study
