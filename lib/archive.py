from zipfile import ZipFile


class Archive:

    def __init__(self, filename: str):
        self._filename = filename
        self._files = []

    def push(self, file: str):
        self._files.append(file)

    def flush(self) -> str:
        with ZipFile(self._filename, 'w') as zip_archive:
            for file in self._files:
                zip_archive.write(filename=file)

        return self._filename
