import re

def extract_user_agents(log_file_path):
    # Regular expression for identifying user agents
    user_agent_pattern = re.compile(
        r'(Mozilla/[^\s]+|Opera/[^\s]+|Chrome/[^\s]+|Safari/[^\s]+|Edge/[^\s]+|Firefox/[^\s]+|MSIE [^\s]+|Trident/[^\s]+)'
    )
    
    user_agents = set()
    
    # Open and read the log file
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        
        # Loop through each line
        for line in lines:
            # Find all matches for user agents in each line
            matches = user_agent_pattern.findall(line)
            if matches:
                user_agents.update(matches)

    return user_agents

# Example usage
log_file_path = '/mnt/c/study/exams/logFile/mine/B/exam.log'  # Path to the log file
unique_user_agents = extract_user_agents(log_file_path)

# Output the list of unique user agents
for agent in unique_user_agents:
    print(agent)
