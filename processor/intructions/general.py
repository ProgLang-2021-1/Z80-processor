from processor.Z80 import Z80
from processor.Bus import Bus
from utils.Debug import Debug

non_HL_ = r'(?!110)([01]{3})'
cc = r'[01]{3}'
n = r'[01]{8}'

def memReqPC(should_increment=True):
	if Z80().getRegister('PC') != None:
		Bus().address = Z80().getRegister('PC')
		Bus().memReq()
		if should_increment:
			Z80().offsetPC()

def getInstruction():
	from processor.intructions.ALU import alu
	from processor.intructions.bit_manipulation import bit_manipulation
	from processor.intructions.CPU_control import CPU_control
	from processor.intructions.jump_call import jump_call
	from processor.intructions.load_exchange import load_exchange
	from processor.intructions.rotate_shift import rotate_shift
	memReqPC(should_increment=False)
	if (alu() or bit_manipulation() or CPU_control() or jump_call() or load_exchange() or rotate_shift()):
		return True
	Debug().newFunction('No Instruction found in PC')
	return False