# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: quokka.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cquokka.proto\x12\x06quokka\"\xfb-\n\x06Quokka\x12!\n\x04meta\x18\x01 \x01(\x0b\x32\x13.quokka.Quokka.Meta\x12\x32\n\rexporter_meta\x18\x02 \x01(\x0b\x32\x1b.quokka.Quokka.ExporterMeta\x12%\n\x06layout\x18\x03 \x03(\x0b\x32\x15.quokka.Quokka.Layout\x12!\n\x04\x64\x61ta\x18\x04 \x03(\x0b\x32\x13.quokka.Quokka.Data\x12)\n\x07structs\x18\x05 \x03(\x0b\x32\x18.quokka.Quokka.Structure\x12\x35\n\x0f\x66unction_chunks\x18\x06 \x03(\x0b\x32\x1c.quokka.Quokka.FunctionChunk\x12\x30\n\x0cinstructions\x18\x07 \x03(\x0b\x32\x1a.quokka.Quokka.Instruction\x12\x11\n\tmnemonics\x18\x08 \x03(\t\x12*\n\tfunctions\x18\t \x03(\x0b\x32\x17.quokka.Quokka.Function\x12,\n\nreferences\x18\n \x03(\x0b\x32\x18.quokka.Quokka.Reference\x12\x14\n\x0cstring_table\x18\x0b \x03(\t\x12\x15\n\roperand_table\x18\x10 \x03(\t\x12(\n\x08operands\x18\x0c \x03(\x0b\x32\x16.quokka.Quokka.Operand\x12\x15\n\rcomment_table\x18\r \x03(\t\x12(\n\x08\x63omments\x18\x0e \x03(\x0b\x32\x16.quokka.Quokka.Comment\x12(\n\x08segments\x18\x0f \x03(\x0b\x32\x16.quokka.Quokka.Segment\x1a\x87\x01\n\x0c\x45xporterMeta\x12.\n\x04mode\x18\x01 \x01(\x0e\x32 .quokka.Quokka.ExporterMeta.Mode\x12\x0f\n\x07version\x18\x02 \x01(\t\"6\n\x04Mode\x12\x0e\n\nMODE_LIGHT\x10\x00\x12\r\n\tMODE_FULL\x10\x01\x12\x0f\n\x0bMODE_NORMAL\x10\x02\x1a\xfe\x06\n\x04Meta\x12\x17\n\x0f\x65xecutable_name\x18\x01 \x01(\t\x12$\n\x03isa\x18\x02 \x01(\x0e\x32\x17.quokka.Quokka.Meta.ISA\x12.\n\x08\x63ompiler\x18\x03 \x01(\x0e\x32\x1c.quokka.Quokka.Meta.Compiler\x12\x41\n\x12\x63\x61lling_convention\x18\x04 \x01(\x0e\x32%.quokka.Quokka.Meta.CallingConvention\x12&\n\x04hash\x18\x05 \x01(\x0b\x32\x18.quokka.Quokka.Meta.Hash\x12\x30\n\tendianess\x18\x06 \x01(\x0e\x32\x1d.quokka.Quokka.Meta.Endianess\x12\x30\n\x0c\x61\x64\x64ress_size\x18\t \x01(\x0e\x32\x1a.quokka.Quokka.AddressSize\x12\x11\n\tbase_addr\x18\x07 \x01(\x04\x12\x13\n\x0bida_version\x18\x08 \x01(\r\x1a\x8a\x01\n\x04Hash\x12\x34\n\thash_type\x18\x01 \x01(\x0e\x32!.quokka.Quokka.Meta.Hash.HashType\x12\x12\n\nhash_value\x18\x02 \x01(\t\"8\n\x08HashType\x12\r\n\tHASH_NONE\x10\x00\x12\x0f\n\x0bHASH_SHA256\x10\x01\x12\x0c\n\x08HASH_MD5\x10\x02\"_\n\x03ISA\x12\x0e\n\nPROC_INTEL\x10\x00\x12\x0c\n\x08PROC_ARM\x10\x01\x12\x0f\n\x0bPROC_DALVIK\x10\x02\x12\x0c\n\x08PROC_PPC\x10\x03\x12\r\n\tPROC_MIPS\x10\x04\x12\x0c\n\x08PROC_UNK\x10\x05\"0\n\tEndianess\x12\n\n\x06\x45ND_LE\x10\x00\x12\n\n\x06\x45ND_BE\x10\x01\x12\x0b\n\x07\x45ND_UNK\x10\x02\"o\n\x08\x43ompiler\x12\x0c\n\x08\x43OMP_GCC\x10\x00\x12\x0b\n\x07\x43OMP_MS\x10\x01\x12\x0b\n\x07\x43OMP_BC\x10\x02\x12\x0f\n\x0b\x43OMP_WATCOM\x10\x03\x12\x0f\n\x0b\x43OMP_VISAGE\x10\x04\x12\x0b\n\x07\x43OMP_BP\x10\x05\x12\x0c\n\x08\x43OMP_UNK\x10\x06\"\x7f\n\x11\x43\x61llingConvention\x12\n\n\x06\x43\x43_UNK\x10\x00\x12\x0c\n\x08\x43\x43_CDECL\x10\x01\x12\x0f\n\x0b\x43\x43_ELLIPSIS\x10\x02\x12\x0e\n\nCC_STDCALL\x10\x03\x12\r\n\tCC_PASCAL\x10\x04\x12\x0f\n\x0b\x43\x43_FASTCALL\x10\x05\x12\x0f\n\x0b\x43\x43_THISCALL\x10\x06\x1a\xa6\x01\n\x07Operand\x12\x0c\n\x04type\x18\x01 \x01(\r\x12\r\n\x05\x66lags\x18\x02 \x01(\r\x12\x12\n\nvalue_type\x18\x03 \x01(\r\x12\x13\n\x0bregister_id\x18\x04 \x01(\r\x12\x11\n\tphrase_id\x18\x05 \x01(\r\x12\r\n\x05value\x18\x06 \x01(\x04\x12\x0f\n\x07\x61\x64\x64ress\x18\x07 \x01(\x03\x12\x0f\n\x07specval\x18\x08 \x01(\x04\x12\x11\n\tspecflags\x18\t \x03(\r\x1au\n\x0bInstruction\x12\x0c\n\x04size\x18\x01 \x01(\r\x12\x16\n\x0emnemonic_index\x18\x02 \x01(\r\x12\x15\n\roperand_index\x18\x03 \x03(\r\x12\x10\n\x08is_thumb\x18\x04 \x01(\x08\x12\x17\n\x0foperand_strings\x18\x05 \x03(\x04\x1a\x87\x04\n\rFunctionChunk\x12\x14\n\x0coffset_start\x18\x01 \x01(\x04\x12\x32\n\x06\x62locks\x18\x02 \x03(\x0b\x32\".quokka.Quokka.FunctionChunk.Block\x12\"\n\x05\x65\x64ges\x18\x03 \x03(\x0b\x32\x13.quokka.Quokka.Edge\x12\x0f\n\x07is_fake\x18\x04 \x01(\x08\x12\x11\n\tis_infile\x18\x05 \x01(\x08\x1a\xe3\x02\n\x05\x42lock\x12\x14\n\x0coffset_start\x18\x01 \x01(\x04\x12\x0f\n\x07is_fake\x18\x02 \x01(\x08\x12\x1a\n\x12instructions_index\x18\x03 \x03(\r\x12@\n\nblock_type\x18\x04 \x01(\x0e\x32,.quokka.Quokka.FunctionChunk.Block.BlockType\"\xd4\x01\n\tBlockType\x12\x15\n\x11\x42LOCK_TYPE_NORMAL\x10\x00\x12\x16\n\x12\x42LOCK_TYPE_INDJUMP\x10\x01\x12\x12\n\x0e\x42LOCK_TYPE_RET\x10\x02\x12\x14\n\x10\x42LOCK_TYPE_NORET\x10\x03\x12\x15\n\x11\x42LOCK_TYPE_CNDRET\x10\x04\x12\x15\n\x11\x42LOCK_TYPE_ENORET\x10\x05\x12\x15\n\x11\x42LOCK_TYPE_EXTERN\x10\x06\x12\x14\n\x10\x42LOCK_TYPE_ERROR\x10\x07\x12\x13\n\x0f\x42LOCK_TYPE_FAKE\x10\x08\x1aV\n\x0f\x42lockIdentifier\x12\x10\n\x08\x62lock_id\x18\x01 \x01(\r\x12\x12\n\x08no_chunk\x18\x02 \x01(\x08H\x00\x12\x12\n\x08\x63hunk_id\x18\x03 \x01(\rH\x00\x42\t\n\x07\x43hunkId\x1a\xf0\x01\n\x04\x45\x64ge\x12/\n\tedge_type\x18\x01 \x01(\x0e\x32\x1c.quokka.Quokka.Edge.EdgeType\x12.\n\x06source\x18\x02 \x01(\x0b\x32\x1e.quokka.Quokka.BlockIdentifier\x12\x33\n\x0b\x64\x65stination\x18\x03 \x01(\x0b\x32\x1e.quokka.Quokka.BlockIdentifier\"R\n\x08\x45\x64geType\x12\x16\n\x12TYPE_UNCONDITIONAL\x10\x00\x12\r\n\tTYPE_TRUE\x10\x01\x12\x0e\n\nTYPE_FALSE\x10\x02\x12\x0f\n\x0bTYPE_SWITCH\x10\x03\x1a\xf6\x04\n\x08\x46unction\x12\x0e\n\x06offset\x18\x01 \x01(\r\x12\x1d\n\x15\x66unction_chunks_index\x18\x02 \x03(\r\x12;\n\rfunction_type\x18\x03 \x01(\x0e\x32$.quokka.Quokka.Function.FunctionType\x12\x0c\n\x04name\x18\x04 \x01(\t\x12(\n\x0b\x63hunk_edges\x18\x05 \x03(\x0b\x32\x13.quokka.Quokka.Edge\x12>\n\x0f\x62lock_positions\x18\x06 \x03(\x0b\x32%.quokka.Quokka.Function.BlockPosition\x12\x14\n\x0cmangled_name\x18\x07 \x01(\t\x1a\x90\x01\n\x08Position\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05\x12\x44\n\rposition_type\x18\x03 \x01(\x0e\x32-.quokka.Quokka.Function.Position.PositionType\"(\n\x0cPositionType\x12\n\n\x06\x43\x45NTER\x10\x00\x12\x0c\n\x08TOP_LEFT\x10\x01\x1au\n\rBlockPosition\x12\x30\n\x08\x62lock_id\x18\x01 \x01(\x0b\x32\x1e.quokka.Quokka.BlockIdentifier\x12\x32\n\x08position\x18\x02 \x01(\x0b\x32 .quokka.Quokka.Function.Position\"f\n\x0c\x46unctionType\x12\x0f\n\x0bTYPE_NORMAL\x10\x00\x12\x11\n\rTYPE_IMPORTED\x10\x01\x12\x10\n\x0cTYPE_LIBRARY\x10\x02\x12\x0e\n\nTYPE_THUNK\x10\x03\x12\x10\n\x0cTYPE_INVALID\x10\x04\x1a\xff\x01\n\x06Layout\x12\x39\n\raddress_range\x18\x01 \x01(\x0b\x32\".quokka.Quokka.Layout.AddressRange\x12\x35\n\x0blayout_type\x18\x02 \x01(\x0e\x32 .quokka.Quokka.Layout.LayoutType\x1a\x33\n\x0c\x41\x64\x64ressRange\x12\x15\n\rstart_address\x18\x01 \x01(\x04\x12\x0c\n\x04size\x18\x02 \x01(\x04\"N\n\nLayoutType\x12\x0e\n\nLAYOUT_UNK\x10\x00\x12\x0f\n\x0bLAYOUT_CODE\x10\x01\x12\x0f\n\x0bLAYOUT_DATA\x10\x02\x12\x0e\n\nLAYOUT_GAP\x10\x03\x1a\xae\x01\n\x04\x44\x61ta\x12\x0e\n\x06offset\x18\x01 \x01(\x04\x12%\n\x04type\x18\x02 \x01(\x0e\x32\x17.quokka.Quokka.DataType\x12\x0e\n\x04size\x18\x03 \x01(\rH\x00\x12\x11\n\x07no_size\x18\x04 \x01(\x08H\x00\x12\x13\n\x0bvalue_index\x18\x05 \x01(\r\x12\x12\n\nname_index\x18\x06 \x01(\r\x12\x17\n\x0fnot_initialized\x18\x07 \x01(\x08\x42\n\n\x08\x44\x61taSize\x1a\xe1\x02\n\tStructure\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x34\n\x04type\x18\x02 \x01(\x0e\x32&.quokka.Quokka.Structure.StructureType\x12\x0c\n\x04size\x18\x03 \x01(\r\x12\x15\n\rvariable_size\x18\x04 \x01(\x08\x12\x30\n\x07members\x18\x05 \x03(\x0b\x32\x1f.quokka.Quokka.Structure.Member\x1aj\n\x06Member\x12\x0e\n\x06offset\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04type\x18\x03 \x01(\x0e\x32\x17.quokka.Quokka.DataType\x12\x0c\n\x04size\x18\x04 \x01(\r\x12\r\n\x05value\x18\x05 \x01(\x03\"M\n\rStructureType\x12\x0f\n\x0bTYPE_STRUCT\x10\x00\x12\r\n\tTYPE_ENUM\x10\x01\x12\x0e\n\nTYPE_UNION\x10\x02\x12\x0c\n\x08TYPE_UNK\x10\x03\x1a\xe4\x01\n\x07\x43omment\x12\x30\n\x04type\x18\x01 \x01(\x0e\x32\".quokka.Quokka.Comment.CommentType\x12\x12\n\nstring_idx\x18\x02 \x01(\r\x12)\n\x08location\x18\x03 \x01(\x0b\x32\x17.quokka.Quokka.Location\"h\n\x0b\x43ommentType\x12\x17\n\x13\x43OMMENT_INSTRUCTION\x10\x00\x12\x14\n\x10\x43OMMENT_FUNCTION\x10\x01\x12\x15\n\x11\x43OMMENT_STRUCTURE\x10\x02\x12\x13\n\x0f\x43OMMENT_INVALID\x10\x03\x1a\xc4\x03\n\x08Location\x12\x12\n\x08inst_idx\x18\x01 \x01(\x04H\x00\x12\x12\n\x08\x64\x61ta_idx\x18\x02 \x01(\rH\x00\x12\x44\n\x0fstruct_position\x18\x03 \x01(\x0b\x32).quokka.Quokka.Location.StructurePositionH\x00\x12M\n\x14instruction_position\x18\x04 \x01(\x0b\x32-.quokka.Quokka.Location.InstructionIdentifierH\x00\x12\x16\n\x0c\x66unction_idx\x18\x05 \x01(\rH\x00\x12\x13\n\tchunk_idx\x18\x06 \x01(\rH\x00\x1a\x61\n\x11StructurePosition\x12\x15\n\rstructure_idx\x18\x01 \x01(\r\x12\x14\n\nmember_idx\x18\x02 \x01(\rH\x00\x12\x13\n\tno_member\x18\x03 \x01(\x08H\x00\x42\n\n\x08MemberId\x1a[\n\x15InstructionIdentifier\x12\x16\n\x0e\x66unc_chunk_idx\x18\x01 \x01(\r\x12\x11\n\tblock_idx\x18\x02 \x01(\r\x12\x17\n\x0finstruction_idx\x18\x03 \x01(\rB\x0e\n\x0cLocationType\x1a\xf9\x01\n\tReference\x12\'\n\x06source\x18\x01 \x01(\x0b\x32\x17.quokka.Quokka.Location\x12,\n\x0b\x64\x65stination\x18\x02 \x01(\x0b\x32\x17.quokka.Quokka.Location\x12>\n\x0ereference_type\x18\x03 \x01(\x0e\x32&.quokka.Quokka.Reference.ReferenceType\"U\n\rReferenceType\x12\x0c\n\x08REF_CALL\x10\x00\x12\x0c\n\x08REF_DATA\x10\x01\x12\x0c\n\x08REF_ENUM\x10\x02\x12\r\n\tREF_STRUC\x10\x03\x12\x0b\n\x07REF_UNK\x10\x04\x1a\xdd\x03\n\x07Segment\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\nstart_addr\x18\x02 \x01(\x04\x12\x0c\n\x04size\x18\x03 \x01(\x04\x12\x13\n\x0bpermissions\x18\x04 \x01(\r\x12)\n\x04type\x18\x05 \x01(\x0e\x32\x1b.quokka.Quokka.Segment.Type\x12\x30\n\x0c\x61\x64\x64ress_size\x18\x06 \x01(\x0e\x32\x1a.quokka.Quokka.AddressSize\x12\x15\n\x0b\x66ile_offset\x18\x07 \x01(\x04H\x00\x12\x13\n\tno_offset\x18\x08 \x01(\x08H\x00\"\xa4\x01\n\x04Type\x12\x0f\n\x0bSEGMENT_UNK\x10\x00\x12\x10\n\x0cSEGMENT_CODE\x10\x01\x12\x10\n\x0cSEGMENT_DATA\x10\x02\x12\x0f\n\x0bSEGMENT_BSS\x10\x03\x12\x10\n\x0cSEGMENT_NULL\x10\x04\x12\x12\n\x0eSEGMENT_EXTERN\x10\x05\x12\x12\n\x0eSEGMENT_NORMAL\x10\x06\x12\x1c\n\x18SEGMENT_ABSOLUTE_SYMBOLS\x10\x07\"N\n\x07\x42itness\x12\x0e\n\nBITNESS_64\x10\x00\x12\x0e\n\nBITNESS_32\x10\x01\x12\x0e\n\nBITNESS_16\x10\x02\x12\x13\n\x0f\x42ITNESS_UNKNOWN\x10\x03\x42\r\n\x0boffset_type\"5\n\x0b\x41\x64\x64ressSize\x12\x0c\n\x08\x41\x44\x44R_UNK\x10\x00\x12\x0b\n\x07\x41\x44\x44R_32\x10\x01\x12\x0b\n\x07\x41\x44\x44R_64\x10\x02\"\xbb\x01\n\x08\x44\x61taType\x12\x0c\n\x08TYPE_UNK\x10\x00\x12\n\n\x06TYPE_B\x10\x01\x12\n\n\x06TYPE_W\x10\x02\x12\x0b\n\x07TYPE_DW\x10\x03\x12\x0b\n\x07TYPE_QW\x10\x04\x12\x0b\n\x07TYPE_OW\x10\x05\x12\x0e\n\nTYPE_FLOAT\x10\x06\x12\x0f\n\x0bTYPE_DOUBLE\x10\x07\x12\x0e\n\nTYPE_ASCII\x10\x08\x12\x0f\n\x0bTYPE_STRUCT\x10\t\x12\x0e\n\nTYPE_ALIGN\x10\n\x12\x10\n\x0cTYPE_POINTER\x10\x0b\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'quokka_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_QUOKKA']._serialized_start=25
  _globals['_QUOKKA']._serialized_end=5908
  _globals['_QUOKKA_EXPORTERMETA']._serialized_start=648
  _globals['_QUOKKA_EXPORTERMETA']._serialized_end=783
  _globals['_QUOKKA_EXPORTERMETA_MODE']._serialized_start=729
  _globals['_QUOKKA_EXPORTERMETA_MODE']._serialized_end=783
  _globals['_QUOKKA_META']._serialized_start=786
  _globals['_QUOKKA_META']._serialized_end=1680
  _globals['_QUOKKA_META_HASH']._serialized_start=1153
  _globals['_QUOKKA_META_HASH']._serialized_end=1291
  _globals['_QUOKKA_META_HASH_HASHTYPE']._serialized_start=1235
  _globals['_QUOKKA_META_HASH_HASHTYPE']._serialized_end=1291
  _globals['_QUOKKA_META_ISA']._serialized_start=1293
  _globals['_QUOKKA_META_ISA']._serialized_end=1388
  _globals['_QUOKKA_META_ENDIANESS']._serialized_start=1390
  _globals['_QUOKKA_META_ENDIANESS']._serialized_end=1438
  _globals['_QUOKKA_META_COMPILER']._serialized_start=1440
  _globals['_QUOKKA_META_COMPILER']._serialized_end=1551
  _globals['_QUOKKA_META_CALLINGCONVENTION']._serialized_start=1553
  _globals['_QUOKKA_META_CALLINGCONVENTION']._serialized_end=1680
  _globals['_QUOKKA_OPERAND']._serialized_start=1683
  _globals['_QUOKKA_OPERAND']._serialized_end=1849
  _globals['_QUOKKA_INSTRUCTION']._serialized_start=1851
  _globals['_QUOKKA_INSTRUCTION']._serialized_end=1968
  _globals['_QUOKKA_FUNCTIONCHUNK']._serialized_start=1971
  _globals['_QUOKKA_FUNCTIONCHUNK']._serialized_end=2490
  _globals['_QUOKKA_FUNCTIONCHUNK_BLOCK']._serialized_start=2135
  _globals['_QUOKKA_FUNCTIONCHUNK_BLOCK']._serialized_end=2490
  _globals['_QUOKKA_FUNCTIONCHUNK_BLOCK_BLOCKTYPE']._serialized_start=2278
  _globals['_QUOKKA_FUNCTIONCHUNK_BLOCK_BLOCKTYPE']._serialized_end=2490
  _globals['_QUOKKA_BLOCKIDENTIFIER']._serialized_start=2492
  _globals['_QUOKKA_BLOCKIDENTIFIER']._serialized_end=2578
  _globals['_QUOKKA_EDGE']._serialized_start=2581
  _globals['_QUOKKA_EDGE']._serialized_end=2821
  _globals['_QUOKKA_EDGE_EDGETYPE']._serialized_start=2739
  _globals['_QUOKKA_EDGE_EDGETYPE']._serialized_end=2821
  _globals['_QUOKKA_FUNCTION']._serialized_start=2824
  _globals['_QUOKKA_FUNCTION']._serialized_end=3454
  _globals['_QUOKKA_FUNCTION_POSITION']._serialized_start=3087
  _globals['_QUOKKA_FUNCTION_POSITION']._serialized_end=3231
  _globals['_QUOKKA_FUNCTION_POSITION_POSITIONTYPE']._serialized_start=3191
  _globals['_QUOKKA_FUNCTION_POSITION_POSITIONTYPE']._serialized_end=3231
  _globals['_QUOKKA_FUNCTION_BLOCKPOSITION']._serialized_start=3233
  _globals['_QUOKKA_FUNCTION_BLOCKPOSITION']._serialized_end=3350
  _globals['_QUOKKA_FUNCTION_FUNCTIONTYPE']._serialized_start=3352
  _globals['_QUOKKA_FUNCTION_FUNCTIONTYPE']._serialized_end=3454
  _globals['_QUOKKA_LAYOUT']._serialized_start=3457
  _globals['_QUOKKA_LAYOUT']._serialized_end=3712
  _globals['_QUOKKA_LAYOUT_ADDRESSRANGE']._serialized_start=3581
  _globals['_QUOKKA_LAYOUT_ADDRESSRANGE']._serialized_end=3632
  _globals['_QUOKKA_LAYOUT_LAYOUTTYPE']._serialized_start=3634
  _globals['_QUOKKA_LAYOUT_LAYOUTTYPE']._serialized_end=3712
  _globals['_QUOKKA_DATA']._serialized_start=3715
  _globals['_QUOKKA_DATA']._serialized_end=3889
  _globals['_QUOKKA_STRUCTURE']._serialized_start=3892
  _globals['_QUOKKA_STRUCTURE']._serialized_end=4245
  _globals['_QUOKKA_STRUCTURE_MEMBER']._serialized_start=4060
  _globals['_QUOKKA_STRUCTURE_MEMBER']._serialized_end=4166
  _globals['_QUOKKA_STRUCTURE_STRUCTURETYPE']._serialized_start=4168
  _globals['_QUOKKA_STRUCTURE_STRUCTURETYPE']._serialized_end=4245
  _globals['_QUOKKA_COMMENT']._serialized_start=4248
  _globals['_QUOKKA_COMMENT']._serialized_end=4476
  _globals['_QUOKKA_COMMENT_COMMENTTYPE']._serialized_start=4372
  _globals['_QUOKKA_COMMENT_COMMENTTYPE']._serialized_end=4476
  _globals['_QUOKKA_LOCATION']._serialized_start=4479
  _globals['_QUOKKA_LOCATION']._serialized_end=4931
  _globals['_QUOKKA_LOCATION_STRUCTUREPOSITION']._serialized_start=4725
  _globals['_QUOKKA_LOCATION_STRUCTUREPOSITION']._serialized_end=4822
  _globals['_QUOKKA_LOCATION_INSTRUCTIONIDENTIFIER']._serialized_start=4824
  _globals['_QUOKKA_LOCATION_INSTRUCTIONIDENTIFIER']._serialized_end=4915
  _globals['_QUOKKA_REFERENCE']._serialized_start=4934
  _globals['_QUOKKA_REFERENCE']._serialized_end=5183
  _globals['_QUOKKA_REFERENCE_REFERENCETYPE']._serialized_start=5098
  _globals['_QUOKKA_REFERENCE_REFERENCETYPE']._serialized_end=5183
  _globals['_QUOKKA_SEGMENT']._serialized_start=5186
  _globals['_QUOKKA_SEGMENT']._serialized_end=5663
  _globals['_QUOKKA_SEGMENT_TYPE']._serialized_start=5404
  _globals['_QUOKKA_SEGMENT_TYPE']._serialized_end=5568
  _globals['_QUOKKA_SEGMENT_BITNESS']._serialized_start=5570
  _globals['_QUOKKA_SEGMENT_BITNESS']._serialized_end=5648
  _globals['_QUOKKA_ADDRESSSIZE']._serialized_start=5665
  _globals['_QUOKKA_ADDRESSSIZE']._serialized_end=5718
  _globals['_QUOKKA_DATATYPE']._serialized_start=5721
  _globals['_QUOKKA_DATATYPE']._serialized_end=5908
# @@protoc_insertion_point(module_scope)
