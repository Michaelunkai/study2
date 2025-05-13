#!/usr/bin/env python3
import sys
import subprocess
import requests

DOCKER_REPO = "michadockermisha/backup"  # Change this if needed

def fetch_tags():
    """
    Fetch every tag available from the Docker Hub repository along with its size.
    This function paginates through the API to ensure all tags are retrieved.
    """
    base_url = f"https://hub.docker.com/v2/repositories/{DOCKER_REPO}/tags?page_size=100"
    tag_list = []
    url = base_url
    while url:
        try:
            response = requests.get(url)
            data = response.json()
            for item in data.get('results', []):
                tag_list.append({
                    'name': item['name'],
                    'full_size': item.get('full_size', 0)
                })
            url = data.get('next')  # continue to next page if available
        except Exception as e:
            print("Error fetching tags:", e)
            break
    return tag_list

def format_size(size):
    """
    Convert a size in bytes into a human-readable string.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}PB"

def print_tags(tags):
    """
    Print a numbered list of tags with their sizes.
    """
    if not tags:
        print("No tags found.")
        return
    print("\nAvailable Tags:")
    for i, tag in enumerate(tags):
        print(f"{i+1}. {tag['name']} ({format_size(tag['full_size'])})")

def launch_docker_command(tag_info):
    """
    Build and execute the docker command for the selected tag.
    """
    tag = tag_info['name']
    docker_command = (
        f'docker run '
        f'--rm '
        f'-v /mnt/c/games:/mnt/c/games '
        f'-e DISPLAY=$DISPLAY '
        f'-v /tmp/.X11-unix:/tmp/.X11-unix '
        f'--name "{tag}" '
        f'{DOCKER_REPO}:"{tag}" '
        f'sh -c "apk add rsync && rsync -aP /home /mnt/c/games && mv /mnt/c/games/home /mnt/c/games/{tag}"'
    )
    print("\nLaunching docker command:")
    print(docker_command)
    confirm = input("Do you want to proceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    process = subprocess.Popen(docker_command, shell=True)
    process.communicate()
    if process.returncode == 0:
        print("Docker command executed successfully.")
    else:
        print("Docker command failed.")

def show_all_tags(all_tags):
    """
    Display all tags sorted from heaviest to lightest.
    """
    sorted_tags = sorted(all_tags, key=lambda x: x['full_size'], reverse=True)
    print_tags(sorted_tags)
    choice = input("\nEnter the number of the tag to launch (or press Enter to return to menu): ").strip()
    if choice == '':
        return
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(sorted_tags):
            print("Invalid number.")
        else:
            launch_docker_command(sorted_tags[index])
    except ValueError:
        print("Invalid input. Please enter a number.")

def search_tag(all_tags):
    """
    Allow the user to search for tags by name.
    """
    query = input("Enter search term: ").strip().lower()
    if not query:
        print("Empty search query. Returning to menu.")
        return
    filtered_tags = [tag for tag in all_tags if query in tag['name'].lower()]
    if not filtered_tags:
        print("No tags found matching your query.")
        return
    # Sort the filtered results alphabetically
    filtered_tags = sorted(filtered_tags, key=lambda x: x['name'].lower())
    print_tags(filtered_tags)
    choice = input("\nEnter the number of the tag to launch (or press Enter to return to menu): ").strip()
    if choice == '':
        return
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(filtered_tags):
            print("Invalid number.")
        else:
            launch_docker_command(filtered_tags[index])
    except ValueError:
        print("Invalid input. Please enter a number.")

def get_auth_token(username, password):
    """
    Authenticate with Docker Hub and return a token.
    """
    login_url = "https://hub.docker.com/v2/users/login/"
    try:
        response = requests.post(login_url, json={"username": username, "password": password})
        if response.status_code != 200:
            print("Authentication failed:", response.text)
            return None
        data = response.json()
        token = data.get("token")
        if not token:
            print("Token not found in response.")
        return token
    except Exception as e:
        print("Error during authentication:", e)
        return None

def delete_tag_api(token, tag_name):
    """
    Delete the specified tag from Docker Hub using the API.
    """
    url = f"https://hub.docker.com/v2/repositories/{DOCKER_REPO}/tags/{tag_name}/"
    headers = {"Authorization": f"JWT {token}"}
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code in (200, 202, 204):
            print(f"Tag '{tag_name}' deleted successfully.")
            return True
        else:
            print(f"Failed to delete tag '{tag_name}'. Status code: {response.status_code}. Response: {response.text}")
            return False
    except Exception as e:
        print("Error during deletion:", e)
        return False

def delete_tag_option(all_tags):
    """
    Let the user choose a tag to delete from Docker Hub.
    """
    # Sort tags alphabetically for ease of browsing
    sorted_tags = sorted(all_tags, key=lambda x: x['name'].lower())
    print_tags(sorted_tags)
    choice = input("\nEnter the number of the tag to delete (or press Enter to return to menu): ").strip()
    if choice == '':
        return all_tags  # no deletion, return original list
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(sorted_tags):
            print("Invalid number.")
            return all_tags
        selected_tag = sorted_tags[index]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return all_tags

    confirm = input(f"Are you sure you want to delete tag '{selected_tag['name']}' permanently? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Deletion cancelled.")
        return all_tags

    # Ask for Docker Hub credentials
    username = input("Enter your Docker Hub username: ").strip()
    password = input("Enter your Docker Hub password: ").strip()

    token = get_auth_token(username, password)
    if not token:
        print("Unable to authenticate. Aborting deletion.")
        return all_tags

    if delete_tag_api(token, selected_tag['name']):
        # Re-fetch tags after deletion to update the list
        print("Refreshing tag list...")
        updated_tags = fetch_tags()
        return updated_tags
    else:
        print("Deletion failed. Tag list remains unchanged.")
        return all_tags

def main():
    print("Fetching tags from Docker Hub...")
    all_tags = fetch_tags()
    if not all_tags:
        print("No tags available. Exiting.")
        return

    while True:
        print("\nMenu:")
        print("1. Show all tags (heaviest to lightest)")
        print("2. Search tag by name")
        print("3. Delete tag from Docker Hub")
        print("q. Quit")
        choice = input("Enter your choice: ").strip().lower()
        if choice == '1':
            show_all_tags(all_tags)
        elif choice == '2':
            search_tag(all_tags)
        elif choice == '3':
            all_tags = delete_tag_option(all_tags)
        elif choice == 'q':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
