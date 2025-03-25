def format_size(size_in_bytes):
    """Convert bytes to a human-readable format."""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1048576:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1073741824:
        return f"{size_in_bytes / 1048576:.2f} MB"
    else:
        return f"{size_in_bytes / 1073741824:.2f} GB"

def validate_docker_image_name(image_name):
    """Check if the provided Docker image name is valid."""
    if not image_name or len(image_name) > 128:
        return False
    # Add more validation rules as needed
    return True

def generate_unique_id(prefix=''):
    """Generate a unique identifier with an optional prefix."""
    import uuid
    return f"{prefix}{uuid.uuid4().hex}"

def log_message(message):
    """Log a message to the console."""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")