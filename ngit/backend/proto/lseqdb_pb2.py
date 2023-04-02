# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ngit/backend/proto/lseqdb.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fngit/backend/proto/lseqdb.proto\x12\x06lseqdb\x1a\x1bgoogle/protobuf/empty.proto\"A\n\nReplicaKey\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x17\n\nreplica_id\x18\x02 \x01(\x05H\x00\x88\x01\x01\x42\r\n\x0b_replica_id\"$\n\x05Value\x12\r\n\x05value\x18\x01 \x01(\t\x12\x0c\n\x04lseq\x18\x02 \x01(\t\"\x14\n\x04LSeq\x12\x0c\n\x04lseq\x18\x01 \x01(\t\"w\n\rEventsRequest\x12\x12\n\nreplica_id\x18\x01 \x01(\x05\x12\x11\n\x04lseq\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x10\n\x03key\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05limit\x18\x04 \x01(\rH\x02\x88\x01\x01\x42\x07\n\x05_lseqB\x06\n\x04_keyB\x08\n\x06_limit\"(\n\nPutRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"V\n\x0eSeekGetRequest\x12\x0c\n\x04lseq\x18\x01 \x01(\t\x12\x10\n\x03key\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x12\n\x05limit\x18\x03 \x01(\rH\x01\x88\x01\x01\x42\x06\n\x04_keyB\x08\n\x06_limit\"x\n\x07\x44\x42Items\x12%\n\x05items\x18\x01 \x03(\x0b\x32\x16.lseqdb.DBItems.DbItem\x12\x12\n\nreplica_id\x18\x02 \x01(\x05\x1a\x32\n\x06\x44\x62Item\x12\x0c\n\x04lseq\x18\x01 \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"$\n\x0eSyncGetRequest\x12\x12\n\nreplica_id\x18\x01 \x01(\x05\x32\xc9\x02\n\x0cLSeqDatabase\x12/\n\x08GetValue\x12\x12.lseqdb.ReplicaKey\x1a\r.lseqdb.Value\"\x00\x12)\n\x03Put\x12\x12.lseqdb.PutRequest\x1a\x0c.lseqdb.LSeq\"\x00\x12\x34\n\x07SeekGet\x12\x16.lseqdb.SeekGetRequest\x1a\x0f.lseqdb.DBItems\"\x00\x12<\n\x10GetReplicaEvents\x12\x15.lseqdb.EventsRequest\x1a\x0f.lseqdb.DBItems\"\x00\x12\x32\n\x08SyncGet_\x12\x16.lseqdb.SyncGetRequest\x1a\x0c.lseqdb.LSeq\"\x00\x12\x35\n\x08SyncPut_\x12\x0f.lseqdb.DBItems\x1a\x16.google.protobuf.Empty\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ngit.backend.proto.lseqdb_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REPLICAKEY._serialized_start=72
  _REPLICAKEY._serialized_end=137
  _VALUE._serialized_start=139
  _VALUE._serialized_end=175
  _LSEQ._serialized_start=177
  _LSEQ._serialized_end=197
  _EVENTSREQUEST._serialized_start=199
  _EVENTSREQUEST._serialized_end=318
  _PUTREQUEST._serialized_start=320
  _PUTREQUEST._serialized_end=360
  _SEEKGETREQUEST._serialized_start=362
  _SEEKGETREQUEST._serialized_end=448
  _DBITEMS._serialized_start=450
  _DBITEMS._serialized_end=570
  _DBITEMS_DBITEM._serialized_start=520
  _DBITEMS_DBITEM._serialized_end=570
  _SYNCGETREQUEST._serialized_start=572
  _SYNCGETREQUEST._serialized_end=608
  _LSEQDATABASE._serialized_start=611
  _LSEQDATABASE._serialized_end=940
# @@protoc_insertion_point(module_scope)