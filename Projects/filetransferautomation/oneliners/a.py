import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        file_name = os.path.basename(event.src_path)
        if "one liner" in file_name.lower() or "one-liner" in file_name.lower():
            destination = "/mnt/c/study/automation/oneliners"
            shutil.copy(event.src_path, destination)

def main():
    path = "."  # Replace this with the directory you want to monitor
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
