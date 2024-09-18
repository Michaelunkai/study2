import time
import os
from hashlib import sha256

class Duplython:
    def __init__(self, clean_path='.'):
        self.home_dir = os.getcwd()
        self.File_hashes = []
        self.Cleaned_dirs = []
        self.Total_bytes_saved = 0
        self.block_size = 65536
        self.count_cleaned = 0
        self.clean_path = clean_path

    def welcome(self) -> None:
        print('******************************************************************')
        print('****************        DUPLYTHON      ****************************')
        print('********************************************************************\n\n')
        print('----------------        WELCOME        ----------------------------')
        time.sleep(3)
        print('\nCleaning .................')

    def generate_hash(self, Filename: str) -> str:
        Filehash = sha256()
        try:
            with open(Filename, 'rb') as File:
                fileblock = File.read(self.block_size)
                while len(fileblock) > 0:
                    Filehash.update(fileblock)
                    fileblock = File.read(self.block_size)
                Filehash = Filehash.hexdigest()
            return Filehash
        except:
            return False

    def clean(self) -> None:
        os.chdir(self.clean_path)
        all_dirs = [path[0] for path in os.walk('.')]
        for path in all_dirs:
            if not os.path.exists(path):
                continue  # Skip non-existent paths
            os.chdir(path)
            All_Files = [file for file in os.listdir() if os.path.isfile(file)]
            for file in All_Files:
                filehash = self.generate_hash(file)
                if not filehash in self.File_hashes:
                    if filehash:
                        self.File_hashes.append(filehash)
                        # print(file)
                else:
                    byte_saved = os.path.getsize(file)
                    self.count_cleaned += 1
                    self.Total_bytes_saved += byte_saved
                    os.remove(file)
                    filename = file.split('/')[-1]
                    print(filename, '.. cleaned ')
            os.chdir(self.home_dir)

    def cleaning_summary(self) -> None:
        mb_saved = self.Total_bytes_saved / 1048576
        mb_saved = round(mb_saved, 2)
        print('\n\n--------------FINISHED CLEANING ------------')
        print('File cleaned  : ', self.count_cleaned)
        print('Total Space saved : ', mb_saved, 'MB')
        print('-----------------------------------------------')

    def main(self) -> None:
        self.welcome()
        self.clean()
        self.cleaning_summary()

if __name__ == '__main__':
    clean_path = input("Enter the path to clean (default is current directory): ").strip() or '.'
    App = Duplython(clean_path)
    App.main()