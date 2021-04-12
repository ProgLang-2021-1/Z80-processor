class Memory:
	class __Memory:
		def __init__(self):
            memory = {}

		instance = None

		def __new__(cls):  # __new__ always a classmethod
			if not Z80.instance:
				Z80.instance = Z80.__Z80()
			return Z80.instance

		def __getattr__(self, name):
			return getattr(self.instance, name)

		def __setattr__(self, name):
			return setattr(self.instance, name)
		
		def setMemory(addr, value):
			self.memory[addr] = value

		def getMemory(addr):
			return self.memory[addr]
