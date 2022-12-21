import dataclasses
from typing import Optional, List

from basyx.aas import model
from basyx.aas.util import traversal


def none_to_empty_string(o: Optional[str]) -> str:
    if o is None:
        return ""
    else:
        return o


@dataclasses.dataclass
class FlatSubmodelObject:
    parent: Optional["FlatSubmodelObject"] = None
    children: Optional[List["FlatSubmodelObject"]] = None
    object_type: Optional[str] = None
    id_short: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    semantic_id: Optional[str] = None
    kind: Optional[str] = None
    identifier: Optional[str] = None
    administrative_information: Optional[str] = None
    value: Optional[str] = None
    value_type: Optional[str] = None
    value_id: Optional[str] = None

    def add_child(self, child: "FlatSubmodelObject"):
        if self.children is None:
            self.children = [child]
        else:
            self.children.append(child)

    def to_csv_string(
            self,
            delimiter: str = "; ",
            include_object_type: bool = True,
            include_id_short: bool = True,  # Note: Do not set to False, as it would generate nonsensical output
            include_category: bool = False,
            include_description: bool = False,
            include_semantic_id: bool = True,
            include_kind: bool = False,
            include_identification: bool = True,
            include_administrative_information: bool = False,
            include_value: bool = True,  # Note: Do not set to False, as it would generate nonsensical output
            include_value_type: bool = False,
            include_value_id: bool = False
    ) -> str:
        return_string: str = ""
        if include_object_type:
            return_string += none_to_empty_string(self.object_type) + delimiter
        if include_id_short:
            return_string += none_to_empty_string(self.id_short) + delimiter
        if include_category:
            return_string += none_to_empty_string(self.category) + delimiter
        if include_description:
            return_string += none_to_empty_string(self.description) + delimiter
        if include_semantic_id:
            return_string += none_to_empty_string(self.semantic_id) + delimiter
        if include_kind:
            return_string += none_to_empty_string(self.kind) + delimiter
        if include_identification:
            return_string += none_to_empty_string(self.identifier) + delimiter
        if include_administrative_information:
            return_string += none_to_empty_string(self.administrative_information) + delimiter
        if include_value:
            return_string += none_to_empty_string(self.value) + delimiter
        if include_value_type:
            return_string += none_to_empty_string(self.value_type) + delimiter
        if include_value_id:
            return_string += none_to_empty_string(self.value_id) + delimiter
        return return_string


