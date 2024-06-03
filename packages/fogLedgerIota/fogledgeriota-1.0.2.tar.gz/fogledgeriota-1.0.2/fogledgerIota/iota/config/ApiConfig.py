from .NodeConfig import (NodeConfig)
from typing import Dict
from fogbed import (
   VirtualInstance
)
class ApiConfig(NodeConfig):
    def __init__(self, name: str = None, port_bindings: Dict[str, str] = None,  ip:str=None):
        super().__init__(name, port_bindings, ip)