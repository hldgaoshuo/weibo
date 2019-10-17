import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()


class GEncoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {
                self.prefix: o.name,
            }
        else:
            return super().default(self, o)


def g_decode(d):
    if GEncoder.prefix in d:
        name = d[GEncoder.prefix]
        return UserRole[name]
    else:
        return d
