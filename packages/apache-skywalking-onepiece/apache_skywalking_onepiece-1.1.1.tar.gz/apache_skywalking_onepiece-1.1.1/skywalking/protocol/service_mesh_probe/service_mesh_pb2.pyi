from common import Common_pb2 as _Common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
HTTP: Protocol
gRPC: Protocol

class HTTPServiceMeshMetric(_message.Message):
    __slots__ = ["destInstanceProperties", "destServiceInstance", "destServiceName", "detectPoint", "endTime", "endpoint", "internalErrorCode", "internalRequestLatencyNanos", "internalResponseLatencyNanos", "latency", "protocol", "responseCode", "sourceInstanceProperties", "sourceServiceInstance", "sourceServiceName", "startTime", "status", "tlsMode"]
    DESTINSTANCEPROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DESTSERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    DESTSERVICENAME_FIELD_NUMBER: _ClassVar[int]
    DETECTPOINT_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    INTERNALERRORCODE_FIELD_NUMBER: _ClassVar[int]
    INTERNALREQUESTLATENCYNANOS_FIELD_NUMBER: _ClassVar[int]
    INTERNALRESPONSELATENCYNANOS_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    RESPONSECODE_FIELD_NUMBER: _ClassVar[int]
    SOURCEINSTANCEPROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SOURCESERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    SOURCESERVICENAME_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TLSMODE_FIELD_NUMBER: _ClassVar[int]
    destInstanceProperties: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    destServiceInstance: str
    destServiceName: str
    detectPoint: _Common_pb2.DetectPoint
    endTime: int
    endpoint: str
    internalErrorCode: str
    internalRequestLatencyNanos: int
    internalResponseLatencyNanos: int
    latency: int
    protocol: Protocol
    responseCode: int
    sourceInstanceProperties: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    sourceServiceInstance: str
    sourceServiceName: str
    startTime: int
    status: bool
    tlsMode: str
    def __init__(self, startTime: _Optional[int] = ..., endTime: _Optional[int] = ..., sourceServiceName: _Optional[str] = ..., sourceServiceInstance: _Optional[str] = ..., destServiceName: _Optional[str] = ..., destServiceInstance: _Optional[str] = ..., endpoint: _Optional[str] = ..., latency: _Optional[int] = ..., responseCode: _Optional[int] = ..., status: bool = ..., protocol: _Optional[_Union[Protocol, str]] = ..., detectPoint: _Optional[_Union[_Common_pb2.DetectPoint, str]] = ..., tlsMode: _Optional[str] = ..., internalErrorCode: _Optional[str] = ..., internalRequestLatencyNanos: _Optional[int] = ..., internalResponseLatencyNanos: _Optional[int] = ..., sourceInstanceProperties: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ..., destInstanceProperties: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ...) -> None: ...

class HTTPServiceMeshMetrics(_message.Message):
    __slots__ = ["metrics"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[HTTPServiceMeshMetric]
    def __init__(self, metrics: _Optional[_Iterable[_Union[HTTPServiceMeshMetric, _Mapping]]] = ...) -> None: ...

class MeshProbeDownstream(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ServiceMeshMetrics(_message.Message):
    __slots__ = ["httpMetrics", "tcpMetrics"]
    HTTPMETRICS_FIELD_NUMBER: _ClassVar[int]
    TCPMETRICS_FIELD_NUMBER: _ClassVar[int]
    httpMetrics: HTTPServiceMeshMetrics
    tcpMetrics: TCPServiceMeshMetrics
    def __init__(self, httpMetrics: _Optional[_Union[HTTPServiceMeshMetrics, _Mapping]] = ..., tcpMetrics: _Optional[_Union[TCPServiceMeshMetrics, _Mapping]] = ...) -> None: ...

class TCPServiceMeshMetric(_message.Message):
    __slots__ = ["destInstanceProperties", "destServiceInstance", "destServiceName", "detectPoint", "endTime", "internalErrorCode", "internalRequestLatencyNanos", "internalResponseLatencyNanos", "receivedBytes", "sentBytes", "sourceInstanceProperties", "sourceServiceInstance", "sourceServiceName", "startTime", "tlsMode"]
    DESTINSTANCEPROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DESTSERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    DESTSERVICENAME_FIELD_NUMBER: _ClassVar[int]
    DETECTPOINT_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    INTERNALERRORCODE_FIELD_NUMBER: _ClassVar[int]
    INTERNALREQUESTLATENCYNANOS_FIELD_NUMBER: _ClassVar[int]
    INTERNALRESPONSELATENCYNANOS_FIELD_NUMBER: _ClassVar[int]
    RECEIVEDBYTES_FIELD_NUMBER: _ClassVar[int]
    SENTBYTES_FIELD_NUMBER: _ClassVar[int]
    SOURCEINSTANCEPROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SOURCESERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    SOURCESERVICENAME_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    TLSMODE_FIELD_NUMBER: _ClassVar[int]
    destInstanceProperties: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    destServiceInstance: str
    destServiceName: str
    detectPoint: _Common_pb2.DetectPoint
    endTime: int
    internalErrorCode: str
    internalRequestLatencyNanos: int
    internalResponseLatencyNanos: int
    receivedBytes: int
    sentBytes: int
    sourceInstanceProperties: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    sourceServiceInstance: str
    sourceServiceName: str
    startTime: int
    tlsMode: str
    def __init__(self, startTime: _Optional[int] = ..., endTime: _Optional[int] = ..., sourceServiceName: _Optional[str] = ..., sourceServiceInstance: _Optional[str] = ..., destServiceName: _Optional[str] = ..., destServiceInstance: _Optional[str] = ..., detectPoint: _Optional[_Union[_Common_pb2.DetectPoint, str]] = ..., tlsMode: _Optional[str] = ..., internalErrorCode: _Optional[str] = ..., internalRequestLatencyNanos: _Optional[int] = ..., internalResponseLatencyNanos: _Optional[int] = ..., sourceInstanceProperties: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ..., destInstanceProperties: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ..., receivedBytes: _Optional[int] = ..., sentBytes: _Optional[int] = ...) -> None: ...

class TCPServiceMeshMetrics(_message.Message):
    __slots__ = ["metrics"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[TCPServiceMeshMetric]
    def __init__(self, metrics: _Optional[_Iterable[_Union[TCPServiceMeshMetric, _Mapping]]] = ...) -> None: ...

class Protocol(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
