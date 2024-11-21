import os

def get_disk_space(path='.'):
    if not path:
        path = '.'

    total, used, free = os.statvfs(path)[:3]
    total_space_gb = total * free / (2 ** 30)
    used_space_gb = used * free / (2 ** 30)
    free_space_gb = free * free / (2 ** 30)

    return total_space_gb, used_space_gb, free_space_gb

if __name__ == "__main__":
    path = input("Enter the path to analyze (default is current directory): ").strip()
    total, used, free = get_disk_space(path)

    print(f"Total Space: {total:.2f} GB")
    print(f"Used Space: {used:.2f} GB")
    print(f"Free Space: {free:.2f} GB")
