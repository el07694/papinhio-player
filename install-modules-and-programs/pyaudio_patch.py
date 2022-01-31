import os
import sys

patch_code_1 = '''
import time, os, sys, contextlib

@contextlib.contextmanager
def ignoreStderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)
'''

patch_code_2 = '''
        pa.initialize()
        self._streams = set()
'''

patch_code_3 = '''
        with ignoreStderr():
            pa.initialize()
            self._streams = set()
'''

import pyaudio
pyaudio_path = pyaudio.__file__

with open(pyaudio_path, 'r') as file:
    data = file.read()

data = patch_code_1+data
data = data.replace(patch_code_2,patch_code_3)
    

# and write everything back
with open(pyaudio_path, 'w') as file:
    file.write(data)