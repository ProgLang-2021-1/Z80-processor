from processor.Bus import Bus
from processor.Z80 import Z80
from processor.intructions.general import *


def jump_call():
	import re

	JR_E 		= rf'00011000(?P<r>{n})'
	JR_C_E 	= rf'00111000(?P<r>{n})'
	JR_NC_E = rf'00110000(?P<r>{n})'
	JR_Z_E	= rf'00101000(?P<r>{n})'
	JR_NZ_E = rf'00100000(?P<r>{n})'

	RET 	 = rf'11001001'
	RET_CC = rf'11(?P<cc>{cc})000'

