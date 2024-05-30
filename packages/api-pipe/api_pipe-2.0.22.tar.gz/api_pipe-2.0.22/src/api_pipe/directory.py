'''
    Directory
'''
import shutil
from pathlib import Path

def remove_dir(dir: Path, recreate: bool = False):
    '''
        Remove directory. If recreate is True, create the directory
    '''
    if dir.exists():
        shutil.rmtree(dir)

    if recreate:
        dir.mkdir(
            parents=True,
            exist_ok=True
        )

def remove_file(file: Path, recreate: bool = False):
    '''
        Remove file. If recreate is True, create the file
    '''
    if file.exists():
        file.unlink()

    if recreate:
        file.touch()
