from processor.Z80 import Z80
from processor.Bus import Bus
from utils.Debug import Debug
from processor.Memory import Memory

if __name__ == '__main__':
	for i in range (0,10):
		Z80().process()
	print(Debug().log)