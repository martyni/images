#!/usr/bin/env python

import semantic_version
import sys

VERSION_FILE = sys.argv[1]

print(f'Using version file {VERSION_FILE}')
with open(VERSION_FILE, encoding='utf-8') as ver_file:
   VERSION = semantic_version.Version(ver_file.read().strip()) 

print(f'Current version {VERSION}')

with open(VERSION_FILE, 'w', encoding='utf-8') as ver_file:
   VERSION = VERSION.next_patch()
   print(f'New version {VERSION}')
   ver_file.write(str(VERSION))
