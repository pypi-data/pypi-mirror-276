from common import Common_pb2 as _Common_pb2
from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

Cache: SpanLayer
CrossProcess: RefType
CrossThread: RefType
DESCRIPTOR: _descriptor.FileDescriptor
Database: SpanLayer
Entry: SpanType
Exit: SpanType
FAAS: SpanLayer
Http: SpanLayer
Local: SpanType
MQ: SpanLayer
RPCFramework: SpanLayer
Unknown: SpanLayer

class ID(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[_Iterable[str]] = ...) -> None: ...

class Log(_message.Message):
    __slots__ = ["data", "time"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    time: int
    def __init__(self, time: _Optional[int] = ..., data: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ...) -> None: ...

class SegmentCollection(_message.Message):
    __slots__ = ["segments"]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[SegmentObject]
    def __init__(self, segments: _Optional[_Iterable[_Union[SegmentObject, _Mapping]]] = ...) -> None: ...

class SegmentObject(_message.Message):
    __slots__ = ["isSizeLimited", "service", "serviceInstance", "spans", "traceId", "traceSegmentId"]
    ISSIZELIMITED_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SPANS_FIELD_NUMBER: _ClassVar[int]
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    TRACESEGMENTID_FIELD_NUMBER: _ClassVar[int]
    isSizeLimited: bool
    service: str
    serviceInstance: str
    spans: _containers.RepeatedCompositeFieldContainer[SpanObject]
    traceId: str
    traceSegmentId: str
    def __init__(self, traceId: _Optional[str] = ..., traceSegmentId: _Optional[str] = ..., spans: _Optional[_Iterable[_Union[SpanObject, _Mapping]]] = ..., service: _Optional[str] = ..., serviceInstance: _Optional[str] = ..., isSizeLimited: bool = ...) -> None: ...

class SegmentReference(_message.Message):
    __slots__ = ["networkAddressUsedAtPeer", "parentEndpoint", "parentService", "parentServiceInstance", "parentSpanId", "parentTraceSegmentId", "refType", "traceId"]
    NETWORKADDRESSUSEDATPEER_FIELD_NUMBER: _ClassVar[int]
    PARENTENDPOINT_FIELD_NUMBER: _ClassVar[int]
    PARENTSERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    PARENTSERVICE_FIELD_NUMBER: _ClassVar[int]
    PARENTSPANID_FIELD_NUMBER: _ClassVar[int]
    PARENTTRACESEGMENTID_FIELD_NUMBER: _ClassVar[int]
    REFTYPE_FIELD_NUMBER: _ClassVar[int]
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    networkAddressUsedAtPeer: str
    parentEndpoint: str
    parentService: str
    parentServiceInstance: str
    parentSpanId: int
    parentTraceSegmentId: str
    refType: RefType
    traceId: str
    def __init__(self, refType: _Optional[_Union[RefType, str]] = ..., traceId: _Optional[str] = ..., parentTraceSegmentId: _Optional[str] = ..., parentSpanId: _Optional[int] = ..., parentService: _Optional[str] = ..., parentServiceInstance: _Optional[str] = ..., parentEndpoint: _Optional[str] = ..., networkAddressUsedAtPeer: _Optional[str] = ...) -> None: ...

class SpanAttachedEvent(_message.Message):
    __slots__ = ["endTime", "event", "startTime", "summary", "tags", "traceContext"]
    class SpanReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class SpanReference(_message.Message):
        __slots__ = ["spanId", "traceId", "traceSegmentId", "type"]
        SPANID_FIELD_NUMBER: _ClassVar[int]
        TRACEID_FIELD_NUMBER: _ClassVar[int]
        TRACESEGMENTID_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        spanId: str
        traceId: str
        traceSegmentId: str
        type: SpanAttachedEvent.SpanReferenceType
        def __init__(self, type: _Optional[_Union[SpanAttachedEvent.SpanReferenceType, str]] = ..., traceId: _Optional[str] = ..., traceSegmentId: _Optional[str] = ..., spanId: _Optional[str] = ...) -> None: ...
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    SKYWALKING: SpanAttachedEvent.SpanReferenceType
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TRACECONTEXT_FIELD_NUMBER: _ClassVar[int]
    ZIPKIN: SpanAttachedEvent.SpanReferenceType
    endTime: _Common_pb2.Instant
    event: str
    startTime: _Common_pb2.Instant
    summary: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyIntValuePair]
    tags: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    traceContext: SpanAttachedEvent.SpanReference
    def __init__(self, startTime: _Optional[_Union[_Common_pb2.Instant, _Mapping]] = ..., event: _Optional[str] = ..., endTime: _Optional[_Union[_Common_pb2.Instant, _Mapping]] = ..., tags: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ..., summary: _Optional[_Iterable[_Union[_Common_pb2.KeyIntValuePair, _Mapping]]] = ..., traceContext: _Optional[_Union[SpanAttachedEvent.SpanReference, _Mapping]] = ...) -> None: ...

class SpanObject(_message.Message):
    __slots__ = ["componentId", "endTime", "isError", "logs", "operationName", "parentSpanId", "peer", "refs", "skipAnalysis", "spanId", "spanLayer", "spanType", "startTime", "tags"]
    COMPONENTID_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    ISERROR_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    OPERATIONNAME_FIELD_NUMBER: _ClassVar[int]
    PARENTSPANID_FIELD_NUMBER: _ClassVar[int]
    PEER_FIELD_NUMBER: _ClassVar[int]
    REFS_FIELD_NUMBER: _ClassVar[int]
    SKIPANALYSIS_FIELD_NUMBER: _ClassVar[int]
    SPANID_FIELD_NUMBER: _ClassVar[int]
    SPANLAYER_FIELD_NUMBER: _ClassVar[int]
    SPANTYPE_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    componentId: int
    endTime: int
    isError: bool
    logs: _containers.RepeatedCompositeFieldContainer[Log]
    operationName: str
    parentSpanId: int
    peer: str
    refs: _containers.RepeatedCompositeFieldContainer[SegmentReference]
    skipAnalysis: bool
    spanId: int
    spanLayer: SpanLayer
    spanType: SpanType
    startTime: int
    tags: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    def __init__(self, spanId: _Optional[int] = ..., parentSpanId: _Optional[int] = ..., startTime: _Optional[int] = ..., endTime: _Optional[int] = ..., refs: _Optional[_Iterable[_Union[SegmentReference, _Mapping]]] = ..., operationName: _Optional[str] = ..., peer: _Optional[str] = ..., spanType: _Optional[_Union[SpanType, str]] = ..., spanLayer: _Optional[_Union[SpanLayer, str]] = ..., componentId: _Optional[int] = ..., isError: bool = ..., tags: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ..., logs: _Optional[_Iterable[_Union[Log, _Mapping]]] = ..., skipAnalysis: bool = ...) -> None: ...

class SpanType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class RefType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SpanLayer(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
