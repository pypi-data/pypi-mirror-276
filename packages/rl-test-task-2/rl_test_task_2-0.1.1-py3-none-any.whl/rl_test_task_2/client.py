import shutil


class Client:
    def client_code(self, source_file_path: str, destination_dir_path: str) -> None:
        try:
            shutil.move(source_file_path, destination_dir_path)

        except FileNotFoundError:
            print(f'Source file not found: {source_file_path}')

        print(destination_dir_path)
