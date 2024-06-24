#!/usr/bin/env python
'''
Increment script
'''
import sys
import semantic_version

VERSION_FILE = sys.argv[1]
INCREMENT_TYPE = sys.argv[2].lower()
INCREMENT_FUNC = {
    "major": "next_major",
    "minor": "next_minor",
    "patch": "next_patch"

}

print(f'Using version file {VERSION_FILE} increment type is {INCREMENT_TYPE}')
with open(VERSION_FILE, encoding='utf-8') as ver_file:
    VERSION = semantic_version.Version(ver_file.read().strip())

print(f'Current version {VERSION}')

with open(VERSION_FILE, 'w', encoding='utf-8') as ver_file:
    next_version = getattr(VERSION, INCREMENT_FUNC[INCREMENT_TYPE])
    VERSION = next_version()
    print(f'New version {VERSION}')
    ver_file.write(str(VERSION))
