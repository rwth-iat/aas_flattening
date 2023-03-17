import copy
from generic_data import flattened_type
from basyx.aas import model
from basyx.aas.util import traversal
from header_list import HeaderList
import util


def add_type_to_obj(o, flat_obj: flattened_type, headers: HeaderList):
    kind = o.kind
    flat_obj.append_attrib_val_pair({"kind": "INSTANCE" if kind is model.ModelingKind.INSTANCE else "TEMPLATE"})
    headers.append("kind")


def flatten_Submodel(o: model.Submodel, flat_obj: flattened_type, headers: HeaderList):
    add_type_to_obj(o, flat_obj, headers)
    childs = list(o.submodel_element)
    childs.append(flat_obj)
    return childs


def flatten_MultiLanguageProperty(o: model.MultiLanguageProperty, flat_obj: flattened_type, headers: HeaderList):
    add_type_to_obj(o, flat_obj, headers)
    objects = [flat_obj]
    if o.value:
        objects = []
    for lang, string in o.value.items():
        flat_obj = copy.deepcopy(flat_obj)
        flat_obj.append_attrib_val_pair({"value": f'{{"{lang}": "{string}"}}'})
        headers.append("value")
        if not objects:
            objects = []
        objects.append(flat_obj)
    return objects


def flatten_Range(o: model.Range, flat_obj: flattened_type, headers: HeaderList):
    min_flat = copy.deepcopy(flat_obj)
    max_flat = copy.deepcopy(flat_obj)
    min_flat.append_attrib_val_pair({"object_type": "Range.min"})
    max_flat.append_attrib_val_pair({"object_type": "Range.max"})
    headers.append("object_type")
    min_flat.append_attrib_val_pair({"value": str(o.min)})
    max_flat.append_attrib_val_pair({"value": str(o.max)})
    headers.append("value")
    return [min_flat, max_flat]


def flatten_AnnotatedRelationshipElement(o: model.AnnotatedRelationshipElement, flat_obj: flattened_type,
                                         headers: HeaderList):
    flat_obj.append_attrib_val_pair({"value": f'["{str(o.first)}", "{str(o.second)}"]'})
    headers.append("value")
    return flat_obj


def flatten_RelationshipElement(o: model.RelationshipElement, flat_obj: flattened_type,
                                headers: HeaderList):
    flat_obj.append_attrib_val_pair({"value": f'["{str(o.first)}", "{str(o.second)}"]'})
    headers.append("value")
    return flat_obj


def flatten_Property(o: model.Property, flat_obj: flattened_type,
                     headers: HeaderList):
    flat_obj.append_attrib_val_pair({"value_type": util.get_simple_class_name_from_type(o.value_type).lower()})
    headers.append("value_type")
    return flat_obj
