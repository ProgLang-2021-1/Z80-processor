from processor.Z80 import Z80
from processor.Bus import Bus
from processor.Memory import Memory

if __name__ == '__main__':
	for i in range (0,10):
		Z80().process()
		print(hex(Bus().data),hex(Bus().address))
	print(Z80().registers)
	print(Memory().memory,'****')