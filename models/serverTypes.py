from pydantic import BaseModel
from enum import Enum
class serverTypes(Enum):
    DUAL = 'dual'
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
