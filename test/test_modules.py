'''
   Testing module imports
'''
# pylint: disable=W0122
from os import listdir, chdir, walk


def __find_dir(start_dir, directory):
    '''
    Find src directory for source code
    '''
    files = walk(start_dir)
    for level in files:
        if directory in level[1]:
            target_dir = f'{level[0]}/{directory}'
            chdir(target_dir)
            return target_dir
        return __find_dir('./{start_dir}', directory)



SRC = __find_dir('.', 'src')
TESTS_DIR = 'tests'
MODULES = listdir()
SUBMODULES = []


def test_module_imports():
    '''
    Import modules
    '''
    for mod in MODULES:
        if 'egg-info' in mod:
            break
        exec(f'import {mod}')
        assert exec('{mod}') is not False, f'Could not import {mod}'
        for submod in listdir(f'{mod}'):
            if '__init__' in submod:
                break
            submod = submod.split('.py')[0]
            exec(f'import {mod}.{submod}')
            SUBMODULES.append(f'{mod}_{submod}')
            assert exec(f'{mod}.{submod}') is not False, f'Could not initialize {
                mod}.{submod}'


def test_coverage():
    '''
    Check each coverage
    '''
    __find_dir('.', TESTS_DIR)
    tests = set(listdir())
    for submod in SUBMODULES:
        print(submod)
        assert f'{submod}_test.py' in tests


if __name__ == '__main__':
    test_module_imports()
    test_coverage()
