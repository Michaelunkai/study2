# Function to count the number of POST requests in the log
def count_post_requests(log_file_path):
    post_count = 0

    # Open the log file and read each line
    with open(log_file_path, 'r') as file:
        log_content = file.readlines()

    # Process each line and check for POST requests
    for line in log_content:
        if 'POST' in line:
            post_count += 1

    return post_count

# Example usage with the correct file path
log_file_path = '/mnt/c/study/exams/logfile/mine/c/apache_exam.log'
post_request_count = count_post_requests(log_file_path)

print(f"The number of POST requests is: {post_request_count}")
