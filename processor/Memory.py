class Memory:
	class __Memory:
		def __init__(self):
			memory = {}

		def setMemory(self, address: int, value: int):
			#TODO: Reserve some memory for system-specifics
			if 0 <= address <= 0xFFFF and 0 <= value <= 0xFF:
				self.memory[address] = value & 0xFF
			else:
				print("Invalid range")
				return None

		def getMemory(self, address: int):
			if 0 <= address <= 0xFFFF:
				return self.memory.get(address, 0x00)
			return None

	instance = None

	def __new__(cls):  # __new__ always a classmethod
		if not Z80.instance:
			Z80.instance = Z80.__Z80()
		return Z80.instance

	def __getattr__(self, name):
		return getattr(self.instance, name)

	def __setattr__(self, name):
		return setattr(self.instance, name)
