import json
import inspect
import os
import importlib.util

from llmify.utils.openai.tools import functionify
from importlib.util import spec_from_file_location, module_from_spec


class MetaMapper:
    """
    Class for mapping metadata of functions within a module.

    This class provides functionality to load a Python module and map metadata of functions
    within that module. Metadata includes information about function names, descriptions, parameters,
    and required parameters. The metadata is generated using the `functionify` decorator provided
    by the 'llmify.utils.openai.tools' module.

    Attributes:
        module_name (str): The name of the Python module to load and map metadata from.

    Methods:
        map(): Loads the specified module and maps metadata for functions within it.
        load_module(): Loads the specified Python module.

    Example Usage:
        mapper = MetaMapper('example_module')
        metadata = mapper.map()
        print(json.dumps(metadata, indent=4))
    """

    def __init__(self, module_name):
        """
        Initialize MetaMapper with the name of the Python module to map metadata from.

        Parameters:
            module_name (str): The name of the Python module (without file extension).
        """
        self.module_name = module_name

    def map(self):
        """
        Load the specified module and map metadata for functions within it.

        Returns:
            dict: A dictionary containing metadata for functions within the module.
        """
        module = self.load_module()
        if module:
            meta_dict = {}
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj):
                    if hasattr(obj, '__wrapped__'):
                        func = obj
                        decorated_func = functionify(func)
                        meta = decorated_func.meta
                        meta_dict[name] = meta
            return meta_dict

    def load_module(self):
        """
        Load the specified Python module.

        Returns:
            module: The loaded module object, or None if the module is not found.
        """
        spec = importlib.util.find_spec(self.module_name)
        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        else:
            print(f"Module '{self.module_name}' not found.")
            return None