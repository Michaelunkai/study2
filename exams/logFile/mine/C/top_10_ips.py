from collections import Counter

# Function to find the top 10 IP addresses by the number of requests
def find_top_10_ips(log_file_path):
    ip_counter = Counter()

    # Open the log file and read each line
    with open(log_file_path, 'r') as file:
        log_content = file.readlines()

    # Process each line to extract the IP address
    for line in log_content:
        ip_address = line.split()[0]  # Assuming the IP is the first part of the line
        ip_counter[ip_address] += 1

    # Get the top 10 IP addresses
    top_10_ips = ip_counter.most_common(10)

    return top_10_ips

# Example usage with the correct file path
log_file_path = '/mnt/c/study/exams/logfile/mine/c/apache_exam.log'
top_10_ips = find_top_10_ips(log_file_path)

# Print the top 10 IP addresses
print("Top 10 IP addresses by number of requests:")
for ip, count in top_10_ips:
    print(f"{ip}: {count} requests")
