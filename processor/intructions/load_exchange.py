from processor.Bus import Bus
from processor.Z80 import Z80
from utils.Debug import Debug
from processor.intructions.general import *

from utils.enums import Register

def load_exchange():
	import re

	LD_R_N = rf'00(?P<r>{non_HL_})110'
	LD_R_R = rf'01(?P<r1>{non_HL_})(?P<r2>{non_HL_})'
	LD_DD_NN = r'00(?P<dd>[01]{2})0001'
	LD__NN__A = rf'00110010'
	
	# LD Reg Number
	if match := re.search(LD_R_N, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()															# PC + 1
		register = Register(match.group('r')).name		# Get register
		memReqPC()																		# Request mem read at PC
		Z80().setRegister(register, Bus().data)				# set Register with Bus data
		Debug().newFunction('LD {}, {:02X}H'.format(register, Bus().data))
	
	#LD Reg Reg
	elif match := re.search(LD_R_R, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()															# PC + 1
		register_1 = Register(match.group('r1')).name	# Get register 1
		register_2 = Register(match.group('r2')).name	# Get register 2
		Z80().setRegister(register_1, Z80().getRegister(register_2)) # Set register 1 with value of register 2
		Debug().newFunction(f'LD {register_1}, {register_2}')

	#LD 2Reg 2Byte
	elif match := re.search(LD_DD_NN, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		register = Register(match.group('dd'))
		
		memReqPC()
		val_2 = Bus().data
		memReqPC()
		val_1 = Bus().data
		if register == Register.BC:
			Z80().setRegister('B', val_1)
			Z80().setRegister('C', val_2)
		elif register == Register.DE:
			Z80().setRegister('D', val_1)
			Z80().setRegister('E', val_2)
		elif register == Register.HL:
			Z80().setRegister('H', val_1)
			Z80().setRegister('L', val_2)
		elif register == Register.SP:
			Z80().setRegister('SP', (val_1 << 8)+val_2)
		else:
			Degug().newLog('No valid register can be accesed\nShould terminate?')
		Debug().newFunction('LD {}, {:02X}{:02X}H'.format(register.name, val_1, val_2))

	# LD (Number_16) Acumulator
	elif match := re.search(LD__NN__A, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()										# PC + 1
		memReqPC()												# Request mem read at PC
		val_1 = Bus().data									# Read Bus data
		memReqPC()												# Request mem read at PC
		val_2 = Bus().data									# Read Bus data
		Bus().address = val_1 + (val_2<< 8)	# Put address in Bus
		Bus().data = Z80().getRegister('A')	# Put Acumulator data in Bus
		Bus().memUpdate()										# Request Mem write
		Debug().newFunction('LD ({:04X}H), A'.format(Bus().address))
	else:
		return False
	return True