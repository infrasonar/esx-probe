import asyncio
import logging
from http.client import BadStatusLine
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from pyVmomi import vim  # type: ignore
from typing import List

from .vmwareconn import get_content, get_data, drop_connnection

DEFAULT_INTERVAL = 300


async def vmwarequery_content(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> list:
    address = check_config.get('address')
    if not address:
        address = asset.name
    username = asset_config.get('username')
    password = asset_config.get('password')
    if None in (username, password):
        msg = 'missing credentials'
        raise CheckException(msg)

    try:
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            get_content,
            address,
            username,
            password,
        )
    except CheckException:
        raise
    except (vim.fault.InvalidLogin,
            vim.fault.NotAuthenticated):
        msg = 'invalid login or not authenticated'
        raise CheckException(msg)
    except vim.fault.HostConnectFault:
        msg = 'failed to connect.'
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
        msg = 'missing credentials'
        raise CheckException(msg)

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
    except CheckException:
        raise
    except (vim.fault.InvalidLogin,
            vim.fault.NotAuthenticated):
        msg = 'invalid login or not authenticated'
        raise CheckException(msg)
    except vim.fault.HostConnectFault:
        msg = 'failed to connect.'
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
