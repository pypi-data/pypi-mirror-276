# mypackage/__init__.py

import pkgutil
import inspect
import sys


__all__ = []

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = __import__(f"{__name__}.{module_name}", fromlist=[module_name])
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) or inspect.isclass(obj):
            setattr(sys.modules[__name__], name, obj)
            __all__.append(name)
