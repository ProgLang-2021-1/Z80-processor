class Bus:
	class __Bus:
		def __init__(self):
			self.address = 0x0000
			self.data = 0x00
			self.control = {
				'M1': 0,
				'MREQ': 0,
				'IORQ': 0,
				'RD': 0,
				'WR': 0,
				'RFSH': 0,
				'HALT': 0,
				'WAIT': 0,
				'INT': 0,
				'NMI': 0,
				'RESET': 0,
				'BUSRQ': 0,
				'BUSACK': 0
			}

		def setControl(self, control, value):
			if control in self.control.keys():
				self.control[control] = value
			else:
				print(f"{control} is not a valid control key")

		@property
		def data(self):
				return self.__data

		@data.setter
		def data(self, data):
				self.__data = data & 0xFF
				
		@property
		def address(self):
				return self.__address

		@address.setter
		def address(self, address):
				self.__address = address & 0xFFFF
		
	instance = None

	def __new__(cls):	# __new__ always a classmethod
		if not Z80.instance:
			Z80.instance = Z80.__Z80()
		return Z80.instance

	def __getattr__(self, name):
		return getattr(self.instance, name)

	def __setattr__(self, name):
		return setattr(self.instance, name)
