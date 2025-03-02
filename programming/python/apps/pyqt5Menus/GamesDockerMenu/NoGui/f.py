#!/usr/bin/env python3
import sys
import subprocess
import requests

def fetch_tags():
    """
    Fetch every tag available from the Docker Hub repository along with its size.
    """
    url = "https://hub.docker.com/v2/repositories/michadockermisha/backup/tags?page_size=100"
    try:
        response = requests.get(url)
        data = response.json()
        tag_list = []
        for item in data.get('results', []):
            tag_list.append({
                'name': item['name'],
                'full_size': item.get('full_size', 0)
            })
        return tag_list
    except Exception as e:
        print("Error fetching tags:", e)
        return []

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
        print("q. Quit")
        choice = input("Enter your choice: ").strip().lower()
        if choice == '1':
            show_all_tags(all_tags)
        elif choice == '2':
            search_tag(all_tags)
        elif choice == 'q':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
