from processor.Bus import Bus
from processor.Z80 import Z80
from utils.Debug import Debug
from utils.enums import FlagCC
from processor.intructions.general import *

def call():
	Z80().offsetPC()

	# Get nn 
	memReqPC()
	val2 = Bus().data
	memReqPC()
	val1 = Bus().data

	# Memory update stack push first PC Value
	Bus().data = Z80().getRegister('PC') >> 8 
	Z80().stackPush()
	
	# Memory update stack push second PC Value
	Bus().data = Z80().getRegister('PC') & 0xFF
	Z80().stackPush()

	Z80().setRegister('PC', (val1 << 8) + val2)
	Debug().newFunction('CALL {:02X}{:02X}H'.format(val1,val2))
def ret():
	Z80().offsetPC()

	Z80().stackPop()
	val2 = Bus().data

	Z80().stackPop()
	val1 = Bus().data

	Z80().setRegister('PC', (val1 << 8) + val2)
	Debug().newFunction('RET')

def jump_call():
	import re

	JR_E 		= rf'00011000'
	JR_C_E 	= rf'00111000'
	JR_NC_E = rf'00110000'
	JR_Z_E	= rf'00101000'
	JR_NZ_E = rf'00100000'

	CALL_NN = rf'11001101'
	CALL_CC_NN = rf'11(?P<cc>{cc})100'

	RET 	 = rf'11001001'
	RET_CC = rf'11(?P<cc>{cc})000'

	if match := re.search(JR_E, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		memReqPC()
		Z80().offsetPC(Bus().data)
		Debug().newFunction('JR $+{:02X}'.format(Bus().data))

	elif match := re.search(JR_C_E, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		memReqPC()
		if Z80().getFlag('C'):
			Z80().offsetPC(Bus().data)
		Debug().newFunction('JR C, $+{:02X}'.format(Bus().data))

	elif match := re.search(JR_NC_E, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		memReqPC()
		if not Z80().getFlag('C'):
			Z80().offsetPC(Bus().data)
		Debug().newFunction('JR NC, $+{:02X}'.format(Bus().data))

	elif match := re.search(JR_Z_E, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		memReqPC()
		if not Z80().getFlag('Z'):
			Z80().offsetPC(Bus().data)
		Debug().newFunction('JR Z, $+{:02X}'.format(Bus().data))

	elif match := re.search(JR_NZ_E, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		memReqPC()
		if not Z80().getFlag('Z'):
			Z80().offsetPC(Bus().data)
		Debug().newFunction('JR NZ, $+{:02X}'.format(Bus().data))



	elif match := re.search(CALL_NN, '{0:08b}'.format(Bus().data)):
		call()

	elif match := re.search(CALL_CC_NN, '{0:08b}'.format(Bus().data)):
		if ((match.group('cc') == FlagCC.NZ.value and Z80().getFlag(FlagCC.NZ.name)) or
		(match.group('cc') == FlagCC.Z.value and Z80().getFlag(FlagCC.Z.name)) or
		(match.group('cc') == FlagCC.NC.value and Z80().getFlag(FlagCC.NC.name)) or
		(match.group('cc') == FlagCC.C.value and Z80().getFlag(FlagCC.C.name)) or
		(match.group('cc') == FlagCC.PO.value and Z80().getFlag(FlagCC.PO.name)) or
		(match.group('cc') == FlagCC.PE.value and Z80().getFlag(FlagCC.PE.name)) or
		(match.group('cc') == FlagCC.P.value and Z80().getFlag(FlagCC.P.name)) or
		(match.group('cc') == FlagCC.M.value and Z80().getFlag(FlagCC.M.name))):
			call()
		else:
			if match.group('cc') is not None:
				Debug().newFunction(f'CALL {FlagCC(match.group("cc")).name}, NN')
			Z80().offsetPC(2)

	elif match := re.search(RET, '{0:08b}'.format(Bus().data)):
		ret()

	elif match := re.search(RET_CC, '{0:08b}'.format(Bus().data)):
		if ((match.group('cc') == FlagCC.NZ.value and Z80().getFlag(FlagCC.NZ.name)) or
		(match.group('cc') == FlagCC.Z.value and Z80().getFlag(FlagCC.Z.name)) or
		(match.group('cc') == FlagCC.NC.value and Z80().getFlag(FlagCC.NC.name)) or
		(match.group('cc') == FlagCC.C.value and Z80().getFlag(FlagCC.C.name)) or
		(match.group('cc') == FlagCC.PO.value and Z80().getFlag(FlagCC.PO.name)) or
		(match.group('cc') == FlagCC.PE.value and Z80().getFlag(FlagCC.PE.name)) or
		(match.group('cc') == FlagCC.P.value and Z80().getFlag(FlagCC.P.name)) or
		(match.group('cc') == FlagCC.M.value and Z80().getFlag(FlagCC.M.name))):
			ret()
		else:
			Debug().newFunction(f'RET {FlagCC(match.group("cc")).name}')
			Z80().offsetPC()

	else:
		return False
	return True