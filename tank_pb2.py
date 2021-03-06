# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tank.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tank.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\ntank.proto\" \n\x08Position\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02\"S\n\x06Player\x12\x0c\n\x04nick\x18\x01 \x02(\t\x12\x16\n\x03pos\x18\x02 \x02(\x0b\x32\t.Position\x12\n\n\x02hp\x18\x03 \x02(\x02\x12\x17\n\x03\x64ir\x18\x04 \x02(\x0e\x32\n.Direction\"V\n\x06\x42ullet\x12\n\n\x02id\x18\x01 \x01(\x07\x12\x0f\n\x07shooter\x18\x02 \x01(\x07\x12\x16\n\x03pos\x18\x03 \x01(\x0b\x32\t.Position\x12\x17\n\x03\x64ir\x18\x04 \x01(\x0e\x32\n.Direction\"\x1d\n\rNickSelection\x12\x0c\n\x04nick\x18\x01 \x01(\t\"\x1a\n\x05Voice\x12\x11\n\tvoicedata\x18\x01 \x02(\x0c\";\n\x08Movement\x12\x16\n\x03pos\x18\x01 \x02(\x0b\x32\t.Position\x12\x17\n\x03\x64ir\x18\x02 \x02(\x0e\x32\n.Direction\"v\n\rInfoBroadcast\x12,\n\x07players\x18\x01 \x03(\x0b\x32\x1b.InfoBroadcast.PlayersEntry\x1a\x37\n\x0cPlayersEntry\x12\x0b\n\x03key\x18\x01 \x01(\x07\x12\x16\n\x05value\x18\x02 \x01(\x0b\x32\x07.Player:\x02\x38\x01\"z\n\x0f\x42ulletBroadcast\x12.\n\x07\x62ullets\x18\x01 \x03(\x0b\x32\x1d.BulletBroadcast.BulletsEntry\x1a\x37\n\x0c\x42ulletsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x07\x12\x16\n\x05value\x18\x02 \x01(\x0b\x32\x07.Bullet:\x02\x38\x01\"\x18\n\nDisconnect\x12\n\n\x02id\x18\x01 \x02(\x07\"7\n\x04Init\x12\n\n\x02id\x18\x01 \x02(\x07\x12\n\n\x02hp\x18\x02 \x02(\x02\x12\x17\n\x04move\x18\x03 \x02(\x0b\x32\t.Movement\"\x1b\n\x0c\x45rrorMessage\x12\x0b\n\x03msg\x18\x01 \x02(\t*2\n\tDirection\x12\x06\n\x02UP\x10\x00\x12\x08\n\x04\x44OWN\x10\x01\x12\t\n\x05RIGHT\x10\x02\x12\x08\n\x04LEFT\x10\x03'
)

_DIRECTION = _descriptor.EnumDescriptor(
  name='Direction',
  full_name='Direction',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UP', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DOWN', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RIGHT', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LEFT', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=697,
  serialized_end=747,
)
_sym_db.RegisterEnumDescriptor(_DIRECTION)

Direction = enum_type_wrapper.EnumTypeWrapper(_DIRECTION)
UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3



_POSITION = _descriptor.Descriptor(
  name='Position',
  full_name='Position',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='Position.x', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='Position.y', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=14,
  serialized_end=46,
)


_PLAYER = _descriptor.Descriptor(
  name='Player',
  full_name='Player',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nick', full_name='Player.nick', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pos', full_name='Player.pos', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hp', full_name='Player.hp', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dir', full_name='Player.dir', index=3,
      number=4, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=131,
)


_BULLET = _descriptor.Descriptor(
  name='Bullet',
  full_name='Bullet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Bullet.id', index=0,
      number=1, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='shooter', full_name='Bullet.shooter', index=1,
      number=2, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pos', full_name='Bullet.pos', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dir', full_name='Bullet.dir', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=133,
  serialized_end=219,
)


_NICKSELECTION = _descriptor.Descriptor(
  name='NickSelection',
  full_name='NickSelection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nick', full_name='NickSelection.nick', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=221,
  serialized_end=250,
)


