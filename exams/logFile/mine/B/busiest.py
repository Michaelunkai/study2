from collections import Counter
from datetime import datetime

# Function to find the busiest hour in the log
def find_busiest_hour(log_file_path):
    hour_counter = Counter()

    # Open the log file and read each line
    with open(log_file_path, 'r') as file:
        log_content = file.readlines()

    # Process each line to extract the timestamp
    for line in log_content:
        # Extract the part of the log line that contains the date and time
        timestamp_part = line.split('[')[1].split(']')[0]
        
        # Convert the timestamp to a datetime object
        log_time = datetime.strptime(timestamp_part, '%d/%b/%Y:%H:%M:%S %z')
        
        # We are only interested in the hour, so round to the hour
        hour_str = log_time.strftime('%Y-%m-%d %H:00:00')
        
        # Increment the counter for that hour
        hour_counter[hour_str] += 1

    # Find the busiest hour
    busiest_hour, request_count = hour_counter.most_common(1)[0]
    
    return busiest_hour, request_count

# Example usage
log_file_path = '/mnt/c/study/exams/logFile/mine/b/exam.log'  # Update this with your actual log file path
busiest_hour, request_count = find_busiest_hour(log_file_path)

print(f"The busiest hour is {busiest_hour} with {request_count} requests.")
