from collections import Counter

# Function to find the top 5 referrers from the log file
def find_top_5_referrers(log_file_path):
    referrer_counter = Counter()

    # Open the log file and read each line
    with open(log_file_path, 'r') as file:
        log_content = file.readlines()

    # Process each line to extract the referrer
    for line in log_content:
        # Referrer is typically between the second set of quotes in the log entry
        referrer = line.split('"')[3]
        
        # Only count valid referrers (ignoring "-" which means no referrer)
        if referrer != "-":
            referrer_counter[referrer] += 1

    # Get the top 5 referrers
    top_5_referrers = referrer_counter.most_common(5)

    return top_5_referrers

# Example usage with the correct file path
log_file_path = '/mnt/c/study/exams/logfile/mine/c/apache_exam.log'
top_5_referrers = find_top_5_referrers(log_file_path)

# Print the top 5 referrers
print("Top 5 referrers:")
for referrer, count in top_5_referrers:
    print(f"{referrer}: {count} requests")
