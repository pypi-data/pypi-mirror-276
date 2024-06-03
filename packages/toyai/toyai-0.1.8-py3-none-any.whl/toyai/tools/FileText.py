import os
import re
from .os import mkdir


class FileText:
    texts: list[str] = []
    data: list[any] = []
    filepath: str
    isSaved: bool = True
    label: any
    transformer: any = None

    def __init__(self, filepath, label=None, texts=[], transformer=None) -> None:
        self.filepath = filepath
        self.texts = texts
        self.label = label
        self.transformer = transformer

    def load(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                self.texts = [line.strip() for line in file.readlines()]
        except Exception as e:
            print("An error occurred:", e)

        return self

    def get_texts(self):
        return self.texts

    def set_texts(self, texts):
        self.texts = texts
        return self

    def add_text(self, text):
        self.texts.append(text)
        self.isSaved = False

    def transform(self, func):
        return func(self.texts)

    def save(self):
        with open(self.filepath, "w") as file:
            file.write("\n".join(self.texts))
            self.isSaved = True
        return self

    def save_as(self, new_filepath):
        new_filepath = mkdir(new_filepath)
        with open(new_filepath, "w") as file:
            file.write("\n".join(self.texts))
            self.isSaved = True
        return self


class FileTextLabel(FileText):
    texts: list[str]
    labels: list[int]

    def __init__(
        self,
        file_format=r"^[0-9]+_.*",
        filename_seperator="_",
    ):
        self.sep = filename_seperator
        self.texts = []
        self.labels = []
        self.classes = {}
        self.file_format = file_format

    @staticmethod
    def load_file(self, filepath, label=0):
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                line_words = line.strip().split()
                self.texts.extend(line_words)
                self.labels.extend([id] * len(line_words))
        return self

    @staticmethod
    def load_dir(self, dir, file_format=r"^[0-9]+_.*"):
        pattern = file_format  # แก้ไข pattern
        for filename in os.listdir(dir):
            if re.match(pattern, filename):
                file_parts = filename.split(self.sep)
                id = int(file_parts[0])
                label = file_parts[1].split(".")[0]  # แก้ไขสำหรับตัดส่วนขยายไฟล์ออก

                self.classes[id] = label

                filepath = os.path.join(dir, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    for line in file:
                        line_words = line.strip().split()
                        self.texts.extend(line_words)
                        self.labels.extend([id] * len(line_words))
        return self
