from google.protobuf import timestamp_pb2 as _timestamp_pb2
from unionai.internal.secret import definition_pb2 as _definition_pb2
from unionai.internal.validate.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSecretRequest(_message.Message):
    __slots__ = ["id", "secret_spec"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_SPEC_FIELD_NUMBER: _ClassVar[int]
    id: _definition_pb2.SecretIdentifier
    secret_spec: _definition_pb2.SecretSpec
    def __init__(self, id: _Optional[_Union[_definition_pb2.SecretIdentifier, _Mapping]] = ..., secret_spec: _Optional[_Union[_definition_pb2.SecretSpec, _Mapping]] = ...) -> None: ...

class CreateSecretResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateSecretRequest(_message.Message):
    __slots__ = ["id", "secret_spec"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_SPEC_FIELD_NUMBER: _ClassVar[int]
    id: _definition_pb2.SecretIdentifier
    secret_spec: _definition_pb2.SecretSpec
    def __init__(self, id: _Optional[_Union[_definition_pb2.SecretIdentifier, _Mapping]] = ..., secret_spec: _Optional[_Union[_definition_pb2.SecretSpec, _Mapping]] = ...) -> None: ...

class UpdateSecretResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSecretRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _definition_pb2.SecretIdentifier
    def __init__(self, id: _Optional[_Union[_definition_pb2.SecretIdentifier, _Mapping]] = ...) -> None: ...

class GetSecretResponse(_message.Message):
    __slots__ = ["secret"]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: _definition_pb2.Secret
    def __init__(self, secret: _Optional[_Union[_definition_pb2.Secret, _Mapping]] = ...) -> None: ...

class DeleteSecretRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _definition_pb2.SecretIdentifier
    def __init__(self, id: _Optional[_Union[_definition_pb2.SecretIdentifier, _Mapping]] = ...) -> None: ...

class DeleteSecretResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListSecretsRequest(_message.Message):
    __slots__ = ["organization", "domain", "project", "limit", "token"]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    organization: str
    domain: str
    project: str
    limit: int
    token: str
    def __init__(self, organization: _Optional[str] = ..., domain: _Optional[str] = ..., project: _Optional[str] = ..., limit: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class ListSecretsResponse(_message.Message):
    __slots__ = ["secrets", "token"]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    secrets: _containers.RepeatedCompositeFieldContainer[_definition_pb2.Secret]
    token: str
    def __init__(self, secrets: _Optional[_Iterable[_Union[_definition_pb2.Secret, _Mapping]]] = ..., token: _Optional[str] = ...) -> None: ...
