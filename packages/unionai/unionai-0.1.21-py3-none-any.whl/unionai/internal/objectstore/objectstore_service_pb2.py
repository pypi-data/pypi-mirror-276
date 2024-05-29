# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: objectstore/objectstore_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from unionai.internal.objectstore import payload_pb2 as objectstore_dot_payload__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%objectstore/objectstore_service.proto\x12\x17\x63loudidl.objectstore.v1\x1a\x19objectstore/payload.proto2\x9f\n\n\x12ObjectStoreService\x12\x61\n\x08Metadata\x12(.cloudidl.objectstore.v1.MetadataRequest\x1a).cloudidl.objectstore.v1.MetadataResponse\"\x00\x12U\n\x04Head\x12$.cloudidl.objectstore.v1.HeadRequest\x1a%.cloudidl.objectstore.v1.HeadResponse\"\x00\x12R\n\x03Put\x12#.cloudidl.objectstore.v1.PutRequest\x1a$.cloudidl.objectstore.v1.PutResponse\"\x00\x12R\n\x03Get\x12#.cloudidl.objectstore.v1.GetRequest\x1a$.cloudidl.objectstore.v1.GetResponse\"\x00\x12[\n\x06\x44\x65lete\x12&.cloudidl.objectstore.v1.DeleteRequest\x1a\'.cloudidl.objectstore.v1.DeleteResponse\"\x00\x12U\n\x04List\x12$.cloudidl.objectstore.v1.ListRequest\x1a%.cloudidl.objectstore.v1.ListResponse\"\x00\x12U\n\x04\x43opy\x12$.cloudidl.objectstore.v1.CopyRequest\x1a%.cloudidl.objectstore.v1.CopyResponse\"\x00\x12\x85\x01\n\x14StartMultipartUpload\x12\x34.cloudidl.objectstore.v1.StartMultipartUploadRequest\x1a\x35.cloudidl.objectstore.v1.StartMultipartUploadResponse\"\x00\x12i\n\nUploadPart\x12*.cloudidl.objectstore.v1.UploadPartRequest\x1a+.cloudidl.objectstore.v1.UploadPartResponse\"\x00(\x01\x12\xa3\x01\n\x1eListInProgressMultipartUploads\x12>.cloudidl.objectstore.v1.ListInProgressMultipartUploadsRequest\x1a?.cloudidl.objectstore.v1.ListInProgressMultipartUploadsResponse\"\x00\x12\x91\x01\n\x18TerminateMultipartUpload\x12\x38.cloudidl.objectstore.v1.TerminateMultipartUploadRequest\x1a\x39.cloudidl.objectstore.v1.TerminateMultipartUploadResponse\"\x00\x12o\n\x0c\x44ownloadPart\x12,.cloudidl.objectstore.v1.DownloadPartRequest\x1a-.cloudidl.objectstore.v1.DownloadPartResponse\"\x00\x30\x01\x42\xe6\x01\n\x1b\x63om.cloudidl.objectstore.v1B\x17ObjectstoreServiceProtoH\x02P\x01Z.github.com/unionai/cloud/gen/pb-go/objectstore\xa2\x02\x03\x43OX\xaa\x02\x17\x43loudidl.Objectstore.V1\xca\x02\x17\x43loudidl\\Objectstore\\V1\xe2\x02#Cloudidl\\Objectstore\\V1\\GPBMetadata\xea\x02\x19\x43loudidl::Objectstore::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'objectstore.objectstore_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033com.cloudidl.objectstore.v1B\027ObjectstoreServiceProtoH\002P\001Z.github.com/unionai/cloud/gen/pb-go/objectstore\242\002\003COX\252\002\027Cloudidl.Objectstore.V1\312\002\027Cloudidl\\Objectstore\\V1\342\002#Cloudidl\\Objectstore\\V1\\GPBMetadata\352\002\031Cloudidl::Objectstore::V1'
  _globals['_OBJECTSTORESERVICE']._serialized_start=94
  _globals['_OBJECTSTORESERVICE']._serialized_end=1405
# @@protoc_insertion_point(module_scope)
