from enum import Enum
from basyx.aas import model


class datatypes(Enum):
    int = int
    float = float
    str = str


def init_Property(df):
    id_short = df.id_short
    value_type = getattr(datatypes, df.value_type).value
    value = df.value
    value_id = df.value_id
    if value and value != "None":
        value = value_type(value)
        return model.Property(id_short=id_short, value_type=value_type, value=value, value_id=value_id)
    return model.Property(id_short=id_short, value_type=value_type, value_id=value_id)
