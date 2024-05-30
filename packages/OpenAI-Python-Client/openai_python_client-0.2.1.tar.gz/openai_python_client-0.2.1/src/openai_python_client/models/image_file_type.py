from enum import Enum


class ImageFileType(str, Enum):
    IMAGE_FILE = "image_file"

    def __str__(self) -> str:
        return str(self.value)
