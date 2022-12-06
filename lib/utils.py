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


ALLOWED_FQDN_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-.'


def hostname_to_valid_fqdn(host_name):
    fqdn = ''
    for cr in host_name.lower():
        if cr in ALLOWED_FQDN_CHARS:
            fqdn += cr
        elif cr == '_':
            fqdn += '-'

    return fqdn


def datetime_to_timestamp(inp):
    if inp is None:
        return inp
    return calendar.timegm(inp.timetuple())


def dyn_property_list_to_kv_list(lst):
    lst_out = []
    for feature in lst:
        lst_out.append({
            'name': feature.key,
            'value': feature.value
        })
    return lst_out


def dyn_property_list_to_dict(lst, item_name=None):
    dct = {}
    for item in lst:
        dct[item.identifierType.key] = item.identifierValue
    if item_name:
        dct['name'] = item_name
    return dct


def prop_val_to_value_list(prop_val, value_name='value'):
    lst = []
    for name, info in prop_val._propInfo.items():
        if info.type in BASE_TYPES:
            lst.append({'name': name, value_name: getattr(prop_val, name)})
        elif info.type == datetime.datetime:
            lst.append({'name': name, value_name:
                        datetime_to_timestamp(getattr(prop_val, name))})
        elif hasattr(info.type, 'values'):
            # values (lookup) is always empty
            lst.append({'name': name, value_name: getattr(prop_val, name)})
    return lst


def prop_val_to_dict(prop_val, item_name=None):
    dct = {}
    for name, info in prop_val._propInfo.items():
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
