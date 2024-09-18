import re
from datetime import datetime

# Log file path
log_file_path = '/mnt/c/Users/micha/Downloads/exam.log'

# Function to parse timestamp
def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M:%S.%f")

# Initialize variables
transactions = {}
fastest_time = float('inf')
fastest_id = None

# Regular expression patterns to identify the start and end of a transaction
begin_pattern = re.compile(r'transaction (\d+) begun')
done_pattern = re.compile(r'transaction done, id=(\d+)')

# Read the log file and process each line
with open(log_file_path, 'r') as file:
    for line in file:
        # Extract the timestamp from the beginning of the line
        timestamp_str = line.split('\t')[0]
        timestamp = parse_timestamp(timestamp_str)

        # Check for transaction begun
        begin_match = begin_pattern.search(line)
        if begin_match:
            transaction_id = begin_match.group(1)
            transactions[transaction_id] = timestamp

        # Check for transaction done
        done_match = done_pattern.search(line)
        if done_match:
            transaction_id = done_match.group(1)
            if transaction_id in transactions:
                start_time = transactions.pop(transaction_id)
                end_time = timestamp

                # Calculate the duration in milliseconds
                duration = (end_time - start_time).total_seconds() * 1000

                # Check if this is the fastest transaction
                if duration < fastest_time:
                    fastest_time = duration
                    fastest_id = transaction_id

# Output the ID of the fastest transaction
if fastest_id:
    print(f"The fastest transaction ID is: {fastest_id}")
else:
    print("No transactions found.")
