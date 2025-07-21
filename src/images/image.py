from PIL import Image
from time import sleep
from pathlib import Path


class Picture(object):
    def __init__(self, filename, path, logger=print):
        """Picture caries out a series of operations to understand an image passed to it as a filepath"""
        self.filename = filename
        self.filetype = self.filename.split(".")[-1]
        self.name = self.filename.split(".")[0]
        self.path = path
        self.filenumber = self.filename[-1]
        self.logger = logger
        try:
            self.filenumber = int(self.filenumber)
            self.filenumber += 1
        except ValueError:
            self.filenumber = 1
        self.open_image()

    def open_image(self):
        self.im = Image.open(f"{self.path}/{self.filename}")

    def size(self):
        """Return the width and height of a picture"""
        self.logger(f"width: {self.im.width}, height: {self.im.height}")
        return self.im.width, self.im.height

    def new_filename(self):
        self.filename = f'{self.name}{self.filenumber}.{self.filetype}'
        self.filepath = f'{self.path}/{self.filename}'
        self.logger(f"new_filename: {self.filename}")

    def new_format(self, new_format):
        self.open_image()
        self.filetype = new_format
        self.logger(f'fileType is {self.filetype}')

    def resize(
            self,
            width=None,
            height=None,
            squish=None,
            new_format=None,
            max_width=1080,
            max_height=1920):
        if width is None:
            width = max_width
        if height is None:
            height = max_height
        if new_format is None:
            self.open_image()
        else:
            self.new_format(new_format)
        self.logger(f'fileType is {self.filetype}')

        self.logger(f"width: {width}, height: {height}")
        if squish is None:
            self.im.thumbnail((int(width), int(height)), 0)
        else:
            self.im = self.im.resize((int(width), int(width)))
        self.new_filename()
        self.logger(f"saving: {self.filepath}")
        self.im.save(f"{self.filepath}")
        self.logger(f"saved: {self.filepath}")
        self.im.close()
        return self.filename
