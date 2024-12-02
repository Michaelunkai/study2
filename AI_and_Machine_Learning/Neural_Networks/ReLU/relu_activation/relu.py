import numpy as np

def relu(x):
    return np.maximum(0, x)

# Test the ReLU function
if __name__ == "__main__":
    input_data = np.array([-2, -1, 0, 1, 2])
    output_data = relu(input_data)
    print("Input: ", input_data)
    print("Output: ", output_data)