_VOICE = _descriptor.Descriptor(
  name='Voice',
  full_name='Voice',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='voicedata', full_name='Voice.voicedata', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=252,
  serialized_end=278,
)


_MOVEMENT = _descriptor.Descriptor(
  name='Movement',
  full_name='Movement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pos', full_name='Movement.pos', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dir', full_name='Movement.dir', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=280,
  serialized_end=339,
)


_INFOBROADCAST_PLAYERSENTRY = _descriptor.Descriptor(
  name='PlayersEntry',
  full_name='InfoBroadcast.PlayersEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='InfoBroadcast.PlayersEntry.key', index=0,
      number=1, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='InfoBroadcast.PlayersEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=404,
  serialized_end=459,
)

_INFOBROADCAST = _descriptor.Descriptor(
  name='InfoBroadcast',
  full_name='InfoBroadcast',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='players', full_name='InfoBroadcast.players', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_INFOBROADCAST_PLAYERSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=341,
  serialized_end=459,
)


_BULLETBROADCAST_BULLETSENTRY = _descriptor.Descriptor(
  name='BulletsEntry',
  full_name='BulletBroadcast.BulletsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='BulletBroadcast.BulletsEntry.key', index=0,
      number=1, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='BulletBroadcast.BulletsEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=528,
  serialized_end=583,
)

_BULLETBROADCAST = _descriptor.Descriptor(
  name='BulletBroadcast',
  full_name='BulletBroadcast',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bullets', full_name='BulletBroadcast.bullets', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_BULLETBROADCAST_BULLETSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=461,
  serialized_end=583,
)


_DISCONNECT = _descriptor.Descriptor(
  name='Disconnect',
  full_name='Disconnect',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Disconnect.id', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=585,
  serialized_end=609,
)


_INIT = _descriptor.Descriptor(
  name='Init',
  full_name='Init',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Init.id', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hp', full_name='Init.hp', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='move', full_name='Init.move', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=611,
  serialized_end=666,
)


_ERRORMESSAGE = _descriptor.Descriptor(
  name='ErrorMessage',
  full_name='ErrorMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='msg', full_name='ErrorMessage.msg', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=668,
  serialized_end=695,
)

_PLAYER.fields_by_name['pos'].message_type = _POSITION
_PLAYER.fields_by_name['dir'].enum_type = _DIRECTION
_BULLET.fields_by_name['pos'].message_type = _POSITION
_BULLET.fields_by_name['dir'].enum_type = _DIRECTION
_MOVEMENT.fields_by_name['pos'].message_type = _POSITION
_MOVEMENT.fields_by_name['dir'].enum_type = _DIRECTION
_INFOBROADCAST_PLAYERSENTRY.fields_by_name['value'].message_type = _PLAYER
_INFOBROADCAST_PLAYERSENTRY.containing_type = _INFOBROADCAST
_INFOBROADCAST.fields_by_name['players'].message_type = _INFOBROADCAST_PLAYERSENTRY
_BULLETBROADCAST_BULLETSENTRY.fields_by_name['value'].message_type = _BULLET
_BULLETBROADCAST_BULLETSENTRY.containing_type = _BULLETBROADCAST
_BULLETBROADCAST.fields_by_name['bullets'].message_type = _BULLETBROADCAST_BULLETSENTRY
_INIT.fields_by_name['move'].message_type = _MOVEMENT
DESCRIPTOR.message_types_by_name['Position'] = _POSITION
DESCRIPTOR.message_types_by_name['Player'] = _PLAYER
DESCRIPTOR.message_types_by_name['Bullet'] = _BULLET
DESCRIPTOR.message_types_by_name['NickSelection'] = _NICKSELECTION
DESCRIPTOR.message_types_by_name['Voice'] = _VOICE
DESCRIPTOR.message_types_by_name['Movement'] = _MOVEMENT
DESCRIPTOR.message_types_by_name['InfoBroadcast'] = _INFOBROADCAST
DESCRIPTOR.message_types_by_name['BulletBroadcast'] = _BULLETBROADCAST
DESCRIPTOR.message_types_by_name['Disconnect'] = _DISCONNECT
DESCRIPTOR.message_types_by_name['Init'] = _INIT
DESCRIPTOR.message_types_by_name['ErrorMessage'] = _ERRORMESSAGE
DESCRIPTOR.enum_types_by_name['Direction'] = _DIRECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Position = _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {
  'DESCRIPTOR' : _POSITION,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:Position)
  })
