import importlib
import sys

if __name__ == "__main__":
    module = sys.argv[1]
    importlib.import_module(module)

