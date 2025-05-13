#!/usr/bin/env python3
import sys
import subprocess
import requests
import getpass

def fetch_tags():
    """
    Fetch every tag available from the Docker Hub repository along with its size.
    This function paginates through the API to ensure all tags are retrieved.
    """
    base_url = "https://hub.docker.com/v2/repositories/michadockermisha/backup/tags?page_size=100"
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
        f'michadockermisha/backup:"{tag}" '
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
    Allow the user to search for tags by name to launch.
    """
    query = input("Enter search term: ").strip().lower()
    if not query:
        print("Empty search query. Returning to menu.")
        return
    filtered_tags = [tag for tag in all_tags if query in tag['name'].lower()]
    if not filtered_tags:
        print("No tags found matching your query.")
        return
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

def get_dockerhub_token(username, password):
    """
    Log in to Docker Hub and return a JWT token.
    """
    login_url = "https://hub.docker.com/v2/users/login/"
    try:
        response = requests.post(login_url, json={"username": username, "password": password})
        if response.status_code != 200:
            print("Failed to login to Docker Hub. Check your credentials.")
            return None
        token = response.json().get("token")
        return token
    except Exception as e:
        print("Error during Docker Hub login:", e)
        return None

def delete_tag(all_tags):
    """
    Allow the user to choose a tag to delete from Docker Hub.
    The user can either view all tags or search for a tag.
    Before deletion, the user is prompted for Docker Hub credentials.
    """
    print("\nDelete Tag")
    print("1. Show all tags")
    print("2. Search tag by name")
    choice = input("Enter your choice (or press Enter to return to main menu): ").strip().lower()
    if not choice:
        return

    if choice == '1':
        sorted_tags = sorted(all_tags, key=lambda x: x['name'].lower())
        print_tags(sorted_tags)
        choice2 = input("\nEnter the number of the tag to delete (or press Enter to return): ").strip()
        if not choice2:
            return
        try:
            index = int(choice2) - 1
            if index < 0 or index >= len(sorted_tags):
                print("Invalid number.")
                return
            selected_tag = sorted_tags[index]
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
    elif choice == '2':
        query = input("Enter search term for deletion: ").strip().lower()
        if not query:
            print("Empty search query. Returning.")
            return
        filtered_tags = [tag for tag in all_tags if query in tag['name'].lower()]
        if not filtered_tags:
            print("No tags found matching your query.")
            return
        filtered_tags = sorted(filtered_tags, key=lambda x: x['name'].lower())
        print_tags(filtered_tags)
        choice2 = input("\nEnter the number of the tag to delete (or press Enter to return): ").strip()
        if not choice2:
            return
        try:
            index = int(choice2) - 1
            if index < 0 or index >= len(filtered_tags):
                print("Invalid number.")
                return
            selected_tag = filtered_tags[index]
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
    else:
        print("Invalid choice.")
        return

    print(f"\nSelected tag for deletion: {selected_tag['name']} ({format_size(selected_tag['full_size'])})")
    username = input("Enter your Docker Hub username (default: michadockermisha): ").strip()
    if not username:
        username = "michadockermisha"
    password = getpass.getpass("Enter your Docker Hub password: ")

    token = get_dockerhub_token(username, password)
    if token is None:
        print("Cannot proceed without a valid token.")
        return

    confirm = input("Are you sure you want to delete this tag? This action cannot be undone. (y/n): ").strip().lower()
    if confirm != 'y':
        print("Deletion cancelled.")
        return

    delete_url = f"https://hub.docker.com/v2/repositories/michadockermisha/backup/tags/{selected_tag['name']}/"
    headers = {"Authorization": f"JWT {token}"}
    try:
        response = requests.delete(delete_url, headers=headers)
        if response.status_code in [200, 204]:
            print(f"Tag '{selected_tag['name']}' deleted successfully.")
        else:
            print(f"Failed to delete tag '{selected_tag['name']}'. Status code: {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print("Error during deletion:", e)

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
        print("3. Delete tag")
        print("q. Quit")
        choice = input("Enter your choice: ").strip().lower()
        if choice == '1':
            show_all_tags(all_tags)
        elif choice == '2':
            search_tag(all_tags)
        elif choice == '3':
            delete_tag(all_tags)
        elif choice == 'q':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
