import toml
import pandas as pd
import key_constants as kc
from importlib import import_module
import util
import logging

DEFAULT_DELIM = ";"


def create_new_object(init_meta, df):
    id_vars = init_meta[kc.KEY_CONSTRUCTOR_ARG]
    const_args = dict()
    for var in id_vars.split(","):
        const_args.update({var: getattr(df, var)})
    module_name = init_meta[kc.KEY_OBJECT_MODULE]
    class_name = init_meta[kc.KEY_OBJECT_CLASS]
    module = import_module(module_name)
    obj_class = getattr(module, class_name)
    return obj_class(**const_args)


def set_values(obj, df, object_meta):
    attribs = object_meta[kc.KEY_ATTRIBUTES]
    for attrib in attribs.split(","):
        if hasattr(df, attrib):
            setattr(obj, attrib, getattr(df, attrib))


def csvtoobj(csvfilepath: str, configfilepath: str):
    dfs = pd.read_csv(csvfilepath, delimiter=DEFAULT_DELIM)
    csv2obj_config = toml.load(configfilepath)
    obj_list = dict()
    for df in dfs.itertuples():
        if hasattr(df, kc.KEY_OBJECT_TYPE):
            object_type = getattr(df, kc.KEY_OBJECT_TYPE)
            if object_type in csv2obj_config:
                object_meta = csv2obj_config[object_type]
                if kc.KEY_INIT in object_meta:
                    init_meta = object_meta[kc.KEY_INIT]
                    obj = create_new_object(init_meta, df)
                elif kc.KEY_CUSTOM_INIT in object_meta:
                    custom_init_meta = object_meta[kc.KEY_CUSTOM_INIT]
                    custom_init_module = import_module(custom_init_meta[kc.KEY_MODULE])
                    custom_init_func = custom_init_meta[kc.KEY_FUNCTION]
                    args = [df]
                    obj = getattr(custom_init_module, custom_init_func)(*args)
                set_values(obj, df, object_meta)
                if kc.KEY_ID_FIELD in object_meta:
                    id_field = object_meta[kc.KEY_ID_FIELD]
                    obj_list.update({getattr(obj, id_field): obj})
                if hasattr(df, kc.KEY_HEADER_PARENT_ID):
                    parent_id = str(getattr(df, kc.KEY_HEADER_PARENT_ID))
                    if parent_id != "nan" and kc.KEY_PARENT in object_meta:
                        if parent_id in obj_list:
                            parent_obj = obj_list[parent_id]
                            parent_metas = object_meta[kc.KEY_PARENT]
                            for par_meta in parent_metas:
                                parent_module = par_meta[kc.KEY_PARENT_MODULE]
                                par_class = util.load_module(kc.KEY_parent_package, parent_module)
                                if isinstance(parent_obj, par_class):
                                    child_list = getattr(parent_obj, par_meta[kc.KEY_PARENT_ATTRIB])
                                    child_list.add(obj)
                                    break
    logging.info(f'Converted {len(obj_list.keys())} objects from CSV.')
    return obj_list
