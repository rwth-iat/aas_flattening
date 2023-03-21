from config_based_aas_flattening.objtocsv import obj2csv
from config_based_aas_flattening.csvtoobj import csvtoobj
from basyx.aas.examples.data import example_submodel_template
import toml
import os

try:
    # serializing submodel to csv
    example_submodel = example_submodel_template.create_example_submodel_template()
    config_obj_2_csv = toml.load("../objtocsv/config.toml")
    flattened_submodel, headers = obj2csv.get_flatten_from_object(example_submodel, config_obj_2_csv)
    obj2csv.write_to_csv(headers, [flattened_submodel], "test_file.csv")

    # deserializing csv to object
    config_csv_2_obj = toml.load("../csvtoobj/csvtoobj.toml")
    csvtoobj.get_obj_from_csv("test_file.csv", config_csv_2_obj)

finally:
    if os.path.exists("test_file.csv"):
        os.remove("test_file.csv")
