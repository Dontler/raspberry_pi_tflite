from zipfile import ZipFile


class Archive:

    def __init__(self, filename: str):
        self._filename = filename
        self._files = []

    @property
    def file(self):
        return self._filename

    def push(self, file: str):
        self._files.append(file)

    def build(self) -> str:
        with ZipFile(self.file, 'w') as zip_archive:
            for file in self._files:
                zip_archive.write(filename=file)

        return self._filename
