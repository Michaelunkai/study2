#!/usr/bin/env python3
import os
import time
import zipfile
import rarfile
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Get the downloads folder path
downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

# Set default password for password-protected archives
DEFAULT_PASSWORD = '123'

class ArchiveHandler(FileSystemEventHandler):
    def __init__(self):
        self.processed_files = set()

    def on_created(self, event):
        # Check if the created item is a file
        if not event.is_directory:
            file_path = event.src_path
            file_extension = os.path.splitext(file_path)[1].lower()

            # Check if the file is a ZIP or RAR archive and hasn't been processed before
            if file_extension in ['.zip', '.rar'] and file_path not in self.processed_files:
                logger.info(f"Detected new archive: {file_path}")
                # Wait a bit to ensure file is completely written
                time.sleep(2)
                self.processed_files.add(file_path)
                self.extract_archive(file_path)

    def extract_archive(self, archive_path):
        try:
            # Wait a moment to ensure the file is fully downloaded
            time.sleep(1)

            # Get the base filename without extension
            filename = os.path.basename(archive_path)
            base_name = os.path.splitext(filename)[0]

            # Create extraction folder
            extract_folder = os.path.join(downloads_folder, base_name)
            if not os.path.exists(extract_folder):
                os.makedirs(extract_folder)

            # Extract based on file type
            file_extension = os.path.splitext(archive_path)[1].lower()

            if file_extension == '.zip':
                logger.info(f"Extracting ZIP file: {filename} to {extract_folder}")
                # Make sure the file exists and is accessible
                if os.path.exists(archive_path) and os.access(archive_path, os.R_OK):
                    try:
                        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                            # First try without password
                            try:
                                zip_ref.extractall(extract_folder)
                                logger.info(f"Successfully extracted {filename}")
                            except RuntimeError as e:
                                # If password required, try with default password
                                if "password required" in str(e).lower() or "encrypted" in str(e).lower():
                                    logger.info(f"Archive is password protected, trying with default password")
                                    # Need to reopen the file for password extraction
                                    with zipfile.ZipFile(archive_path, 'r') as zip_pwd:
                                        zip_pwd.extractall(path=extract_folder, pwd=DEFAULT_PASSWORD.encode())
                                    logger.info(f"Successfully extracted password-protected archive {filename}")
                                else:
                                    raise
                    except Exception as e:
                        logger.error(f"Error extracting ZIP {filename}: {str(e)}")
                else:
                    logger.error(f"Cannot access ZIP file: {archive_path}")

            elif file_extension == '.rar':
                logger.info(f"Extracting RAR file: {filename} to {extract_folder}")
                if os.path.exists(archive_path) and os.access(archive_path, os.R_OK):
                    try:
                        rarfile.UNRAR_TOOL = "unrar"  # Ensure unrar tool is set
                        with rarfile.RarFile(archive_path, 'r') as rar_ref:
                            # Check if password is needed
                            if rar_ref.needs_password():
                                logger.info(f"RAR archive is password protected, using default password")
                                rar_ref.setpassword(DEFAULT_PASSWORD)
                            
                            rar_ref.extractall(extract_folder)
                            logger.info(f"Successfully extracted {filename}")
                    except Exception as e:
                        logger.error(f"Error extracting RAR {filename}: {str(e)}")
                else:
                    logger.error(f"Cannot access RAR file: {archive_path}")

        except zipfile.BadZipFile:
            logger.error(f"Bad ZIP file format: {archive_path}")
        except rarfile.BadRarFile:
            logger.error(f"Bad RAR file format: {archive_path}")
        except PermissionError:
            logger.error(f"Permission denied accessing: {archive_path}")
        except Exception as e:
            logger.error(f"Error extracting {archive_path}: {str(e)}")

def main():
    logger.info(f"Starting archive monitoring for: {downloads_folder}")
    
    # Create the handler first so we have access to its methods
    handler = ArchiveHandler()

    # Check for existing archives in downloads folder
    for filename in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, filename)
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1].lower() in ['.zip', '.rar']:
            logger.info(f"Found existing archive: {file_path}")
            handler.extract_archive(file_path)
            # Add to processed files set to avoid re-processing
            handler.processed_files.add(file_path)

    # Create observer
    observer = Observer()

    # Schedule the observer to watch the downloads folder
    observer.schedule(handler, downloads_folder, recursive=False)
    observer.start()

    try:
        logger.info("Monitoring for new archives. Press Ctrl+C to stop.")
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Monitoring stopped by user")
    except Exception as e:
        observer.stop()
        logger.error(f"Error occurred: {str(e)}")
    
    observer.join()

if __name__ == "__main__":
    main()
