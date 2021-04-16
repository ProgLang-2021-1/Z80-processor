from processor.Bus import Bus
from processor.Z80 import Z80
from utils.Debug import Debug
from processor.intructions.general import *
from utils.enums import Register


def xor_a_number(number):
	Z80().registers['A']=Z80().registers['A'] ^ number

def add_a_number(number, update=True):
	"""
	Binary addition between register A and [number_8|reg|indexed|(HL)].

	The result is stored in register A
	"""
	acumulator = Z80().registers['A']
	result = acumulator + number

	carry = result > 0xFF or result < 0

	# if they have the same sign, and the result has the opposite sign
	overflow = ((acumulator & 0x80) == (number & 0x80)) and ((acumulator & 0x80) != (result & 0x80))
	halfcarry = ((acumulator & 0xF) + (number & 0XF)) > 0xF

	if update:
		Z80().setRegister('A', result & 0xFF)
	Z80().setFlags(result < 0, result == 0, halfcarry, overflow, False, carry)

def sub_a_number(number:int, update=True):
	"""
	Substracts number from register A and updates flags.
	Register A is only updated if {update} is set to true

	:param number number to substract register A with
	:param update true if register should be updated
	"""
	acumulator = Z80().getRegister('A')
	result = acumulator - number

	# borrow = result > 0xFF or result < 0
	borrow = number > acumulator

	halfcarry = (number & 0xF) > (acumulator & 0xF)
	# If their signs are different and the result has the same sign as the subtrahend.
	overflow = ((acumulator & 0x80) != (number & 0x80)) and ((number & 0x80) == (result & 0x80))
	
	if update:
		Z80().setRegister('A', result & 0xFF)

	Z80().setFlags(result < 0, result == 0, halfcarry, overflow, True, borrow)

def alu():
	import re
	
	CP_N = rf'11111110'
	CP_R = rf'10111(?P<r>{non_HL_})'
	CP__HL_ = rf'10111110'


	CPL = rf'00101111'
	SUB_R = rf'10010(?P<r>{non_HL_})'
	ADD_A_R = rf'10000(?P<r>{non_HL_})'
	ADD_A__HL_ = rf'10000110'

	INC = rf'00(?P<r>{non_HL_})100'
	
	NEG = rf'01000100'

	XOR_R = rf'10101(?P<r>{non_HL_})'
	XOR_N = rf'11101110'
	XOR__HL__=rf'10101110'


	# CP N    compara el valor N y el acumulador  A-N
	if match := re.search(CP_N, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		memReqPC()
		number = Bus().data
		sub_a_number(number, update=False)
		Debug().newFunction('CP {:02X}H'.format(number))

	# CP R    compara el valor en el registro R y el acumulador  A-(R)
	elif match := re.search(CP_R, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		register = Register(match.group('r')).name
		number = Z80().getRegister(register)
		sub_a_number(number, update=False)
		Debug().newFunction(f'CP {register}')

	# CP (HL)    compara el valor en la direccion en memoria HL R y el acumulador  A-(HL)
	elif match := re.search(CP__HL_, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		
		Bus().address = Z80().getRegisters('H','L')
		Bus().memReq()	
		number=Bus().data		
		sub_a_number(number, update=False)
		Debug().newFunction('CP (HL)')


	# CPL one's complement
	elif match := re.search(CPL, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		Z80().setRegister('A', ~ Z80().getRegister('A') & 0XFF)
		Debug().newFunction('CPL')


	# Sub reg
	elif match := re.search(SUB_R, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		register = Register(match.group('r')).name
		sub_a_number(Z80().getRegister(register))
		Debug().newFunction(f'SUB {register}')
	
	# Add acumulator reg
	elif match := re.search(ADD_A_R, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		register = Register(match.group('r')).name
		add_a_number(Z80().getRegister(register))
		Debug().newFunction(f'ADD A, {register}')
	
	# Add acumulator (HL)
	elif match := re.search(ADD_A__HL_, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		Bus().address = Z80().getRegisters('H','L')
		Bus().memReq()
		add_a_number(Bus().data)
		Debug().newFunction('ADD A, (HL)')
		# Z80().currentfunction = 'ADD A, (HL)'

	elif match := re.search(INC, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		register = Register(match.group('r')).name
		value = Z80().getRegister(register)+1
		Z80().setRegister(register, value)
		Z80().setFlags(value & 0x80 == 0x80, value, value & 0x40 == 0x40, value == 0x7F, False, Z80().getFlag('C'))
		Debug().newFunction(f'INC {register}')
	
	elif match := re.search(PREFIX_ED, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		memReqPC()
		if match := re.search(NEG, '{0:08b}'.format(Bus().data)):
			value = Z80().getRegister('A')
			result = (~value) + 1
			Z80().setRegister('A',result & 0xFF)
			Z80().setFlags((result & 0xFF) >> 7, result == 0, (value & 0xF) > 0, value == 0x80, True, value != 0)
			Debug().newFunction(f'NEG')
			
	

	# XOR R , xor entre A y el registro R se guarda en A
	elif match := re.search(XOR_R, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		xor_a_number(Z80().getRegister(Register(match.group('r')).name))

	# XOR N , xor entre A y el numero n, se guarda en A
	elif match := re.search(XOR_N, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		Bus().memReq()
		value=Bus().data
		xor_a_number(value)
		# XOR N , xor entre A y el numero n, se guarda en A
	elif match := re.search(XOR__HL__, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		Bus().address=Z80().getRegisters('H','L')
		memReqPC()
		value=Bus().data
		xor_a_number(value)
	
	
	else:
		return False
	return True