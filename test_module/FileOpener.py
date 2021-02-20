import os

class FileRead:
    def __init__(self, file_path):
        super().__init__()
        self.read_file = file_path

    def open_and_read(self):
        dir = os.path.dirname(self.read_file)
        print(f"accessing dir: {dir}")
        another_file = os.path.join(dir, 'some_file.txt')

        with open(self.read_file, 'r') as rf, open(another_file) as another:
            print(f'file \"{self.read_file}\" content:')
            for line in rf.read().splitlines():
                print(line)

    def read_and_write_new(self):
        dir = os.path.dirname(self.read_file)
        print(f"accessing dir: {dir}")
        another_file = os.path.join(dir, 'some_file.txt')

        with open(self.read_file, 'r') as rf, open(another_file) as another:
            print(f'file \"{self.read_file}\" content:')
            for line in rf.read().splitlines():
                print(line)
                print(another.write(line + '\n'))

            print(f'file \"{another_file}\" content:')
            for line in another.read().splitlines():
                print(line)

