import util
from generic_data import flattened_type
import key_constants as kc
import logging
from importlib import import_module
from header_list import HeaderList


def get_parents(o):
    parents = type(o).__bases__
    par_simp_name = {}
    for i in parents:
        par_simp_name[i.__name__] = i
    return par_simp_name


def get_simple_class_name_from_object(o):
    return get_simple_class_name_from_type(o.__class__)


def get_simple_class_name_from_type(t):
    return t.__name__


def flatten_child(o: flattened_type, config, headers: HeaderList, parent_flattened: flattened_type, par_obj):
    parent_class_name = get_simple_class_name_from_object(par_obj)
    # getting id from parent type
    try:
        id_field = config[parent_class_name][kc.KEY_ID_FIELD]
        parent_id = getattr(par_obj, id_field)
    except KeyError:
        logging.warning(f'"{parent_class_name}" section in config should have a "{kc.KEY_ID_FIELD}" entry!')
        # handling special case for types like OperationVariable where they do not have an id field.
        if kc.KEY_ID_SHORT not in parent_flattened.attrib_map:
            parent_flattened.append_attrib_val_pair({kc.KEY_ID_SHORT: util.generate_object_id(par_obj)})
            headers.append(kc.KEY_ID_SHORT)
        parent_id = parent_flattened.attrib_map.get(kc.KEY_ID_SHORT)
    flattened_child = get_flatten_from_object(o, config, headers, parent_id=parent_id)
    # returned flattened child object could be a list or a single object
    if not isinstance(flattened_child, list):
        flattened_child = [flattened_child]
    for c in flattened_child:
        if c:
            parent_flattened.add_child(c)


def flatten_as_parents(o, config, headers: HeaderList, flatten_object: flattened_type, parent_id):
    parents = get_parents(o)
    for p in parents:
        if p in config:
            # TODO: We need to address this issue; the only other way to typecast is through a Constructor,
            #  but this would be quite difficult. If we do not use this method, we won't be able to take advantage of
            #  the inheritance structure of the data.
            # put it in try catch -- put a note in the specification
            try:
                orig_type = type(o)
                par_type = parents[p]
                logging.info(f"Changing type of {o} to {par_type}")
                o.__class__ = par_type
                flatten_object = get_flatten_from_object(o, config, headers, flatten_object, parent_id)
                o.__class__ = orig_type
            finally:
                logging.info(f"Setting type of {o} back to its original type {orig_type}")
                o.__class__ = orig_type


