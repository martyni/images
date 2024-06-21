import pytest
from my_app.app import main


def test_main():
    return_phrase = 'hi'
    assert main() is return_phrase, f'{return_phrase} not returned'
