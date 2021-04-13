from utils.Debug import Debug
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

		def process(self):
			from processor.intructions.general import getInstruction
			return getInstruction()

		def offsetPC(self, offset=1):
			if (offset >> 7) == 1:
				offset = (~offset & 0xFF) + 0x01
				
				self.setRegister('PC', self.getRegister('PC') - offset)
			else:
				self.setRegister('PC', self.getRegister('PC') + offset)
		
		def stackPush(self):
			from processor.Bus import Bus
			Bus().address = self.getRegister('SP')
			Bus().memUpdate()
			self.registers['SP'] -= 1
		
		def stackPop(self):
			from processor.Bus import Bus
			Bus().address = self.getRegister('SP')
			Bus().memReq()
			self.registers['SP'] += 1


		def setRegister(self, register: str, value: int):
			#FIXME: Limit value bytes depending on register type
			if register in self.registers.keys():
				self.registers[register] = value
				Debug().updateReg(register)
			else:
				# TODO: Only print if DEBUG is active
				print(f"{register} is not a valid register")

		def getRegister(self, register):
			return self.registers.get(register, None)

		def setFlags(self, S, Z, H, PV, N, C):
			def set_bit(mask, x):
				"""Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
				flag = self.getRegister('F')
				flag &= ~mask								# Clear the bit indicated by the mask (if x is False)
				if x:
					flag |= mask							# If x was True, set the bit indicated by the mask.
				self.setRegister('F', flag)	# Return the result, we're done.
			set_bit(1<<7,S)
			set_bit(1<<6,Z)
			set_bit(1<<4,H)
			set_bit(1<<2,PV)
			set_bit(1<<1,N)
			set_bit(1<<0,C)

		def getFlag(self, flag):
			if flag == 'S':
				return (self.getRegister('F') & 1<<7) >> 7
			if flag == 'Z':
				return (self.getRegister('F') & 1<<6) >> 6
			if flag == 'H':
				return (self.getRegister('F') & 1<<4) >> 4
			if flag == 'P/V':
				return (self.getRegister('F') & 1<<2) >> 2
			if flag == 'N':
				return (self.getRegister('F') & 1<<1) >> 1
			if flag == 'C':
				return (self.getRegister('F') & 1<<0) >> 0

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
