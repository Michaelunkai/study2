# daemon threads

# Daemon threads run in the background.
# Automatically exit when main ends.
# Non-daemon threads block program exit.
# Used for tasks like garbage collection.
# Set with setDaemon(True).

# import threading
# import time

# def timer():
#     print()
#     count = 0 
#     while True:
#         time.sleep(1)
#         count += 1
#         print("logged in for: ", count, "seconds")

# x = threading.Thread(target=timer)
# x.start()

# answer = input("Do you wish to exit?")
# _______________________________________________
import threading
import time

def timer():
    print()
    count = 0 
    while True:
        time.sleep(1)
        count += 1
        print("logged in for: ", count, "seconds")

x = threading.Thread(target=timer, daemon=True)
x.start()

answer = input("Do you wish to exit?")


# In Python, a daemon thread runs in the background 
# and automatically exits when the main
#  program ends, suitable for tasks 
# like garbage collection. A non-daemon thread,
#  by contrast, blocks program exit,
#  requiring explicit termination, 
# and is used for tasks that should 
# complete before program termination.