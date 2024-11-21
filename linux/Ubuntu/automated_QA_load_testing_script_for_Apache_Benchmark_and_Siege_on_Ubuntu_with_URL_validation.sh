#!/bin/ 

# Step 1: Install necessary tools
sudo apt update && sudo apt install -y apache2-utils siege

# Step 2: Define variables
URL="http://example.com/" # Replace with the actual, valid URL of the application you want to test, include the full path if needed
CONCURRENT_USERS=50
DURATION="5M"

# Step 3: Validate URL format
if [[ ! $URL =~ ^https?:// ]]; then
    echo "Invalid URL format. Please include 'http://' or 'https://' at the beginning."
    exit 1
fi

# Step 4: Run the load test using Apache Benchmark (ab)
echo "Running load test with Apache Benchmark (ab)..."
ab -n 10000 -c $CONCURRENT_USERS $URL

# Step 5: Run the load test using Siege
echo "Running load test with Siege..."
siege -c $CONCURRENT_USERS -t $DURATION $URL

# Step 6: Collect and display results
echo "Load test completed."
echo "Apache Benchmark (ab) results:"
ab -n 10000 -c $CONCURRENT_USERS $URL | grep 'Requests per second\|Time per request\|Transfer rate'

echo "Siege results:"
siege -c $CONCURRENT_USERS -t $DURATION $URL -g

# End of script
