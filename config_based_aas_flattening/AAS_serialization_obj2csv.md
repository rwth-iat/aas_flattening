<ol><h3>Overview</h3>
The flattening API is a tool that allows users to convert AAS objects into a CSV file. This specification file outlines the API and the format of the TOML file required to flatten objects into a CSV file. The TOML file is a text-based configuration file that contains the necessary information to flatten objects into a CSV file. The TOML file contains the following information a specific object type: the object type, the object attributes, information about connected objects to object type, and information regarding custom flattening code, if required for an object type. 

Once the TOML file is defined, the flattening API can be employed to convert the object into a CSV file. This API will accept the TOML file and AAS objects as input and will produce a CSV file that contains the flattened object. The CSV file will contain for every object, its attributes and linkages to other related objects. This CSV file can then be used to store the flattened object in a database or to be used in other applications such as doing modelling on the objects.

This specification file outlines the API and the format of the TOML file required to flatten objects into a CSV file.

<li><h3>Format of TOML File</h3>
The following is the format of the TOML file required to flatten objects into a CSV file:
<ol>
<li><h4>[Type]</h4>
This section of the TOML file contains the configuration for each Object type. This section include the following fields:
<ul>
<li><b>object_type</b>: (optional) The name of the type of the Object, if it is different from classname.</li> 
<li><b>id_field</b>: (optional) The attribute name that corresponds to the ID of the object. If the object has any children, an id_field must be specified. If no id_field is provided, the API will generate a random ID in the format {object_type}_{object_uuid} and use it to link the object to its related objects.</li>
</ul>
</li>

<li><h4>[[Type.attribute]]</h4>
This section provides details about list of attributes related to a specific object type. It includes following fields:
<ul>
<li><b>name</b>: (mandatory) The name of the attribute.</li>
<li><b>include</b>: (optional) This boolean flag indicates if the attribute should be included or not. </li>
<li><b>cast_into</b>: (optional) The python data type into which attribute value should be changed or "cast" into. For example, "str" or "int".</li>
</ul>
</li>
<li><h4>[[Type.child]]</h4>
This section provides details about child objects connected to Type. It includes following fields:
<ul>
<li><b>is_list</b>: (mandatory) This Boolean flag specifies whether there is a single object associated with the Type, or a collection of objects.</li>
<li><b>attribute_name</b>: (mandatory) This is the attribute name to query the connected objects.</li>
<li><b>child_module</b>: (optional) The module name this connected object type belongs to is used for filtering if there are multiple type of objects connected to the same attribute name.</li>
<li><b>child_type</b>: (optional) The class name of the connected object. It is used for filtering if there are multiple type of objects connected to the same attribute name.</li>
</ul>
</li>
<li>
<h4>[Type.custom_flattening]</h4>
This section allows specifying any custom functionality related to the Type. It includes following fields:
<ul>
<li><b>module</b>: (mandatory) The name of the module containing custom functionality related to the Type.</li>
<li><b>function</b>: (mandatory) The name of the function containing custom functionality related to the Type.</li>
</ul>
</li>
</ol>

<li>
<h3>Example of TOML configuration</h3>
The following sample TOML file outlines the configuration for a Type, “Submodel”:

`[Submodel]`<br>
`object_type = "Submodel"`<br>
`id_field = "id_short"`<br>
`[[Submodel.attribute]]`<br>
`name = "id_short"`<br>
`include = true`<br>
`[[Submodel.attribute]]`<br>
`name = "category"`<br>
`include = false`<br>
`[Submodel.custom_flattening]`<br>
`module = "customflatteners"`<br>
`function = "flatten_Submodel"`<br>
`returns_child = true`<br>
`[[Submodel.child]] `<br>
`is_list = true`<br>
`child_module = "basyx.aas.model"`<br>
`child_type = "Qualifier"`<br>
`attribute_name="qualifier"`<br>
</li>

<li>
<h4>Custom Flatteners</h4>
If we need to create custom functionality to flatten an object. For special cases if the flattening for an object can't be handled by above configuration. To do that, we must specify the module and function that contain the custom code in the configuration file in the object specification. Below is an example for the configuration of object_type "Property", to use custom Flattening.<br>
  
`[Property]`<br>
`object_type = "Property"`<br>
`[Property.custom_flattening]`<br>
`module = "config_based_aas_flattening.objtocsv.customflatteners"`<br>
`function = "flatten_Property"`<br>

In the module file, where we actually define the custom flattening method, the signature for the function must contain these arguments:
<ul>	
<li><b>object_type</b>: The object that is being flattened</li>
<li><b>flat_obj</b>: The flattened object of type flattened_type</li>
<li><b>headers</b>: List of type HeaderList, containing headers to be written in csv.
</ul>

Example custom flattener signature,

`def flatten_Submodel(o: model.Submodel, flat_obj: flattened_type, headers: HeaderList)`
</li>

<li>
<h3>Infer Attributes from Parent Type</h3>
If an object type has an entry in the configuration file, the API will automatically reference attributes from the parent type of the object being flattened. Therefore, attributes belonging to the parent type do not need to be specified in the child type, as they are automatically inferred. Moreover, when there is no entry of a particular object type in the configuration, the object will be flattened based solely on its parent type entries in the configuration file.
</li>
</ol>
