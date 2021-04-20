from utils.enums import FlagCC, Flags
from processor.Z80 import Z80

def write_byte(fout, string: str, base=2, pattern='*', in_bytes=False):
	result = '{0:0{1}X}'.format(int(pattern.replace('*', string), base), 2)

	if in_bytes:
		fout.write(bytes.fromhex(result))
	else:
		fout.write(result)

	return 1


def write_hex(fout, hexstring: str, in_bytes=False):
	return write_byte(fout, hexstring, 16, in_bytes=in_bytes)


def conditional_flag(flagcc:str = None) -> bool:
	"""If no flag is given this returns True
	"""
	return ((flagcc == FlagCC.NZ.value and not Z80().getFlag(Flags.Z.name)) or
		(flagcc == FlagCC.Z.value and Z80().getFlag(Flags.Z.name)) or
		(flagcc == FlagCC.NC.value and not Z80().getFlag(Flags.C.name)) or
		(flagcc == FlagCC.C.value and Z80().getFlag(Flags.C.name)) or
		(flagcc == FlagCC.PO.value and not Z80().getFlag(Flags.PV.name)) or
		(flagcc == FlagCC.PE.value and Z80().getFlag(Flags.PV.name)) or
		(flagcc == FlagCC.P.value and not Z80().getFlag(Flags.S.name)) or
		(flagcc == FlagCC.M.value and Z80().getFlag(Flags.S.name))) or flagcc is None