class SubmodelFlattener:
    def __init__(
            self,
            include_object_type: bool = True,
            include_id_short: bool = True,  # Note: Do not set to False, as it would generate nonsensical stuff
            include_category: bool = False,
            include_description: bool = False,
            include_semantic_id: bool = True,
            include_qualifier: bool = False,
            include_kind: bool = False,
            include_identification: bool = True,
            include_administrative_information: bool = False,
            include_value: bool = True,  # Note: Do not set to False, as it would generate nonsensical stuff
            include_value_type: bool = False,
            include_value_id: bool = False
    ):
        self.include_object_type: bool = include_object_type
        self.include_id_short: bool = include_id_short
        self.include_category: bool = include_category
        self.include_description: bool = include_description
        self.include_semantic_id: bool = include_semantic_id
        self.include_qualifier: bool = include_qualifier
        self.include_kind: bool = include_kind
        self.include_identification: bool = include_identification
        self.include_administrative_information: bool = include_administrative_information
        self.include_value: bool = include_value
        self.include_value_type: bool = include_value_type
        self.include_value_id: bool = include_value_id

    def submodel_to_csv(self, o: model.Submodel, file: str, delimiter: str = "; "):
        """
        Takes a submodel, flattens it and outputs it to a CSV file

        :param o:
        :param file:
        :param delimiter: The CSV delimiter
        """
        flat_submodel = self.flatten_submodel(o)

        def title_string() -> str:
            title: str = ""
            if self.include_object_type:
                title += "ObjectType" + delimiter
            if self.include_id_short:
                title += "idShort" + delimiter
            if self.include_category:
                title += "Category" + delimiter
            if self.include_description:
                title += "Description" + delimiter
            if self.include_semantic_id:
                title += "SemanticID" + delimiter
            if self.include_kind:
                title += "Kind" + delimiter
            if self.include_identification:
                title += "Identifier" + delimiter
            if self.include_administrative_information:
                title += "AdministrativeInformation" + delimiter
            if self.include_value:
                title += "Value" + delimiter
            if self.include_value_type:
                title += "ValueType" + delimiter
            if self.include_value_id:
                title += "ValueID" + delimiter
            return title

        with open(file, "w") as f:
            f.write(title_string() + "\n")

            def recursive_write_flat_submodel_object(fso: FlatSubmodelObject):
                f.write(fso.to_csv_string(
                    delimiter,
                    self.include_object_type,
                    self.include_id_short,
                    self.include_category,
                    self.include_description,
                    self.include_semantic_id,
                    self.include_kind,
                    self.include_identification,
                    self.include_administrative_information,
                    self.include_value,
                    self.include_value_type,
                    self.include_value_id
                ))
                f.write("\n")
                if fso.children is not None:
                    for child in fso.children:
                        recursive_write_flat_submodel_object(child)

            recursive_write_flat_submodel_object(flat_submodel)

    def flatten_submodel(self, o: model.Submodel) -> FlatSubmodelObject:
        flat_submodel_object: FlatSubmodelObject = FlatSubmodelObject()
        if self.include_object_type:
            flat_submodel_object.object_type = "Submodel"
        if self.include_identification:
            flat_submodel_object.identifier = self._flatten_identifier(o.identification)
        if self.include_id_short:
            flat_submodel_object.id_short = o.id_short
        if self.include_category:
            flat_submodel_object.category = o.category
        if self.include_description:
            flat_submodel_object.description = o.description
        if self.include_administrative_information:
            flat_submodel_object.administrative_information = self._flatten_administrative_information(o.administration)
        if self.include_semantic_id:
            flat_submodel_object.semantic_id = self._flatten_reference(o.semantic_id)
        if self.include_qualifier:
            # Todo: Constraints are so abstract, we cannot flatten them
            # Todo: We could, in theory however flatten Formulas
            for qualifier in o.qualifier:
                if isinstance(qualifier, model.Qualifier):
                    self._flatten_qualifier(flat_submodel_object, qualifier)
        if self.include_kind:
            flat_submodel_object.kind = self._flatten_kind(o.kind)
        # Traverse SubmodelElements and flatten them as well
        for submodel_element in traversal.walk_submodel(o):
            # todo: Check if this is what we want, maybe we better do it manually
            self._flatten_submodel_element(flat_submodel_object, submodel_element)
        return flat_submodel_object

    @staticmethod
    def _flatten_reference(o: model.Reference) -> str:
        return str(o)

    @staticmethod
    def _flatten_administrative_information(o: model.AdministrativeInformation) -> str:
        return str(o)

    @staticmethod
    def _flatten_identifier(o: model.Identifier) -> str:
        return str(o)

    def _flatten_qualifier(self, parent: FlatSubmodelObject, o: model.Qualifier):
        flat_qualifier: FlatSubmodelObject = FlatSubmodelObject(parent=parent)
        if self.include_object_type:
            flat_qualifier.object_type = "Qualifier"
        # Todo: What to do with QualifierType
        if self.include_value:
            flat_qualifier.value = self._flatten_value_data_type(o.value)
        if self.include_value_id:
            flat_qualifier.value_id = self._flatten_reference(o.value_id)
        if self.include_value_type:
            flat_qualifier.value_type = self._flatten_value_data_type(o.value)
        if self.include_semantic_id:
            flat_qualifier.semantic_id = self._flatten_reference(o.semantic_id)
        parent.add_child(flat_qualifier)

    @staticmethod
    def _flatten_value_data_type(o: model.ValueDataType) -> str:
        return str(o)

    @staticmethod
    def _flatten_kind(o: model.ModelingKind) -> str:
        if o is model.ModelingKind.INSTANCE:
            return "INSTANCE"
        else:
            return "TEMPLATE"

    def _flatten_submodel_element(self, parent: FlatSubmodelObject, o: model.SubmodelElement):
        if isinstance(o, model.Property):
            self._flatten_property(parent, o)
        elif isinstance(o, model.MultiLanguageProperty):
            self._flatten_multi_language_property(parent, o)
        elif isinstance(o, model.Range):
            self._flatten_range(parent, o)
        elif isinstance(o, model.Blob):
            self._flatten_blob(parent, o)
        elif isinstance(o, model.File):
            self._flatten_file(parent, o)
        elif isinstance(o, model.ReferenceElement):
            self._flatten_reference_element(parent, o)
        elif isinstance(o, model.SubmodelElementCollection):
            self._flatten_submodel_element_collection(parent, o)
        elif isinstance(o, model.AnnotatedRelationshipElement):
            self._flatten_annotated_relationship_element(parent, o)
        elif isinstance(o, model.RelationshipElement):
            self._flatten_relationship_element(parent, o)
        elif isinstance(o, model.Operation):
            self._flatten_operation(parent, o)
        elif isinstance(o, model.Capability):
            self._flatten_capability(parent, o)
        elif isinstance(o, model.Entity):
            self._flatten_entity(parent, o)
        elif isinstance(o, model.Event):
            self._flatten_event(parent, o)

    def _flatten_abstract_submodel_element_attributes(self, p: FlatSubmodelObject, o: model.SubmodelElement) -> FlatSubmodelObject:
        flat_submodel_object: FlatSubmodelObject = FlatSubmodelObject()
        flat_submodel_object.parent = p
        if self.include_id_short:
            flat_submodel_object.id_short = o.id_short
        if self.include_category:
            flat_submodel_object.category = o.category
        if self.include_description:
            flat_submodel_object.description = str(o.description)  # todo: Double Check
        if self.include_semantic_id:
            flat_submodel_object.semantic_id = self._flatten_reference(o.semantic_id)
        if self.include_qualifier:
            # Todo: Constraints are so abstract, we cannot flatten them
            # Todo: We could, in theory however flatten Formulas
            for qualifier in o.qualifier:
                if isinstance(qualifier, model.Qualifier):
                    self._flatten_qualifier(flat_submodel_object, qualifier)
        if self.include_kind:
            flat_submodel_object.kind = self._flatten_kind(o.kind)
        return flat_submodel_object

    def _flatten_property(self, p: FlatSubmodelObject, o: model.Property):
        flat_submodel_object: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_submodel_object.object_type = "Property"
        if self.include_value:
            flat_submodel_object.value = str(o.value)
        if self.include_value_type:
            flat_submodel_object.value_type = self._flatten_value_data_type(o.value)
        if self.include_value_id:
            flat_submodel_object.value_id = self._flatten_reference(o.value_id)
        # Add the new FlatSubmodelObject to its parent's children
        p.add_child(flat_submodel_object)

    def _flatten_multi_language_property(self, p: FlatSubmodelObject, o: model.MultiLanguageProperty):
        for lang, string in o.value.items():
            flat_submodel_object: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
            if self.include_object_type:
                flat_submodel_object.object_type = "MultiLanguageProperty"
            if self.include_value:
                flat_submodel_object.value = f'{{"{lang}": "{string}"}}'
            if self.include_value_id:
                flat_submodel_object.value_id = self._flatten_reference(o.value_id)
            # Add the new FlatSubmodelObject to its parent's children
            p.add_child(flat_submodel_object)

    def _flatten_range(self, p: FlatSubmodelObject, o: model.Range):
        min_flat = self._flatten_abstract_submodel_element_attributes(p, o)
        max_flat = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            min_flat.object_type = "Range.min"
            max_flat.object_type = "Range.max"
        if self.include_value:
            min_flat.value = self._flatten_value_data_type(o.min)
            max_flat.value = self._flatten_value_data_type(o.max)
            # Add the new FlatSubmodelObject to its parent's children
            p.add_child(min_flat)
            p.add_child(max_flat)

    def _flatten_blob(self, p: FlatSubmodelObject, o: model.Blob):
        flat_submodel_object: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_submodel_object.object_type = "Blob"
        # Todo: How do we handle mime_type?
        # Todo: It probably does not make sense to include the value here
        # Add the new FlatSubmodelObject to its parent's children
        p.add_child(flat_submodel_object)

    def _flatten_file(self, p: FlatSubmodelObject, o: model.File):
        flat_submodel_object: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_submodel_object.object_type = "File"
        # Todo: How do we handle mime_type?
        if self.include_value:
            flat_submodel_object.value = str(o.value)
        # Add the new FlatSubmodelObject to its parent's children
        p.add_child(flat_submodel_object)

    def _flatten_reference_element(self, p: FlatSubmodelObject, o: model.ReferenceElement):
        flat_submodel_object: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_submodel_object.object_type = "ReferenceElement"
        if self.include_value:
            flat_submodel_object.value = self._flatten_reference(o.value)
        # Add the new FlatSubmodelObject to its parent's children
        p.add_child(flat_submodel_object)

    def _flatten_submodel_element_collection(self, p: FlatSubmodelObject, o: model.SubmodelElementCollection):
        flat_collection: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_collection.object_type = "SubmodelElementCollection"
        # Here, not including value does not make sense, so always include it
        for submodel_element in o.value:
            self._flatten_submodel_element(flat_collection, submodel_element)
        p.add_child(flat_collection)

    def _flatten_relationship_element(self, p: FlatSubmodelObject, o: model.RelationshipElement):
        flat_relation: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_relation.object_type = "RelationshipElement"
        if self.include_value:
            flat_relation.value = f'["{self._flatten_reference(o.first)}", "{self._flatten_reference(o.second)}"]'
        # Add the new FlatSubmodelObject to its parent's children
        p.add_child(flat_relation)

    def _flatten_annotated_relationship_element(self, p: FlatSubmodelObject, o: model.AnnotatedRelationshipElement):
        flat_relation: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_relation.object_type = "AnnotatedRelationshipElement"
        if self.include_value:
            flat_relation.value = f'["{self._flatten_reference(o.first)}", "{self._flatten_reference(o.second)}"]'
        for data_element in o.annotation:
            self._flatten_submodel_element(flat_relation, data_element)
        # Add the new FlatSubmodelObject to its parent's children
        p.add_child(flat_relation)

    def _flatten_operation(self, p: FlatSubmodelObject, o: model.Operation):
        flat_submodel_object: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_submodel_object.object_type = "Operation"
        if o.input_variable:
            for variable in o.input_variable:
                self._flatten_submodel_element(flat_submodel_object, variable)
        if o.output_variable:
            for variable in o.output_variable:
                self._flatten_submodel_element(flat_submodel_object, variable)
        if o.in_output_variable:
            for variable in o.in_output_variable:
                self._flatten_submodel_element(flat_submodel_object, variable)
        # Add the new FlatSubmodelObject to its parent's children
        p.add_child(flat_submodel_object)

    def _flatten_capability(self, p: FlatSubmodelObject, o: model.Capability):
        flat_submodel_object: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_submodel_object.object_type = "Capability"
        # Add the new FlatSubmodelObject to its parent's children
        p.add_child(flat_submodel_object)

    def _flatten_entity(self, p: FlatSubmodelObject, o: model.Entity):
        flat_submodel_object: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_submodel_object.object_type = "Entity"
        # Todo: How to deal with EntityType?
        for submodel_element in o.statement:
            self._flatten_submodel_element(flat_submodel_object, submodel_element)
        if self.include_value:
            flat_submodel_object.value = self._flatten_reference(o.asset)
        # Add the new FlatSubmodelObject to its parent's children
        p.add_child(flat_submodel_object)

    def _flatten_event(self, p: FlatSubmodelObject, o: model.Event):
        flat_submodel_object: FlatSubmodelObject = self._flatten_abstract_submodel_element_attributes(p, o)
        if self.include_object_type:
            flat_submodel_object.object_type = "Event"
        # Add the new FlatSubmodelObject to its parent's children
        p.add_child(flat_submodel_object)
