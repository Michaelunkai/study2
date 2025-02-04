#!/bin/ 

# Script: install_setup_and_run_datafusion_pipeline_on_ubuntu.sh
# Description: Installs dependencies, sets up Apache Arrow DataFusion in Rust, creates a data pipeline, and runs a sample query on Ubuntu.

set -e  # Exit immediately if a command exits with a non-zero status.

echo "Starting the setup of Apache Arrow DataFusion on Ubuntu..."

# Step 1: Install Essential Dependencies
echo "Installing build-essential and curl..."
sudo apt update
sudo apt install -y build-essential curl

# Step 2: Install Rust using rustup
echo "Installing Rust programming language..."
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Configure the current shell to use Rust
echo "Configuring Rust environment..."
source "$HOME/.cargo/env"

# Verify Rust installation
echo "Verifying Rust installation..."
rustc --version

# Step 3: Create a New Rust Project
echo "Creating a new Rust project named 'datafusion_pipeline'..."
cargo new datafusion_pipeline
cd datafusion_pipeline

# Step 4: Add DataFusion and Tokio Dependencies
echo "Adding DataFusion and Tokio dependencies to Cargo.toml..."
# Use 'sed' to insert dependencies after the [dependencies] section header
sed -i '/^\[dependencies\]/a datafusion = "23.0.0"\ntokio = { version = "1.28", features = ["full"] }' Cargo.toml

# Step 5: Create Sample Data Directory and sales.csv
echo "Creating sample data directory and sales.csv file..."
mkdir -p data
cat << EOF > data/sales.csv
id,region,amount
1,North,100
2,South,150
3,East,200
4,West,130
5,North,170
EOF

# Step 6: Write the Rust Application Code to src/main.rs
echo "Writing Rust application code to src/main.rs..."
cat << 'EOF' > src/main.rs
use datafusion::prelude::*;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Initialize the execution context
    let ctx = SessionContext::new();

    // Register a CSV file as a table
    ctx.register_ ("sales", "data/sales. ", CsvReadOptions::new()).await?;

    // Create a SQL query
    let df = ctx.sql("SELECT region, SUM(amount) as total_sales FROM sales GROUP BY region").await?;

    // Execute the query and collect results
    let results = df.collect().await?;

    // Display the results
    for batch in results {
        println!("{:?}", batch);
    }

    Ok(())
}
EOF

# Step 7: Build the Project
echo "Building the DataFusion project..."
cargo build --release

# Step 8: Run the Tool After the Script Completes
echo "Running the DataFusion project..."
cargo run --release

echo "DataFusion setup, build, and execution completed successfully!"
