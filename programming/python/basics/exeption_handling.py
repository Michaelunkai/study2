# exeption handling

# exception = events detected during execution that interrupt the flow of a program.
# numerator = int(input("Enter a number to divide: "))
# denominator = int(input("Enter a number to divide by: "))
# result = numerator / denominator
# print(result)
# this will allow me to divide 2 numbers

#  if ill try to divide a number with 0, ill get an error.
#  this is an "exeption"

# try:
#     numerator = int(input("Enter a number to divide: "))
#     denominator = int(input("Enter a number to divide by: "))
#     result = numerator / denominator
#     print(result)
# except Exception:
#     print("something went wrong :(")


# try:
#     numerator = int(input("Enter a number to divide: "))
#     denominator = int(input("Enter a number to divide by: "))
#     result = numerator / denominator
#     print(result)
# except ZeroDivisionError:
#     print("You cant divide by zero! cunt. ")
# except ValueError:
#     print("Enter only numbers pls")
# except Exception:
#      print("something went wrong :(")
# ------------------------------------------------------------------------
try:
    numerator = int(input("Enter a number to divide: "))
    denominator = int(input("Enter a number to divide by: "))
    result = numerator / denominator
    print(result)
except ZeroDivisionError as e:
    print(e)
    print("You cant divide by zero! cunt. ")
except ValueError as e:
    print(e)
    print("Enter only numbers pls")
except Exception as e:
    print(e)
    print("something went wrong :(")
else:
    print(result)
finally:
    print("This will always execute")

# output: Enter a number to divide: 5
# Enter a number to divide by: 111
# 0.04504504504504504
# PS C:\Users\micha> & C:/Users/micha/AppData/Local/Microsoft/WindowsApps/python3.12.exe "c:/study/python/exeption handling.py"
# Enter a number to divide: 5
# Enter a number to divide by: 0
# division by zero
# You cant divide by zero! cunt. 
# This will always execute
# PS C:\Users\micha> & C:/Users/micha/AppData/Local/Microsoft/WindowsApps/python3.12.exe "c:/study/python/exeption handling.py"
# Enter a number to divide: 5
# Enter a number to divide by: 3
# 1.6666666666666667
# 1.6666666666666667
# This will always execute