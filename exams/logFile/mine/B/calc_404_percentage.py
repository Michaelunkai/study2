def calculate_404_percentage(log_file_path):
    total_requests = 0
    total_404s = 0
    
    # Open and read the log file
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        
        # Loop through each line
        for line in lines:
            total_requests += 1
            if ' 404 ' in line:  # Check if the line contains a 404 status code
                total_404s += 1
    
    if total_requests == 0:
        return 0  # Avoid division by zero
    
    # Calculate the percentage of 404 responses
    return (total_404s / total_requests) * 100

# Example usage
log_file_path = '/mnt/c/study/exams/logFile/mine/B/exam.log'  # Correct log file path
percentage_404 = calculate_404_percentage(log_file_path)

# Output the percentage of 404 requests
print(f"Percentage of 404 requests: {percentage_404:.2f}%")
