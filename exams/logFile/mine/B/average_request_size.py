import re
import sys

def parse_log_line(line):
    """
    Parses a single line of the nginx access log and extracts the size of the response.

    Parameters:
        line (str): A single line from the log file.

    Returns:
        int: Size of the response in bytes. Returns None if size is not available.
    """
    # Regex pattern to match the size field at the end of the line
    # Example log line:
    # 127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 612 "-" "Mozilla/5.0 ..."
    pattern = r'"\s*\d{3}\s+(\d+|-)'
    match = re.search(pattern, line)
    if match:
        size_str = match.group(1)
        if size_str != '-':
            try:
                return int(size_str)
            except ValueError:
                return None
    return None

def calculate_average_size(log_file_path):
    """
    Calculates the average size of HTTP responses from the log file.

    Parameters:
        log_file_path (str): Path to the nginx access log file.

    Returns:
        float: Average size of responses in bytes.
    """
    total_size = 0
    count = 0
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line_number, line in enumerate(file, 1):
            size = parse_log_line(line)
            if size is not None:
                total_size += size
                count += 1
            else:
                # Optionally, you can log or print lines with missing/malformed size
                # print(f"Line {line_number}: Size field is missing or malformed.")
                pass
    if count == 0:
        return 0.0
    return total_size / count

def main():
    """
    Main function to execute the average size calculation.
    """
    log_file = 'exam.log'  # Ensure the log file is in the same directory as this script

    try:
        average_size = calculate_average_size(log_file)
        print(f"The average request size is: {average_size:.2f} bytes")
    except FileNotFoundError:
        print(f"Error: The log file '{log_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
