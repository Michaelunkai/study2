import requests
from urllib.parse import urljoin, urlparse

def generate_wget_command(url, filename):
    """
    Generate a wget command for a specific file from a URL
    """
    try:
        # Clean up the URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Clean up the filename (remove leading/trailing spaces)
        filename = filename.strip()
        
        # Create the full URL by joining the base URL and filename
        full_url = urljoin(url, filename)
        
        # Generate the wget command
        wget_command = f'wget --no-check-certificate --content-disposition "{full_url}" -O "{filename}"'
        
        return wget_command
        
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("=== File Download Command Generator ===")
    print("This script will generate a wget command for your specific file.\n")
    
    while True:
        # Get base URL
        url = input("Enter the base URL (or 'quit' to exit): ").strip()
        
        if url.lower() == 'quit':
            break
            
        if not url:
            print("Please enter a valid URL.\n")
            continue
        
        # Get filename
        filename = input("Enter the exact filename to download: ").strip()
        
        if not filename:
            print("Please enter a valid filename.\n")
            continue
        
        print("\nGenerating wget command...")
        command = generate_wget_command(url, filename)
        
        print("\nWget command for downloading the file:")
        print("-" * 50)
        print(command)
        print("-" * 50)
        print("\n")
        
        continue_choice = input("Generate another command? (y/n): ").strip().lower()
        if continue_choice != 'y':
            break
        print("\n")

if __name__ == "__main__":
    main()
