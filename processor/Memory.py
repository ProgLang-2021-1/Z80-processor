from processor.Bus import Bus
from utils.Debug import Debug
class Memory:
	class __Memory:
		def __init__(self):
			self.memory = {}

		def init_memory(self, memory):
			self.memory = memory
		def setMemory(self):
			#TODO: Reserve some memory for system-specifics
			address = Bus().address
			value = Bus().data

			if 0 <= address <= 0xFFFF and 0 <= value <= 0xFF:
				self.memory[address] = value & 0xFF
				Debug().updateMem(address)
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
