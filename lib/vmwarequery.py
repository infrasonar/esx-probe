import asyncio
import logging
from http.client import BadStatusLine
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, IgnoreResultException
from pyVmomi import vim  # type: ignore
from typing import List, Dict

from .vmwareconn import get_data


async def vmwarequery(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        obj_type: vim.ManagedEntity,
        properties: List[str]) -> list:
    address = check_config.get('address')
    if not address:
        address = asset.name
    assert asset_config, 'missing credentials'
    username = asset_config['username']
    password = asset_config['password']

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
    except IgnoreResultException:
        raise
    except BadStatusLine:
        msg = 'Vmware is shutting down'
        # TODO cls.tryDropVmwareConnection()
        raise CheckException(msg)
    except (vim.fault.InvalidLogin,
            vim.fault.NotAuthenticated,
            IOError,
            ConnectionError) as e:
        msg = str(e) or e.__class__.__name__
        if (
            'Cannot complete login due to an incorrect user name or'
            ' password'
        ) in msg:
            logging.warning('Cannot complete login due to an incorrect user'
                            ' name or password.')
            raise IgnoreResultException
        elif 'The session is not authenticated.' in msg:
            # drop the rest of the ugly message
            logging.warning('The session is not authenticated.')
            raise IgnoreResultException
        # TODO cls.tryDropVmwareConnection()
        raise CheckException(msg)
    except (vim.fault.HostConnectFault, Exception) as e:
        msg = str(e) or e.__class__.__name__
        if '503 Service Unavailable' in msg:
            msg = (
                '503 Service Unavailable'
                '\nSee: '
                'https://kb.vmware.com/clsservice/microsites/search.do?'
                'language=en_US&cmd=displayKC&externalId=2033822'
            )
        else:
            logging.warning(f'Unhandled check error {msg}')
        # TODO cls.tryDropVmwareConnection()
        raise CheckException(msg)
    else:
        return result
