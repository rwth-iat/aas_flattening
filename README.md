# AAS Flattening Algorithm

A (WIP) collection of algorithms for Asset Administration Shell data analysis, based on the 
[Eclipse BaSyx Python SDK](https://github.com/eclipse-basyx/basyx-python-sdk).

## SubmodelFlattener

This algorithm is capable of transforming a given `Submodel` into a `FlatSubmodelObject` structure. 
The information contained in the `FlatSubmodelObject` structure can be defined using the `include_`-switches when 
instantiating the `SubmodelFlattener`-class. After instantiation, the `SubmodelFlattener` is, for example, capable
of flattening a `Submodel` object into a `.csv` file, using the `submodel_to_csv()`-function. 

**Example Usage:**
```python
from basyx.aas.examples.data import example_submodel_template
from aas_flattening.submodel_flattening import SubmodelFlattener

example_submodel = example_submodel_template.create_example_submodel_template()

submodel_flattener = SubmodelFlattener(include_semantic_id=False, include_identification=False)
submodel_flattener.submodel_to_csv(example_submodel, "example.csv")
```
