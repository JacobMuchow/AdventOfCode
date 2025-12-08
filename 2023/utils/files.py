class FileUtils:
    @staticmethod
    def read_lines(file_path: str) -> list[str]:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]