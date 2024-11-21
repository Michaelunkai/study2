# # # # time module
# # # # time module in Python provides
# # # # functions to work with time, 
# # # # including delays, measuring
# # # # execution time, and formatting
# # # # timestamps.

# # # # Prints Epoch time as a string:
# # # # import time

# # # # print(time.ctime(0))
# # # # output: Thu Jan  1 00:00:00 1970

# # # # Epoch refers to the starting point for
# # # # measuring time in computing.
# # # # It is often set to
# # # # January 1, 1970 (00:00:00 UTC),
# # # # and time is represented as the
# # # # number of seconds elapsed
# # # # since then.
# # # import time

# # # print(time.ctime(1000000)) # convert a time expressed in seconds since epoch to a readable string
# # # #  epoch = when my pc thinks time began (reference point)

# # # # output: Mon Jan 12 13:46:40 1970
# # # ________________________________________________

# # import time
# # print(time.time()) #returm current seconds since epoch
# # # output: 1705403161.0874536
# # # ________________________________________________

# import time

# print(time.ctime(time.time()))
# # this will print the current date and time

# _____________________________________________
import time

time_object = time.localtime()
print(time_object)
# output: time.struct_time(tm_year=2024, tm_mon=1, tm_mday=16, tm_hour=11, tm_min=10, tm_sec=52, tm_wday=1, tm_yday=16, tm_isdst=0)
