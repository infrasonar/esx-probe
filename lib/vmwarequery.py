import asyncio
import logging
from http.client import BadStatusLine
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, IgnoreCheckException, \
    IgnoreResultException
from pyVmomi import vim  # type: ignore
from typing import List

from .vmwareconn import get_alarms, get_data, drop_connnection


async def vmwarequery_alarms(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> list:
    address = check_config.get('address')
    if not address:
        address = asset.name
    username = asset_config.get('username')
    password = asset_config.get('password')
    if None in (username, password):
        logging.error(f'missing credentails for {asset}')
        raise IgnoreResultException

    try:
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            get_alarms,
            address,
            username,
            password,
        )
    except (vim.fault.InvalidLogin,
            vim.fault.NotAuthenticated):
        raise IgnoreResultException
    except vim.fault.HostConnectFault:
        msg = 'Failed to connect.'
        raise CheckException(msg)
    except (IOError,
            BadStatusLine,
            ConnectionError) as e:
        msg = str(e) or e.__class__.__name__
        drop_connnection(address)
        raise CheckException(msg)
    except Exception as e:
        msg = str(e) or e.__class__.__name__
        logging.exception(msg)
        raise CheckException(msg)
    else:
        return result


async def vmwarequery(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        obj_type: vim.ManagedEntity,
        properties: List[str]) -> list:
    address = check_config.get('address')
    if not address:
        address = asset.name
    username = asset_config.get('username')
    password = asset_config.get('password')
    if None in (username, password):
        logging.error(f'missing credentails for {asset}')
        raise IgnoreResultException

    try:
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            get_data,
            address,
            username,
            password,
            obj_type,
            properties,
        )
    except (CheckException,
            IgnoreCheckException,
            IgnoreResultException):
        raise
    except (vim.fault.InvalidLogin,
            vim.fault.NotAuthenticated):
        raise IgnoreResultException
    except vim.fault.HostConnectFault:
        msg = 'Failed to connect.'
        raise CheckException(msg)
    except (IOError,
            BadStatusLine,
            ConnectionError) as e:
        msg = str(e) or e.__class__.__name__
        drop_connnection(address)
        raise CheckException(msg)
    except Exception as e:
        msg = str(e) or e.__class__.__name__
        logging.exception(msg)
        raise CheckException(msg)
    else:
        return result
