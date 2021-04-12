from processor.Bus import Bus
class Memory:
	class __Memory:
		def __init__(self):
			self.memory = {0: 1, 1: 104, 2: 242, 3: 62, 4: 162, 5: 50, 6: 101, 7: 32, 8: 254, 9: 247, 10: 120, 11: 145, 12: 47, 13: 33, 14: 101, 15: 32, 16: 134, 17: 50, 18: 102, 19: 32, 20: 118}

		def setMemory(self):
			#TODO: Reserve some memory for system-specifics
			address = Bus().address
			value = Bus().data
			if 0 <= address <= 0xFFFF and 0 <= value <= 0xFF:
				self.memory[address] = value & 0xFF
			else:
				print("Invalid range")
				return None

		def getMemory(self):
			address = Bus().address
			if 0 <= address <= 0xFFFF:
				Bus().data = self.memory.get(address, 0x00)
			return None

	instance = None

	def __new__(cls):  # __new__ always a classmethod
		if not Memory.instance:
			Memory.instance = Memory.__Memory()
		return Memory.instance

	def __getattr__(self, name):
		return getattr(self.instance, name)

	def __setattr__(self, name):
		return setattr(self.instance, name)
