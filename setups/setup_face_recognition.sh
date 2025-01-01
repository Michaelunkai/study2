#!/bin/ 

# Step 1: Install necessary dependencies (without sudo apt update)
echo "Installing necessary dependencies..."
sudo apt install -y build-essential cmake python3-dev libboost-python-dev libboost-system-dev

# Step 2: Install dlib
echo "Cloning dlib repository..."
git clone https://github.com/davisking/dlib.git
cd dlib

echo "Installing dlib..."
 3 setup.py install

cd ..

# Step 3: Install face_recognition
echo "Installing face_recognition library..."
pip3 install face_recognition

# Step 4: Verify Installation
echo "Verifying face_recognition installation..."
python3 -c "import face_recognition; print('Installation successful!')"

# Step 5: Create and Echo the Python face detection script
echo "Creating face detection script..."

echo 'import face_recognition

# Load an image with faces
image = face_recognition.load_image_file("your_image.jpg")

# Find all the faces in the image
face_locations = face_recognition.face_locations(image)

# Print the locations of the faces
for face_location in face_locations:
    top, right, bottom, left = face_location
    print(f"Found a face at location Top: {top}, Right: {right}, Bottom: {bottom}, Left: {left}")' > face_detect.py

# Step 6: Run the Face Detection Script
echo "Running face detection script..."
 3 face_detect.py
