import pytest
from my_app.app import main

def test_main():
   assert main() is 'hi', 'hello not returned'
