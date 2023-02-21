import sys
import os
import importlib
import inspect


overloads_module = sys.modules[__name__]

for module_name in os.listdir(os.path.dirname(__file__)):
    if module_name == '__init__.py' or module_name[-3:] != '.py':
        continue
    module = importlib.import_module(f'.{module_name[:-3]}', __name__)
    funcs = inspect.getmembers(module, inspect.isfunction)
    for name, func in funcs:
        setattr(overloads_module, name, func)
