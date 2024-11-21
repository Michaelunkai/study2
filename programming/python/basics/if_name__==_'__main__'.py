# # if_name_ == '__main__'
# # if __name__ == '__main__' checks if the Python script is being run directly,
# # allowing or preventing specific
# # code from executing when the script
# # is imported.

# if __name__ == '__main__':
#     pass

# print(__name__)
# output: __main__

# ------------------------------------
def main():
    print("This is the main function.")

if __name__ == '__main__':
    main()
# output: This is the main function.
# ------------------------------------
# Line 1: Define a function
def main():
    print("This is the main function. ")

# Line 5: Check if the script is run directly
if __name__ == '__main__':
    # Line 7: Call the main function
    main()


# Explanation:

# def main():: Defines a function
# named main.
# print("This is the main function."):
# Prints a message when the function is called.
# if __name__ == '__main__'::
# Checks if the script is run
# directly.
# main(): Calls the main function
# if the script is run directly.