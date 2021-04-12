class Z80:
	class __Z80:
		def __init__(self):
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

		def setRegister(self, register: str, value: int):
			#FIXME: Limit value bytes depending on register type
			if register in self.registers.keys():
				self.registers[register] = value
			else:
				# TODO: Only print if DEBUG is active
				print(f"{register} is not a valid register")

		def getRegister(self, register):
			return self.registers.get(register, None)

		def setRegisters(self, register1, register2, value):
			if register1 in self.register.keys() and register2 in self.register.keys():
				self.registers[register1] = (value >> 8) & 0xFF
				self.registers[register2] = (value & 0xFF)
			else:
				print(f"{register1} and {register2} must be valid registers")

		def getRegisters(self, register1, register2):
			"""Returns a 16-bit number based on which is the union between those registers
			"""
			if register1 not in self.registers.keys() or register2 not in self.registers.keys():
				return None

			return (self.registers[register1] << 8) + self.registers[register2]

	instance = None

	def __new__(cls):  # __new__ always a classmethod
		if not Z80.instance:
			Z80.instance = Z80.__Z80()
		return Z80.instance

	def __getattr__(self, register):
		return getattr(self.instance, register)

	def __setattr__(self, register):
		return setattr(self.instance, register)
