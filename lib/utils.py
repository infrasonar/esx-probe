import calendar
import datetime
from pyVmomi.VmomiSupport import short as vmoni_short
from pyVmomi.VmomiSupport import long as vmoni_long


BASE_TYPES = (
    str,
    int,
    vmoni_long,
    vmoni_short,
    float,
    bool)


def datetime_to_timestamp(inp):
    if inp is None:
        return inp
    return calendar.timegm(inp.timetuple())


def prop_val_to_dict(prop_val, item_name=None):
    dct = {}
    for name, info in prop_val._propInfo.items():
        print(name, info)
        if info.type in BASE_TYPES:
            dct[name] = getattr(prop_val, name)
        elif info.type == datetime.datetime:
            dct[name] = datetime_to_timestamp(getattr(prop_val, name))
        elif hasattr(info.type, 'values'):
            # values (lookup) is always empty
            dct[name] = getattr(prop_val, name)

    if item_name:
        dct['name'] = item_name
    return dct
