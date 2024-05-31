"""
Type annotations for bedrock-runtime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_runtime/type_defs/)

Usage::

    ```python
    from mypy_boto3_bedrock_runtime.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""

import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    ConversationRoleType,
    ImageFormatType,
    StopReasonType,
    ToolResultStatusType,
    TraceType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "BlobTypeDef",
    "ToolUseBlockDeltaTypeDef",
    "ToolUseBlockOutputTypeDef",
    "ToolUseBlockStartTypeDef",
    "ContentBlockStopEventTypeDef",
    "ToolUseBlockTypeDef",
    "ConverseMetricsTypeDef",
    "InferenceConfigurationTypeDef",
    "SystemContentBlockTypeDef",
    "ResponseMetadataTypeDef",
    "TokenUsageTypeDef",
    "ConverseStreamMetricsTypeDef",
    "InternalServerExceptionTypeDef",
    "MessageStartEventTypeDef",
    "MessageStopEventTypeDef",
    "ModelStreamErrorExceptionTypeDef",
    "ThrottlingExceptionTypeDef",
    "ValidationExceptionTypeDef",
    "ImageSourceOutputTypeDef",
    "ModelTimeoutExceptionTypeDef",
    "PayloadPartTypeDef",
    "SpecificToolChoiceTypeDef",
    "ToolInputSchemaTypeDef",
    "ImageSourceTypeDef",
    "InvokeModelRequestRequestTypeDef",
    "InvokeModelWithResponseStreamRequestRequestTypeDef",
    "ContentBlockDeltaTypeDef",
    "ContentBlockStartTypeDef",
    "InvokeModelResponseTypeDef",
    "ConverseStreamMetadataEventTypeDef",
    "ImageBlockOutputTypeDef",
    "ResponseStreamTypeDef",
    "ToolChoiceTypeDef",
    "ToolSpecificationTypeDef",
    "ImageBlockTypeDef",
    "ContentBlockDeltaEventTypeDef",
    "ContentBlockStartEventTypeDef",
    "ToolResultContentBlockOutputTypeDef",
    "InvokeModelWithResponseStreamResponseTypeDef",
    "ToolTypeDef",
    "ToolResultContentBlockTypeDef",
    "ConverseStreamOutputTypeDef",
    "ToolResultBlockOutputTypeDef",
    "ToolConfigurationTypeDef",
    "ToolResultBlockTypeDef",
    "ConverseStreamResponseTypeDef",
    "ContentBlockOutputTypeDef",
    "ContentBlockTypeDef",
    "MessageOutputTypeDef",
    "MessageTypeDef",
    "ConverseOutputTypeDef",
    "MessageUnionTypeDef",
    "ConverseResponseTypeDef",
    "ConverseRequestRequestTypeDef",
    "ConverseStreamRequestRequestTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ToolUseBlockDeltaTypeDef = TypedDict(
    "ToolUseBlockDeltaTypeDef",
    {
        "input": str,
    },
)
ToolUseBlockOutputTypeDef = TypedDict(
    "ToolUseBlockOutputTypeDef",
    {
        "toolUseId": str,
        "name": str,
        "input": Dict[str, Any],
    },
)
ToolUseBlockStartTypeDef = TypedDict(
    "ToolUseBlockStartTypeDef",
    {
        "toolUseId": str,
        "name": str,
    },
)
ContentBlockStopEventTypeDef = TypedDict(
    "ContentBlockStopEventTypeDef",
    {
        "contentBlockIndex": int,
    },
)
ToolUseBlockTypeDef = TypedDict(
    "ToolUseBlockTypeDef",
    {
        "toolUseId": str,
        "name": str,
        "input": Mapping[str, Any],
    },
)
ConverseMetricsTypeDef = TypedDict(
    "ConverseMetricsTypeDef",
    {
        "latencyMs": int,
    },
)
InferenceConfigurationTypeDef = TypedDict(
    "InferenceConfigurationTypeDef",
    {
        "maxTokens": NotRequired[int],
        "temperature": NotRequired[float],
        "topP": NotRequired[float],
        "stopSequences": NotRequired[Sequence[str]],
    },
)
SystemContentBlockTypeDef = TypedDict(
    "SystemContentBlockTypeDef",
    {
        "text": NotRequired[str],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
TokenUsageTypeDef = TypedDict(
    "TokenUsageTypeDef",
    {
        "inputTokens": int,
        "outputTokens": int,
        "totalTokens": int,
    },
)
ConverseStreamMetricsTypeDef = TypedDict(
    "ConverseStreamMetricsTypeDef",
    {
        "latencyMs": int,
    },
)
InternalServerExceptionTypeDef = TypedDict(
    "InternalServerExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
MessageStartEventTypeDef = TypedDict(
    "MessageStartEventTypeDef",
    {
        "role": ConversationRoleType,
    },
)
MessageStopEventTypeDef = TypedDict(
    "MessageStopEventTypeDef",
    {
        "stopReason": StopReasonType,
        "additionalModelResponseFields": NotRequired[Dict[str, Any]],
    },
)
ModelStreamErrorExceptionTypeDef = TypedDict(
    "ModelStreamErrorExceptionTypeDef",
    {
        "message": NotRequired[str],
        "originalStatusCode": NotRequired[int],
        "originalMessage": NotRequired[str],
    },
)
ThrottlingExceptionTypeDef = TypedDict(
    "ThrottlingExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ValidationExceptionTypeDef = TypedDict(
    "ValidationExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ImageSourceOutputTypeDef = TypedDict(
    "ImageSourceOutputTypeDef",
    {
        "bytes": NotRequired[bytes],
    },
)
ModelTimeoutExceptionTypeDef = TypedDict(
    "ModelTimeoutExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
PayloadPartTypeDef = TypedDict(
    "PayloadPartTypeDef",
    {
        "bytes": NotRequired[bytes],
    },
)
SpecificToolChoiceTypeDef = TypedDict(
    "SpecificToolChoiceTypeDef",
    {
        "name": str,
    },
)
ToolInputSchemaTypeDef = TypedDict(
    "ToolInputSchemaTypeDef",
    {
        "json": NotRequired[Mapping[str, Any]],
    },
)
ImageSourceTypeDef = TypedDict(
    "ImageSourceTypeDef",
    {
        "bytes": NotRequired[BlobTypeDef],
    },
)
InvokeModelRequestRequestTypeDef = TypedDict(
    "InvokeModelRequestRequestTypeDef",
    {
        "body": BlobTypeDef,
        "modelId": str,
        "contentType": NotRequired[str],
        "accept": NotRequired[str],
        "trace": NotRequired[TraceType],
        "guardrailIdentifier": NotRequired[str],
        "guardrailVersion": NotRequired[str],
    },
)
InvokeModelWithResponseStreamRequestRequestTypeDef = TypedDict(
    "InvokeModelWithResponseStreamRequestRequestTypeDef",
    {
        "body": BlobTypeDef,
        "modelId": str,
        "contentType": NotRequired[str],
        "accept": NotRequired[str],
        "trace": NotRequired[TraceType],
        "guardrailIdentifier": NotRequired[str],
        "guardrailVersion": NotRequired[str],
    },
)
ContentBlockDeltaTypeDef = TypedDict(
    "ContentBlockDeltaTypeDef",
    {
        "text": NotRequired[str],
        "toolUse": NotRequired[ToolUseBlockDeltaTypeDef],
    },
)
ContentBlockStartTypeDef = TypedDict(
    "ContentBlockStartTypeDef",
    {
        "toolUse": NotRequired[ToolUseBlockStartTypeDef],
    },
)
InvokeModelResponseTypeDef = TypedDict(
    "InvokeModelResponseTypeDef",
    {
        "body": StreamingBody,
        "contentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ConverseStreamMetadataEventTypeDef = TypedDict(
    "ConverseStreamMetadataEventTypeDef",
    {
        "usage": TokenUsageTypeDef,
        "metrics": ConverseStreamMetricsTypeDef,
    },
)
ImageBlockOutputTypeDef = TypedDict(
    "ImageBlockOutputTypeDef",
    {
        "format": ImageFormatType,
        "source": ImageSourceOutputTypeDef,
    },
)
ResponseStreamTypeDef = TypedDict(
    "ResponseStreamTypeDef",
    {
        "chunk": NotRequired[PayloadPartTypeDef],
        "internalServerException": NotRequired[InternalServerExceptionTypeDef],
        "modelStreamErrorException": NotRequired[ModelStreamErrorExceptionTypeDef],
        "validationException": NotRequired[ValidationExceptionTypeDef],
        "throttlingException": NotRequired[ThrottlingExceptionTypeDef],
        "modelTimeoutException": NotRequired[ModelTimeoutExceptionTypeDef],
    },
)
ToolChoiceTypeDef = TypedDict(
    "ToolChoiceTypeDef",
    {
        "auto": NotRequired[Mapping[str, Any]],
        "any": NotRequired[Mapping[str, Any]],
        "tool": NotRequired[SpecificToolChoiceTypeDef],
    },
)
ToolSpecificationTypeDef = TypedDict(
    "ToolSpecificationTypeDef",
    {
        "name": str,
        "inputSchema": ToolInputSchemaTypeDef,
        "description": NotRequired[str],
    },
)
ImageBlockTypeDef = TypedDict(
    "ImageBlockTypeDef",
    {
        "format": ImageFormatType,
        "source": ImageSourceTypeDef,
    },
)
ContentBlockDeltaEventTypeDef = TypedDict(
    "ContentBlockDeltaEventTypeDef",
    {
        "delta": ContentBlockDeltaTypeDef,
        "contentBlockIndex": int,
    },
)
ContentBlockStartEventTypeDef = TypedDict(
    "ContentBlockStartEventTypeDef",
    {
        "start": ContentBlockStartTypeDef,
        "contentBlockIndex": int,
    },
)
ToolResultContentBlockOutputTypeDef = TypedDict(
    "ToolResultContentBlockOutputTypeDef",
    {
        "json": NotRequired[Dict[str, Any]],
        "text": NotRequired[str],
        "image": NotRequired[ImageBlockOutputTypeDef],
    },
)
InvokeModelWithResponseStreamResponseTypeDef = TypedDict(
    "InvokeModelWithResponseStreamResponseTypeDef",
    {
        "body": "EventStream[ResponseStreamTypeDef]",
        "contentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ToolTypeDef = TypedDict(
    "ToolTypeDef",
    {
        "toolSpec": NotRequired[ToolSpecificationTypeDef],
    },
)
ToolResultContentBlockTypeDef = TypedDict(
    "ToolResultContentBlockTypeDef",
    {
        "json": NotRequired[Mapping[str, Any]],
        "text": NotRequired[str],
        "image": NotRequired[ImageBlockTypeDef],
    },
)
ConverseStreamOutputTypeDef = TypedDict(
    "ConverseStreamOutputTypeDef",
    {
        "messageStart": NotRequired[MessageStartEventTypeDef],
        "contentBlockStart": NotRequired[ContentBlockStartEventTypeDef],
        "contentBlockDelta": NotRequired[ContentBlockDeltaEventTypeDef],
        "contentBlockStop": NotRequired[ContentBlockStopEventTypeDef],
        "messageStop": NotRequired[MessageStopEventTypeDef],
        "metadata": NotRequired[ConverseStreamMetadataEventTypeDef],
        "internalServerException": NotRequired[InternalServerExceptionTypeDef],
        "modelStreamErrorException": NotRequired[ModelStreamErrorExceptionTypeDef],
        "validationException": NotRequired[ValidationExceptionTypeDef],
        "throttlingException": NotRequired[ThrottlingExceptionTypeDef],
    },
)
ToolResultBlockOutputTypeDef = TypedDict(
    "ToolResultBlockOutputTypeDef",
    {
        "toolUseId": str,
        "content": List[ToolResultContentBlockOutputTypeDef],
        "status": NotRequired[ToolResultStatusType],
    },
)
ToolConfigurationTypeDef = TypedDict(
    "ToolConfigurationTypeDef",
    {
        "tools": Sequence[ToolTypeDef],
        "toolChoice": NotRequired[ToolChoiceTypeDef],
    },
)
ToolResultBlockTypeDef = TypedDict(
    "ToolResultBlockTypeDef",
    {
        "toolUseId": str,
        "content": Sequence[ToolResultContentBlockTypeDef],
        "status": NotRequired[ToolResultStatusType],
    },
)
ConverseStreamResponseTypeDef = TypedDict(
    "ConverseStreamResponseTypeDef",
    {
        "stream": "EventStream[ConverseStreamOutputTypeDef]",
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ContentBlockOutputTypeDef = TypedDict(
    "ContentBlockOutputTypeDef",
    {
        "text": NotRequired[str],
        "image": NotRequired[ImageBlockOutputTypeDef],
        "toolUse": NotRequired[ToolUseBlockOutputTypeDef],
        "toolResult": NotRequired[ToolResultBlockOutputTypeDef],
    },
)
ContentBlockTypeDef = TypedDict(
    "ContentBlockTypeDef",
    {
        "text": NotRequired[str],
        "image": NotRequired[ImageBlockTypeDef],
        "toolUse": NotRequired[ToolUseBlockTypeDef],
        "toolResult": NotRequired[ToolResultBlockTypeDef],
    },
)
MessageOutputTypeDef = TypedDict(
    "MessageOutputTypeDef",
    {
        "role": ConversationRoleType,
        "content": List[ContentBlockOutputTypeDef],
    },
)
MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "role": ConversationRoleType,
        "content": Sequence[ContentBlockTypeDef],
    },
)
ConverseOutputTypeDef = TypedDict(
    "ConverseOutputTypeDef",
    {
        "message": NotRequired[MessageOutputTypeDef],
    },
)
MessageUnionTypeDef = Union[MessageTypeDef, MessageOutputTypeDef]
ConverseResponseTypeDef = TypedDict(
    "ConverseResponseTypeDef",
    {
        "output": ConverseOutputTypeDef,
        "stopReason": StopReasonType,
        "usage": TokenUsageTypeDef,
        "metrics": ConverseMetricsTypeDef,
        "additionalModelResponseFields": Dict[str, Any],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ConverseRequestRequestTypeDef = TypedDict(
    "ConverseRequestRequestTypeDef",
    {
        "modelId": str,
        "messages": Sequence[MessageUnionTypeDef],
        "system": NotRequired[Sequence[SystemContentBlockTypeDef]],
        "inferenceConfig": NotRequired[InferenceConfigurationTypeDef],
        "toolConfig": NotRequired[ToolConfigurationTypeDef],
        "additionalModelRequestFields": NotRequired[Mapping[str, Any]],
        "additionalModelResponseFieldPaths": NotRequired[Sequence[str]],
    },
)
ConverseStreamRequestRequestTypeDef = TypedDict(
    "ConverseStreamRequestRequestTypeDef",
    {
        "modelId": str,
        "messages": Sequence[MessageUnionTypeDef],
        "system": NotRequired[Sequence[SystemContentBlockTypeDef]],
        "inferenceConfig": NotRequired[InferenceConfigurationTypeDef],
        "toolConfig": NotRequired[ToolConfigurationTypeDef],
        "additionalModelRequestFields": NotRequired[Mapping[str, Any]],
        "additionalModelResponseFieldPaths": NotRequired[Sequence[str]],
    },
)
