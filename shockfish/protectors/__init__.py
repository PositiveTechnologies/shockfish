__all__ = []

import pkgutil
import inspect

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(module_name).load_module(module_name)

    for name, value in inspect.getmembers(module):

        if name.startswith('__'):
            continue

        # Load only protectors entry point.
        if name.endswith("Protector") and inspect.isclass(value):
            globals()[name] = value
            __all__.append(name)
        