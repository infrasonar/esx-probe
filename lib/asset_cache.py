import time
from pyVmomi import vim

K = tuple[str, str]
V = vim.ServiceInstance


class AssetCache:
    _all = {}

    @classmethod
    def get_value(cls, key: K) -> tuple[V | None, int | None]:
        if key in cls._all:
            val, expire_ts = cls._all[key]
            expired = expire_ts and expire_ts < time.time()
            return val, expired
        return None, None

    @classmethod
    def set_value(cls, key: K, val: V, max_age: int | None = None):
        expire_ts = time.time() + max_age if max_age else None
        cls._all[key] = (val, expire_ts)

    @classmethod
    def drop(cls, key: K):
        cls._all.pop(key, None)
