from collections import Counter

# Function to find the most requested resource (URL) in the log file
def find_most_requested_resource(log_file_path):
    resource_counter = Counter()

    # Open the log file and read each line
    with open(log_file_path, 'r') as file:
        log_content = file.readlines()

    # Process each line to extract the requested resource (URL)
    for line in log_content:
        # Split the line by spaces, extract the request method and URL (e.g., "GET /path/to/resource HTTP/1.1")
        request_info = line.split('"')[1]
        request_method, resource, _ = request_info.split()
        
        # Only count valid GET or POST requests (or other methods, if needed)
        if request_method in ['GET', 'POST']:
            resource_counter[resource] += 1

    # Find the most requested resource
    most_requested_resource, count = resource_counter.most_common(1)[0]

    return most_requested_resource, count

# Example usage with the correct file path
log_file_path = '/mnt/c/study/exams/logfile/mine/c/apache_exam.log'
most_requested_resource, request_count = find_most_requested_resource(log_file_path)

# Print the most requested resource
print(f"The most requested resource is: {most_requested_resource} with {request_count} requests")
