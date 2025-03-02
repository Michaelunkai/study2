#!/bin/ 

# Script to set up Apache Arrow for In-Memory Data Analytics on Ubuntu without updates
# Tools used: Apache Arrow, Python, cmake, g++, pip
# This script installs necessary modules: pyarrow, pandas, numpy

# Step 1: Install required dependencies
sudo apt install -y cmake g++ wget unzip

# Step 2: Download Apache Arrow
wget https://github.com/apache/arrow/archive/refs/tags/apache-arrow-12.0.0.zip
unzip apache-arrow-12.0.0.zip
cd arrow-apache-arrow-12.0.0/cpp

# Step 3: Build and install Apache Arrow C++ libraries
mkdir release
cd release
cmake ..
make -j$(nproc)
sudo make install

# Step 4: Set up environment variables
echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH' >> ~/.bashrc
source ~/. rc

# Step 5: Install necessary Python packages
pip install pyarrow pandas numpy

# Step 6: Verify installation by printing PyArrow version
python3 -c "import pyarrow as pa; print(pa.__version__)"

# Step 7: Create example script to demonstrate Apache Arrow usage
cat << 'EOF' > example_arrow_usage.py
import pyarrow as pa
import pandas as pd

# Create a Pandas DataFrame
df = pd.DataFrame({
    'column1': [1, 2, 3, 4],
    'column2': ['a', 'b', 'c', 'd']
})

# Convert Pandas DataFrame to Apache Arrow Table
arrow_table = pa.Table.from_pandas(df)

# Print the Arrow Table
print(arrow_table)

# Save Arrow Table to a Parquet file
import pyarrow.parquet as pq
pq.write_table(arrow_table, 'example.parquet')

# Load the Parquet file into an Arrow Table
loaded_table = pq.read_table('example.parquet')

# Print the loaded Arrow Table
print(loaded_table)
EOF

# Run the example script
 3 example_arrow_usage.py
