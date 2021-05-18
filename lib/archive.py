from zipfile import ZipFile


class Archive:

    def __init__(self, filename: str):
        self._filename = filename

    @property
    def file(self):
        return self._filename

    def push(self, file: str):
        with ZipFile(self.file, 'w') as zip_archive:
            zip_archive.write(file)
