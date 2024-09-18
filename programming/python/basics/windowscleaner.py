import os
import shutil

def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size / (1024*1024*1024)  # Convert bytes to gigabytes

def delete_files_in_folder(folder):
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Failed to delete {filepath}: {e}")

def delete_folders(folder):
    for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
        for dirname in dirnames:
            try:
                shutil.rmtree(os.path.join(dirpath, dirname))
            except Exception as e:
                print(f"Failed to delete {dirname}: {e}")

def main():
    paths_to_delete = [
        os.environ['TEMP'],
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCache'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Windows', 'Temporary Internet Files'),
        os.path.join('C:', 'Windows', 'SoftwareDistribution', 'Download'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Windows', 'Logs'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
        os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles', '[profile name]', 'cache2'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCache', 'IE'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCache', 'Low', 'IE'),
        os.path.join('C:', 'Windows', 'Minidump'),
        os.path.join(os.environ['SystemRoot'], 'PCHEALTH', 'ERRORREP', 'QHEADLES'),
        os.path.join('Control Panel', 'System and Security', 'Administrative Tools'),
        os.path.join('C:', 'Windows', 'WinSxS', 'Backup'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Windows', 'WER', 'ReportArchive'),
        os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
        os.path.join(os.environ['SystemRoot'], 'Logs', 'CBS'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Packages', 'Microsoft.WindowsStore_8wekyb3d8bbwe', 'LocalCache'),
        os.path.join(os.environ['SystemRoot'], 'System32', 'WDI', 'LogFiles'),
        os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows Defender', 'Scans', 'Temp'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp', 'Temporary ASP.NET Files'),
        os.path.join(os.environ['SystemRoot'], 'System32', 'winevt', 'Logs'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Outlook'),
        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Microsoft', 'Windows', 'WER', 'ReportQueue'),
        os.path.join(os.environ['WINDIR'], 'Installer'),
        os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Remote Assistance'),
        os.path.join('Control Panel', 'System and Security', 'System'),
        os.path.join('C:', 'Users', 'micha', 'AppData', 'Local', 'Temp')
    ]

    total_deleted_size = 0
    for path in paths_to_delete:
        if os.path.exists(path):
            print(f"Deleting files in {path}...")
            delete_files_in_folder(path)
            print(f"Deleting folders in {path}...")
            delete_folders(path)
            total_deleted_size += get_folder_size(path)

    print(f"\nTotal space freed up: {total_deleted_size:.2f} GB")

if __name__ == "__main__":
    main()
