from typing import Any, Dict, Optional, Union

import jsonpath_rw

class JsonPath:
    def __init__(self, path: Union[str, jsonpath_rw]): ...
    path: jsonpath_rw.JSONPath

class ContextPath:
    def __init__(self, path: Optional[str] = "$$"): ...
    def __getattr__(self, item: str) -> ContextPath: ...
    _path: str

class Parameters:
    def __init__(self, **kwargs: Any): ...
    def to_dict(self) -> Dict[str, Any]: ...
    _map: Dict[str, Any]
