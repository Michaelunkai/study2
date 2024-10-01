import os

def remove_dot_from_filenames():
    current_path = os.getcwd()  # Get the current directory
    for filename in os.listdir(current_path):
        new_filename = filename.replace(".", "")
        if new_filename != filename:
            os.rename(os.path.join(current_path, filename), os.path.join(current_path, new_filename))
            print(f'Renamed: {filename} to {new_filename}')

if __name__ == "__main__":
    remove_dot_from_filenames()
