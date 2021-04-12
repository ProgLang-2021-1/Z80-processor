from processor.Z80 import Z80
from processor.Bus import Bus

non_HL_ = r'(?!110)([01]{3})'
cc = r'[01]{3}'
n = r'[01]{8}'

def memReqPC(should_increment=True):
	if Z80().getRegister('PC') != None:
		Bus().address = Z80().getRegister('PC')
		Bus().memReq()
		if should_increment:
			Z80().offsetPC()