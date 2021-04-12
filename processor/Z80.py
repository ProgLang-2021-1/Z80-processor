class Z80:
	class __Z80:
		def __init__(self):
			# 8 bits registers
			self.registers = {
				'A': 0x00, 'A\'': 0x00,  # Acumulator
				'F': 0x00, 'F\'': 0x00,  # Flags 

				'B': 0x00, 'B\'': 0x00,  # General purpose registers 
				'C': 0x00, 'C\'': 0x00,

				'D': 0x00, 'D\'': 0x00,
				'E': 0x00, 'E\'': 0x00,

				'H': 0x00, 'H\'': 0x00,
				'L': 0x00, 'L\'': 0x00,

				# 8 bits special registers
				'I': 0x00,  # Interrupt 
				'R': 0x00,  # Refresh

				# 16 bits registers
				'IX': 0x0000,  # Registro índice X
				'IY': 0x0000,  # Registro índice Y
				'SP': 0xFFFF,  # Registro 'Stack Pointer' ,
				'PC': 0x0000,  # Registro 'Program Counter',
			}

		instance = None

		def __new__(cls):  # __new__ always a classmethod
			if not Z80.instance:
				Z80.instance = Z80.__Z80()
			return Z80.instance

		def __getattr__(self, name):
			return getattr(self.instance, name)

		def __setattr__(self, name):
			return setattr(self.instance, name)
		
		def setRegister(name, value):
			self.registers[name] = value

		def getRegister(name):
			return self.registers[name]

		def setRegisters(name1, name2, value):
			self.registers[name1] = (value >> 8)<<4
			self.registers[name2] = (value & 0xFF)

		def getRegisters(name1, name2):
			return (self.registers[name1]<<8) + self.registers[name2]