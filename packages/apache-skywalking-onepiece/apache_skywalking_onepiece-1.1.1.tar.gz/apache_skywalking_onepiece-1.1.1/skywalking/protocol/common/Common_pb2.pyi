from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor
client: DetectPoint
proxy: DetectPoint
server: DetectPoint

class CPU(_message.Message):
    __slots__ = ["usagePercent"]
    USAGEPERCENT_FIELD_NUMBER: _ClassVar[int]
    usagePercent: float
    def __init__(self, usagePercent: _Optional[float] = ...) -> None: ...

class Instant(_message.Message):
    __slots__ = ["nanos", "seconds"]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    nanos: int
    seconds: int
    def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...

class KeyIntValuePair(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: int
    def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...

class KeyStringValuePair(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class DetectPoint(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
