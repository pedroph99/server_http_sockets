from pydantic import BaseModel
from enum import Enum
class serverTypes(Enum):
    """
    Especifica os tipos de servidoes possíveis para o servidor.
    Dual: Servidor IPv4 e IPv6
    IPv4: Servidor IPv4
    IPv6: Servidor IPv6
    """
    DUAL = 'dual'
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
