<ol>
<li><h3>Overview</h3>
This specification file outlines the API and the format of the TOML file required to convert rows in a CSV File into AAS objects. The TOML file is a configuration file that contains the mapping between the CSV file and the AAS objects. It is used to define the structure of the AAS objects and the mapping between the CSV file and the AAS objects. 

The API code uses TOML configuration for the conversion process. The default delimiter used to parse the CSV file is a semicolon, however you can change it by modifying DEFAULT_DELIM variable in the API code. The TOML file is used to define the structure of the AAS objects and the mapping between the CSV file and the AAS objects. The TOML file contains the following information: the object type, the object attributes, the information on how to initialize the object and the information regarding connecting an object to its parent object.

This specification file outlines the API and the format of the TOML file required to convert rows in a CSV File into AAS objects.
</li>

<li><h3>Format of TOML-File</h3>
The following is the format of the TOML file required to convert a CSV file into list of objects:
<ol><li><h4>[Type]</h4>
This section of the TOML file contains the configuration for each Object type. This section includes the following fields:
<ul>
<li><b>id_field</b>: (required) The column name in csv that corresponds to the ID of the object. API uses it for indexing the created object in memory using dict.</li>
<li><b>attributes</b>: (optional) A comma separated list of attributes.</li>
</ul>
An object of a Type can be initialized in two ways, the generic way which is described in next section or a custom way, which is described further. When defining the configuration make sure for a type only one type of initialization is considered either generic or custom.
</li>

<li><h4>[Type.init]</h4>
This section provides details about the general initialization of the object. It includes following fields:
<ul>
<li><b>object_module</b>: (required) The module name in which the class for the Type exists.</li>
<li><b>object_class</b>: (required) The classname of a particular type.</li>
<li><b>constructor_args</b>: (required) The comma separated attributes of a type that goes in the constructor call to initialize the object.</li>
</ul>
</li>


<li><h4>[Type.custom_init]</h4>
This section provides details about the custom initialization of the object. It includes following fields:
<ul>
<li><b>module</b>: (required) The module name of the custom initializers.</li>
<li><b>function</b>: (required) The function name that handles custom initialization for a type.</li>
</ul>
</li>
<li><h4>[[Type.parent]]</h4>
This section provides details about the connecting initialization of the object. It includes following fields:
<ul>
<li><b>parent_package</b>: (required) The module name for the class for the parent type.</li>
<li><b>parent_module</b>: (required) The class name of the parent type.</li>
<li><b>parent_attrib</b>: (required) The attribute (list) in the parent type that holds the Type object.</li>
</ul>
</li>
</ol>
<li>
<h3>Example of TOML configuration</h3>
The following sample TOML file outlines the configuration for a Type, “Submodel”:

`[Submodel]`<br>
`id_field = "id_short"`<br>
`attributes = "id_short,semantic_id"`<br>
`[Submodel.init]`<br>
`object_module = "basyx.aas.model"`<br>
`object_class = "Submodel"`<br>
`constructor_args = "identification,kind"`<br>

Another example of TOML file configuration for Type, “Property”. 

`[Property]`<br>
`id_field = "id_short"`<br>
`attributes = "value_id"`<br>
`[Property.custom_init]`<br>
`module = "custominitializers"`<br>
`function = "init_Property"`<br>
`[[Property.parent]]`<br>
`parent_package = "basyx.aas.model"`<br>
`parent_module = "Submodel"`<br>
`parent_attrib = "submodel_element"`<br>
`[[Property.parent]]`<br>
`parent_package = "basyx.aas.model"`<br>
`parent_module = "SubmodelElementCollection"`<br>
`parent_attrib = "value"`<br>

Here in the Property Type config example, the custom initializer method is used to initialize Property Object. Moreover, the details about its parent connection are also specified. A property can have two types of parents, Submodel and SubmodelElementCollection.
</li>

<li><h3>Custom Initializers</h3>
It is used to initialize an object of a particular type in a custom way. We must specify the module and function that contain the custom code in the configuration file. The signature for the function must contain these arguments:
<ul>
<li>df: The dataframe (Pandas) that represents the row in a CSV.</li>
</ul>

Example custom flattener signature,

`def init_Property(df)`
</li>
</ol>