def get_flatten_from_object(o, config, headers: HeaderList, flatten_object: flattened_type = None, parent_id=None):
    if not flatten_object:
        flatten_object = flattened_type()
    # first we flatten as parents in case only parent class is entered in the config and not the child class
    flatten_as_parents(o, config, headers, flatten_object, parent_id)

    class_name = get_simple_class_name_from_object(o)
    if class_name in config:
        class_meta = config[class_name]
        if not flatten_object:
            flatten_object = flattened_type()
        # check if entry for object's type exist in config
        if kc.KEY_OBJECT_TYPE in class_meta:
            class_name = class_meta[kc.KEY_OBJECT_TYPE]
        flatten_object.append_attrib_val_pair({kc.KEY_OBJECT_TYPE: class_name})
        # adding all the added meta info in header_field for csv header
        headers.append(kc.KEY_OBJECT_TYPE)
        # if input object is a child
        if parent_id:
            flatten_object.append_attrib_val_pair({kc.KEY_HEADER_PARENT_ID: parent_id})
            headers.append(kc.KEY_HEADER_PARENT_ID)
        if kc.KEY_ATTRIBUTE in class_meta:
            meta_attrib = class_meta[kc.KEY_ATTRIBUTE]
            for key in meta_attrib:
                try:
                    attrib_name = key[kc.KEY_NAME]
                except KeyError as error:
                    logging.error(f'"{class_name}.{kc.KEY_ATTRIBUTE}" section in config should '
                                  f'have a "{kc.KEY_NAME}" entry!')
                    raise error
                # checking if not include this attribute
                if kc.KEY_INCLUDE in key and not key[kc.KEY_INCLUDE]:
                    continue
                cast_into = key[kc.KEY_CAST] if kc.KEY_CAST in key else "str"
                flatten_object.append_attrib_val_pair({attrib_name: eval(cast_into)(getattr(o, attrib_name))})
                headers.append(attrib_name)
        # if input object has children
        if kc.KEY_CHILD in class_meta:
            child_meta = class_meta[kc.KEY_CHILD]
            # to get child as an attribute to input object
            for prop in child_meta:
                try:
                    attrib_name = prop[kc.KEY_ATTRIBUTE_NAME]
                except KeyError as error:
                    logging.error(
                        f'"{class_name}.{kc.KEY_CHILD}" section in config should have a "{kc.KEY_ATTRIBUTE_NAME}'
                        f'" entry!')
                    raise error
                attrib = getattr(o, attrib_name)
                if attrib:
                    try:
                        if not prop[kc.KEY_IS_LIST]:
                            attrib = [attrib]
                    except KeyError as error:
                        logging.error(
                            f'"{class_name}.{kc.KEY_CHILD}" section in config should have a "{kc.KEY_IS_LIST}"'
                            f' entry!')
                        raise error
                    check_type = False
                    if kc.KEY_MODULE and kc.KEY_CHILD_TYPE in prop:
                        check_type = True
                        module = import_module(prop[kc.KEY_MODULE])
                        child_type = getattr(module, prop[kc.KEY_CHILD_TYPE])
                    for child in attrib:
                        if check_type and not isinstance(child, child_type):
                            continue
                        flatten_child(child, config, headers, flatten_object, o)
        if kc.KEY_CUSTOM_FLATTENING in class_meta:
            custom_flat_meta = class_meta[kc.KEY_CUSTOM_FLATTENING]
            try:
                custom_flat_module = import_module(custom_flat_meta[kc.KEY_MODULE])
            except KeyError as error:
                logging.error(f'"{class_name}.{kc.KEY_CUSTOM_FLATTENING}" section in config should '
                              f'have a "{kc.KEY_MODULE}" entry!')
                raise error
            try:
                custom_flat_func = custom_flat_meta[kc.KEY_FUNCTION]
            except KeyError as error:
                logging.error(f'"{class_name}.{kc.KEY_CUSTOM_FLATTENING}" section in config should '
                              f'have a "{kc.KEY_FUNCTION}" entry!')
                raise error
            args = [o, flatten_object, headers]
            flatten_object = getattr(custom_flat_module, custom_flat_func)(*args)
            if kc.KEY_CONTAINS_CHILD in custom_flat_meta:
                if custom_flat_meta[kc.KEY_CONTAINS_CHILD]:
                    children = flatten_object[0:-1]
                    flatten_object = flatten_object[-1]
                    for child in children:
                        flatten_child(child, config, headers, flatten_object, o)
    return flatten_object


def write_flattened_to_csv(headers: HeaderList, flattened_object: flattened_type, f, delimiter: str = ";"):
    obj_str: str = ""
    if flattened_object and flattened_object.attrib_map:
        for key in headers:
            obj_str += (flattened_object.attrib_map[key] if key in flattened_object.attrib_map else "") + delimiter
        f.write(obj_str + "\n")
        if flattened_object.children:
            for child in flattened_object.children:
                write_flattened_to_csv(headers, child, f)


def write_to_csv(headers: HeaderList, flattened_objects, file: str, delimiter: str = ";"):
    def title_string(headers: HeaderList):
        title: str = ""
        for field in headers:
            title += field + delimiter
        return title

    with open(file, "w") as f:
        f.write(title_string(headers) + "\n")
        for obj in flattened_objects:
            write_flattened_to_csv(headers, obj, f)
