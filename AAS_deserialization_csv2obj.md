Table of Contents

1.	Overview 
2.	Format of TOML-File
2.1.	[Type]
2.2.	[Type.init]
2.3.	[Type.custom_init]
2.4.	[[Type.parent]]
3.	Example 
4.	Custom Flatteners

1.	Overview
This specification file outlines the API and the format of the TOML file required to convert rows in a CSV File into AAS objects. The TOML file is a configuration file that contains the mapping between the CSV file and the AAS objects. It is used to define the structure of the AAS objects and the mapping between the CSV file and the AAS objects. 

The API code uses TOML configuration for the conversion process. The default delimiter used to parse the CSV file is a semicolon, however you can change it by modifying DEFAULT_DELIM variable in the API code. The TOML file is used to define the structure of the AAS objects and the mapping between the CSV file and the AAS objects. The TOML file contains the following information: the object type, the object attributes, the information on how to initialize the object and the information regarding connecting an object to its parent object.

This specification file outlines the API and the format of the TOML file required to convert rows in a CSV File into AAS objects.

2.	Format of TOML-File
The following is the format of the TOML file required to convert a CSV file into list of objects:
2.1.	[Type]
This section of the TOML file contains the configuration for each Object type. This section includes the following fields:
•	Id_field: (required) The column name in csv that corresponds to the ID of the object. API uses it for indexing the created object in memory using dict.
•	attributes: (optional) A comma separated list of attributes.

An object of a Type can be initialized in two ways, the generic way which is described in section 2.2 or a custom way, which is described in section 2.3. When defining the configuration make sure for a type only one type of initialization is considered either generic or custom.


2.2.	[Type.init]
This section provides details about the general initialization of the object. It includes following fields:
•	object_module: (required) The module name in which the class for the Type exists.
•	object_class: (required) The classname of a particular type.
•	constructor_args: (required) The comma separated attributes of a type that goes in the constructor call to initialize the object.



2.3.	[Type.custom_init]
This section provides details about the custom initialization of the object. It includes following fields:
•	module: (required) The module name of the custom initializers.
•	function: (required) The function name that handles custom initialization for a type.

2.4.	[[Type.parent]]
This section provides details about the connecting initialization of the object. It includes following fields:
•	parent_package: (required) The module name for the class for the parent type.
•	parent_module: (required) The class name of the parent type.
•	parent_attrib: (required) The attribute (list) in the parent type that holds the Type object.

3.	Example of TOML configuration
The following sample TOML file outlines the configuration for a Type, “Submodel”:

`[Submodel]
id_field = "id_short"
attributes = "id_short,semantic_id"
[Submodel.init]
object_module = "basyx.aas.model"
object_class = "Submodel"
constructor_args = "identification,kind"`

Another example of TOML file configuration for Type, “Property”. 

`[Property]
id_field = "id_short"
attributes = "value_id"
[Property.custom_init]
module = "custominitializers"
function = "init_Property"
[[Property.parent]]
parent_package = "basyx.aas.model"
parent_module = "Submodel"
parent_attrib = "submodel_element"
[[Property.parent]]
parent_package = "basyx.aas.model"
parent_module = "SubmodelElementCollection"
parent_attrib = "value"`

Here in the Property Type config example, the custom initializer method is used to initialize Property Object. Moreover, the details about its parent connection are also specified. A property can have two types of parents, Submodel and SubmodelElementCollection.


4.	Custom Initializers
It is used to initialize an object of a particular type in a custom way. We must specify the module and function that contain the custom code in the configuration file. The signature for the function must contain these arguments:
•	df: The dataframe (Pandas) that represents the row in a CSV.

Example custom flattener signature,

`def init_Property(df)`

