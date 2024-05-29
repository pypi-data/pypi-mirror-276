from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Label(_message.Message):
    __slots__ = ["name", "value"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class MeterBucketValue(_message.Message):
    __slots__ = ["bucket", "count", "isNegativeInfinity"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ISNEGATIVEINFINITY_FIELD_NUMBER: _ClassVar[int]
    bucket: float
    count: int
    isNegativeInfinity: bool
    def __init__(self, bucket: _Optional[float] = ..., count: _Optional[int] = ..., isNegativeInfinity: bool = ...) -> None: ...

class MeterData(_message.Message):
    __slots__ = ["histogram", "service", "serviceInstance", "singleValue", "timestamp"]
    HISTOGRAM_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SINGLEVALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    histogram: MeterHistogram
    service: str
    serviceInstance: str
    singleValue: MeterSingleValue
    timestamp: int
    def __init__(self, singleValue: _Optional[_Union[MeterSingleValue, _Mapping]] = ..., histogram: _Optional[_Union[MeterHistogram, _Mapping]] = ..., service: _Optional[str] = ..., serviceInstance: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class MeterDataCollection(_message.Message):
    __slots__ = ["meterData"]
    METERDATA_FIELD_NUMBER: _ClassVar[int]
    meterData: _containers.RepeatedCompositeFieldContainer[MeterData]
    def __init__(self, meterData: _Optional[_Iterable[_Union[MeterData, _Mapping]]] = ...) -> None: ...

class MeterHistogram(_message.Message):
    __slots__ = ["labels", "name", "values"]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.RepeatedCompositeFieldContainer[Label]
    name: str
    values: _containers.RepeatedCompositeFieldContainer[MeterBucketValue]
    def __init__(self, name: _Optional[str] = ..., labels: _Optional[_Iterable[_Union[Label, _Mapping]]] = ..., values: _Optional[_Iterable[_Union[MeterBucketValue, _Mapping]]] = ...) -> None: ...

class MeterSingleValue(_message.Message):
    __slots__ = ["labels", "name", "value"]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.RepeatedCompositeFieldContainer[Label]
    name: str
    value: float
    def __init__(self, name: _Optional[str] = ..., labels: _Optional[_Iterable[_Union[Label, _Mapping]]] = ..., value: _Optional[float] = ...) -> None: ...