_sym_db.RegisterMessage(Position)

Player = _reflection.GeneratedProtocolMessageType('Player', (_message.Message,), {
  'DESCRIPTOR' : _PLAYER,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:Player)
  })
_sym_db.RegisterMessage(Player)

Bullet = _reflection.GeneratedProtocolMessageType('Bullet', (_message.Message,), {
  'DESCRIPTOR' : _BULLET,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:Bullet)
  })
_sym_db.RegisterMessage(Bullet)

NickSelection = _reflection.GeneratedProtocolMessageType('NickSelection', (_message.Message,), {
  'DESCRIPTOR' : _NICKSELECTION,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:NickSelection)
  })
_sym_db.RegisterMessage(NickSelection)

Voice = _reflection.GeneratedProtocolMessageType('Voice', (_message.Message,), {
  'DESCRIPTOR' : _VOICE,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:Voice)
  })
_sym_db.RegisterMessage(Voice)

Movement = _reflection.GeneratedProtocolMessageType('Movement', (_message.Message,), {
  'DESCRIPTOR' : _MOVEMENT,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:Movement)
  })
_sym_db.RegisterMessage(Movement)

InfoBroadcast = _reflection.GeneratedProtocolMessageType('InfoBroadcast', (_message.Message,), {

  'PlayersEntry' : _reflection.GeneratedProtocolMessageType('PlayersEntry', (_message.Message,), {
    'DESCRIPTOR' : _INFOBROADCAST_PLAYERSENTRY,
    '__module__' : 'tank_pb2'
    # @@protoc_insertion_point(class_scope:InfoBroadcast.PlayersEntry)
    })
  ,
  'DESCRIPTOR' : _INFOBROADCAST,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:InfoBroadcast)
  })
_sym_db.RegisterMessage(InfoBroadcast)
_sym_db.RegisterMessage(InfoBroadcast.PlayersEntry)

BulletBroadcast = _reflection.GeneratedProtocolMessageType('BulletBroadcast', (_message.Message,), {

  'BulletsEntry' : _reflection.GeneratedProtocolMessageType('BulletsEntry', (_message.Message,), {
    'DESCRIPTOR' : _BULLETBROADCAST_BULLETSENTRY,
    '__module__' : 'tank_pb2'
    # @@protoc_insertion_point(class_scope:BulletBroadcast.BulletsEntry)
    })
  ,
  'DESCRIPTOR' : _BULLETBROADCAST,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:BulletBroadcast)
  })
_sym_db.RegisterMessage(BulletBroadcast)
_sym_db.RegisterMessage(BulletBroadcast.BulletsEntry)

Disconnect = _reflection.GeneratedProtocolMessageType('Disconnect', (_message.Message,), {
  'DESCRIPTOR' : _DISCONNECT,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:Disconnect)
  })
_sym_db.RegisterMessage(Disconnect)

Init = _reflection.GeneratedProtocolMessageType('Init', (_message.Message,), {
  'DESCRIPTOR' : _INIT,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:Init)
  })
_sym_db.RegisterMessage(Init)

ErrorMessage = _reflection.GeneratedProtocolMessageType('ErrorMessage', (_message.Message,), {
  'DESCRIPTOR' : _ERRORMESSAGE,
  '__module__' : 'tank_pb2'
  # @@protoc_insertion_point(class_scope:ErrorMessage)
  })
_sym_db.RegisterMessage(ErrorMessage)


_INFOBROADCAST_PLAYERSENTRY._options = None
_BULLETBROADCAST_BULLETSENTRY._options = None
# @@protoc_insertion_point(module_scope)
