from processor.Bus import Bus
from processor.Z80 import Z80
from utils.Debug import Debug
from processor.intructions.general import *

from utils.enums import Register

def exchangeRegisters(register_1 , register_2 ):
	temp_reg = Z80().getRegisters(register_1)
	Z80().setRegister(register_1, Z80().getRegister(register_2))
	Z80().setRegister(register_2, temp_reg)



def load_exchange():
	import re

	LD_R_N = rf'00(?P<r>{non_HL_})110'
	LD_R_R = rf'01(?P<r1>{non_HL_})(?P<r2>{non_HL_})'
	LD_DD_NN = r'00(?P<dd>[01]{2})0001'
	LD__NN__A = rf'00110010'
	LD__HL__N = rf'00110110'
	

	LD_IX_D_R_1ST = rf'11011101'
	LD_IX_D_R_2ND = rf'01110(?P<r>{non_HL_})'
	LD_IY_D_R_1ST = rf'11111101'

	EX_DE_HL	=rf'11101011'
	EX_AF_AF_PRIME	=rf'00001000'

	EXX	 = rf'11011001'

	# LD Reg Number
	if match := re.search(LD_R_N, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()																														# PC + 1
		register = Register(match.group('r')).name																	# Get register
		memReqPC()																																	# Request mem read at PC
		Z80().setRegister(register, Bus().data)																			# set Register with Bus data
		Debug().newFunction('LD {}, {:02X}H'.format(register, Bus().data))
	
	#LD Reg Reg
	elif match := re.search(LD_R_R, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()																														# PC + 1
		register_1 = Register(match.group('r1')).name																# Get register 1
		register_2 = Register(match.group('r2')).name																# Get register 2
		Z80().setRegister(register_1, Z80().getRegister(register_2))								# Set register 1 with value of register 2
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
		Z80().offsetPC()																												# PC + 1
		memReqPC()																															# Request mem read at PC
		val_1 = Bus().data																											# Read Bus data
		memReqPC()																															# Request mem read at PC
		val_2 = Bus().data																											# Read Bus data
		Bus().address = (val_1<< 8) + val_2  																		# Put address in Bus
		Bus().data = Z80().getRegister('A')																			# Put Acumulator data in Bus
		Bus().memUpdate()																												# Request Mem write
		Debug().newFunction('LD ({:04X}H), A'.format(Bus().address))

	# LD (HL) N
	elif match := re.search(LD__HL__N, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()																																	
		memReqPC()																																				
		val_1 = Bus().data										
		memReqPC()												
		Bus().address = (Z80().getRegister('H')	<< 8) + Z80().getRegister('L')	  				
		Bus().data = val_1
		Bus().memUpdate()								
		Debug().newFunction('LD ({:04X}H), A'.format(Bus().address))

	# LD (IX+D) R  guarda el valor del registro R en la dirección de memoria (IX + D), con D en complemento a 2
	elif match := re.search(LD_IX_D_R_1ST, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()														# PC + 1
		segundo_byte=re.search(LD_IX_D_R_2ND, '{0:08b}'.format(Bus().data))		#get next byte
		Z80().offsetPC()														# PC + 1
		register = Register(segundo_byte.group('r')).name						# Get register
		memReqPC()																# Request mem read at PC
		direccion = (Z80().getRegister('H')<< 8) + Z80().getRegister('L')	+ distancia		
		distancia = Bus().data
		Bus().address = direccion														# Put address in Bus
		Bus().data = Z80().getRegister(register)										# Put register data in Bus
		Bus().memUpdate()

		Debug().newFunction('LD (IX+{:02X}H), {}'.format(distancia, register))

	# LD (IX+D) R  guarda el valor del registro R en la dirección de memoria (IX + D), con D en complemento a 2
	elif match := re.search(LD_IY_D_R_1ST, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()														# PC + 1
		segundo_byte=re.search(LD_IX_D_R_2ND, '{0:08b}'.format(Bus().data))		#get next byte
		Z80().offsetPC()														# PC + 1
		register = Register(segundo_byte.group('r')).name								# Get register
		memReqPC()																# Request mem read at PC
		direccion = (Z80().getRegister('H')<< 8) + Z80().getRegister('L')	+ distancia		
		distancia = Bus().data
		Bus().address = direccion														# Put address in Bus
		Bus().data = Z80().getRegister(register)										# Put register data in Bus
		Bus().memUpdate()

		Debug().newFunction('LD (IY+{:02X}H), {}'.format(distancia, register))
	
	#EX DE HL  intercambia los valores de los regitros DE y HL
	elif match := re.search(EX_DE_HL, '{0:08b}'.format(Bus().data)):
	 Z80().offsetPC()	
	 exchangeRegisters('H','D')
	 exchangeRegisters('L','E')	
	 Debug().newFunction('EX HL , DL')

	#EXX
	elif match := re.search(EX_DE_HL, '{0:08b}'.format(Bus().data)):
	 Z80().offsetPC()	
	 exchangeRegisters('B','B\'')
	 exchangeRegisters('C','C\'')	
	 exchangeRegisters('D','D\'')
	 exchangeRegisters('E','E\'')	
	 exchangeRegisters('H','H\'')
	 exchangeRegisters('L','L\'')	
	 Debug().newFunction('EXX ')
	else:
		return False
	return True