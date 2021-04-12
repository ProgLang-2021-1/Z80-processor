from processor.Bus import Bus
from processor.Z80 import Z80
from utils.Debug import Debug
from processor.intructions.general import *


def CPU_control():
	import re

	HALT = rf'01110110'

	if match := re.search(HALT, '{0:08b}'.format(Bus().data)):
		Z80().offsetPC()
		Debug().newFunction('HALT')
		# TODO: Stop
		pass
	else:
		return False
	return True

