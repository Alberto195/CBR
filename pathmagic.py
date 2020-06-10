import os
import sys


class Context:
    def __enter__(self):
        module_path = os.path.abspath(os.getcwd() + '\\..\\..')
        if module_path not in sys.path:
            sys.path.append(module_path)

    def __exit__(self, *args):
        pass
