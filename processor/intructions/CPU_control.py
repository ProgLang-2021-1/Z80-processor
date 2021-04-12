from processor.Bus import Bus
from processor.Z80 import Z80
from processor.intructions.general import *


def CPU_control():
	import re

	HALT = rf'01110110'

	memReqPC(should_increment=False)
	if match := re.search(HALT, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		# Z80().currentfunction = 'HALT'
		# TODO: Stop
		pass

