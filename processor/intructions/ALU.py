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