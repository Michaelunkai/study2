# Function to calculate the percentage of successful requests (status code 200)
def calculate_percentage_successful(log_file_path):
    total_requests = 0
    successful_requests = 0

    # Open the log file and read each line
    with open(log_file_path, 'r') as file:
        log_content = file.readlines()

    # Process each line to extract the status code
    for line in log_content:
        # Split the line by spaces and get the status code (typically the 9th field)
        status_code = int(line.split()[8])
        
        total_requests += 1
        if status_code == 200:
            successful_requests += 1

    # Calculate the percentage of successful requests
    if total_requests > 0:
        success_percentage = (successful_requests / total_requests) * 100
    else:
        success_percentage = 0

    return success_percentage

# Example usage with the correct file path
log_file_path = '/mnt/c/study/exams/logfile/mine/c/apache_exam.log'
success_percentage = calculate_percentage_successful(log_file_path)

# Print the percentage of successful requests
print(f"The percentage of successful requests (status code 200) is: {success_percentage:.2f}%")
