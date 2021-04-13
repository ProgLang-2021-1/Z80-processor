class Debug:
	class __Debug:
		def __init__(self):
			self.log = ""
			self.lastFunction = ""
			self.register = []
			self.memory = []

		def newFunction(self, name):
			self.lastFunction = name
			self.newLog(f'Function detected: {name}\n')
		
		def newLog(self, message):
			self.log += message + "\n"
		
		def updateReg(self, name):
			self.register.append(name)
		
		def updateMem(self, addr):
			self.memory.append(addr)

	instance = None

	def __new__(cls):  # __new__ always a classmethod
		if not Debug.instance:
			Debug.instance = Debug.__Debug()
		return Debug.instance

	def __getattr__(self, register):
		return getattr(self.instance, register)

	def __setattr__(self, register):
		return setattr(self.instance, register)