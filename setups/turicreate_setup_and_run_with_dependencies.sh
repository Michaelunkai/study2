#!/bin/ 

# Step 1: Add deadsnakes PPA to install Python 3.8
echo "Adding PPA for Python 3.8"
sudo apt install -y software-properties-common
sudo apt install -y python3-apt
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Step 2: Install Python 3.8 and necessary dependencies
echo "Installing Python 3.8 and necessary dependencies"
sudo apt install -y python3.8 python3.8-dev python3.8-distutils \
build-essential libssl-dev libffi-dev libomp-dev libomp-14-dev libomp5-14

# Step 3: Install Pip for Python 3.8
echo "Installing pip for Python 3.8"
curl -sS https://bootstrap.pypa.io/pip/3.8/get-pip.py -o get-pip.py
 3.8 get-pip.py

# Step 4: Upgrade Pip
echo "Upgrading pip to the latest version"
python3.8 -m pip install --upgrade pip

# Step 5: Install a compatible version of Turi Create
echo "Installing Turi Create"
python3.8 -m pip install turicreate==6.4

# Step 6: Download Iris dataset
echo "Downloading Iris dataset"
wget -q https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data -O iris.csv

# Step 7: Create a Python script to run a simple Turi Create example with Iris dataset
echo "Creating the Turi Create example script"
cat <<EOL > simple_turicreate_example.py
import turicreate as tc

# Load the iris dataset
data = tc.SFrame.read_csv('iris.csv', header=False)
data = data.rename({'X1': 'sepal_length', 'X2': 'sepal_width',
                    'X3': 'petal_length', 'X4': 'petal_width', 'X5': 'class'})

# Split the data into training and testing sets
train_data, test_data = data.random_split(0.8)

# Create a simple classifier
model = tc.classifier.create(train_data, target='class')

# Evaluate the model
metrics = model.eva te(test_data)
print("Accuracy:", metrics['accuracy'])

# Save the model
model.save('iris_classifier.model')
EOL

# Step 8: Run the Turi Create example
echo "Running the Turi Create example script"
 3.8 simple_turicreate_example.py
