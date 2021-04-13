from processor.Z80 import Z80
from processor.Memory import Memory

def load(binary_file:str='output/test.z80.bin'):
	memory = {}

	with open(binary_file, 'rb') as fbin:
		address = 0x00
		byte_position = 0
		pc_start = 0x0000
		while byte := fbin.read(1):
			if byte_position == 0:
				pc_start = int.from_bytes(byte,byteorder='little')
			elif byte_position == 1:
				pc_start += int.from_bytes(byte,byteorder='little') << 8
				address = pc_start
			else:
				memory[address] = int.from_bytes(byte, byteorder='little')
				address += 0x01
			byte_position += 1
		Memory().init_memory(memory)
		Z80().setRegister('PC', pc_start)