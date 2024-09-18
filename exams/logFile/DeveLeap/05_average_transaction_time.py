import re
from datetime import datetime

# Log file path
log_file_path = '/mnt/c/Users/micha/Downloads/exam.log'

# Function to parse timestamp
def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M:%S.%f")

# Initialize variables
transactions = {}
total_time = 0
transaction_count = 0

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

                # Add to the total time and increment the transaction count
                total_time += duration
                transaction_count += 1

# Calculate and output the average transaction time
if transaction_count > 0:
    average_time = total_time / transaction_count
    print(f"The average transaction time is: {average_time:.2f} milliseconds")
else:
    print("No transactions found.")
