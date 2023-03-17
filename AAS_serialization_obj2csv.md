Table of Contents

1.	Overview 
2.	Format of TOML File
2.1.	[Type]
2.2.	[[Type.attribute]]
2.3.	[[Type.child]]
2.4.	[Type.custom_flattening]
3.	Example 
4.	Custom Flatteners
5.	Infer Attributes from Parent Type

1.	Overview
The flattening API is a tool that allows users to convert AAS objects into a CSV file. This specification file outlines the API and the format of the TOML file required to flatten objects into a CSV file. The TOML file is a text-based configuration file that contains the necessary information to flatten objects into a CSV file. The TOML file contains the following information: the object type, the object attributes, information about connected objects to current object, and information regarding custom flattening code. 

Once the TOML file is generated, the flattening API can be employed to convert the object into a CSV file. This API will accept the TOML file and AAS objects as input and will produce a CSV file that contains the flattened object. The CSV file will contain the attributes specified in the TOML file. This CSV file can then be used to store the flattened object in a database or to be used in other applications such as modelling on the objects.

This specification file outlines the API and the format of the TOML file required to flatten objects into a CSV file.

2.	Format of TOML File
The following is the format of the TOML file required to flatten objects into a CSV file:
2.1.	[Type]
This section of the TOML file contains the configuration for each Object type. This section include the following fields:
•	object_type: (optional) The name of the type of the Object, if it is different from classname. 
•	id_field: (optional) The attribute name that corresponds to the ID of the object. If the object has any children, an id_field must be specified. If no id_field is provided, the API will generate a random ID in the format {object_type}_{object_uuid}.


2.2.	[[Type.attribute]]
This section provides details about list of attributes related to a specific object type. It includes following fields:
•	name: (mandatory) The name of the attribute.
•	include: (optional) This boolean flag indicates if the attribute should be included or not. 
•	cast_into: (optional) The data type into which attribute value should be changed or "cast" into. For example, "str" or "int".

2.3.	[[Type.child]]
This section provides details about child objects connected to Type. It includes following fields:
•	is_list: (mandatory) This Boolean flag specifies whether there is a single object associated with the Type, or a collection of objects.
•	attribute_name: (mandatory) This is the attribute name to query the connected objects.
•	child_module: (optional) The module name this connected object type belongs to is used for filtering if there are multiple type of objects connected to the same attribute name.
•	child_type: (optional) The class name of the connected object. It is used for filtering if there are multiple type of objects connected to the same attribute name.
2.4.	[Type.custom_flattening]
This section allows specifying any custom functionality related to the Type. It includes following fields:
•	module: (mandatory) The name of the module containing custom functionality related to the Type.
•	function: (mandatory) The name of the function containing custom functionality related to the Type.


3.	Example of TOML configuration
The following sample TOML file outlines the configuration for a Type, “Submodel”:

`[Submodel]
object_type = "Submodel"
id_field = "id_short"
[[Submodel.attribute]]
name = "id_short"
include = true
[[Submodel.attribute]]
name = "category"
include = false
[Submodel.custom_flattening]
module = "customflatteners"
function = "flatten_Submodel"
returns_child = true
[[Submodel.child]]  
is_list = true
child_module = "basyx.aas.model"
child_type = "Qualifier"
attribute_name="qualifier"`



4.	Custom Flatteners
If we need to create custom functionality to flatten an object. We must specify the module and function that contain the custom code in the configuration file. The signature for the function must contain these arguments:
•	object_type: The object that is being flattened
•	flat_obj: The flattened object of type flattened_type
•	headers: List of type HeaderList, containing headers to be written in csv.

Example custom flattener signature,

`def flatten_Submodel(o: model.Submodel, flat_obj: flattened_type, headers: HeaderList)`


5.	Infer Attributes from Parent Type
If an object type has an entry in the configuration file, the API will automatically reference attributes from the parent type of the object being flattened. Therefore, attributes belonging to the parent type do not need to be specified in the child type, as they are automatically inferred. Moreover, when there is no entry of a particular object type in the configuration, the object will be flattened based solely on its parent type entries in the configuration file. 
