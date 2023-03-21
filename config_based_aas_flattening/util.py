from importlib import import_module
import uuid
import logging


def generate_object_id(parent_obj):
    class_name = get_simple_class_name_from_object(parent_obj)
    obj_id = f'{class_name}_{str(uuid.uuid4())}'
    logging.info(f'Generated Random ID:{obj_id} for object {parent_obj}')
    return obj_id


def get_simple_class_name_from_object(o):
    return get_simple_class_name_from_type(o.__class__)


def get_simple_class_name_from_type(t):
    return t.__name__


def load_module(package: str, module: str):
    package = import_module(package)
    module_obj = getattr(package, module)
    return module_obj
