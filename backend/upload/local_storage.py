from pathlib import Path

from upload.storage import Storage


class LocalStorage(Storage):
    def save(self, path: str, content: bytes) -> str:
        """Write byte contents to a file"""
        # create parent directory if it does not exist
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as file:
            file.write(content)
        return path
