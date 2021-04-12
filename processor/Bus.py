class Bus:
	class __Bus:
		def __init__(self):
			self.address = 0x0000
			self.data = 0x00
			self.control = {
				'M1': False,
				'MREQ': False,
				'IORQ': False,
				'RD': False,
				'WR': False,
				'RFSH': False,
				'HALT': False,
				'WAIT': False,
				'INT': False,
				'NMI': False,
				'RESET': False,
				'BUSRQ': False,
				'BUSACK': False
			}

		def getControl(self, control: str):
			if control in self.control.keys():
				return self.control[control]
			return None

		def setControl(self, control: str, value: bool = False):
			if control in self.control.keys():
				self.control[control] = value
			else:
				print(f"{control} is not a valid control key")

		@property
		def data(self):
			return self.__data

		@data.setter
		def data(self, data):
			if 0 <= data <= 0xFF:
				self.__data = data

		@property
		def address(self):
			return self.__address

		@address.setter
		def address(self, address):
			if 0 <= address <= 0xFFFF:
				self.__address = address
		
	instance = None

	def __new__(cls):	# __new__ always a classmethod
		if not Z80.instance:
			Z80.instance = Z80.__Z80()
		return Z80.instance

	def __getattr__(self, name):
		return getattr(self.instance, name)

	def __setattr__(self, name):
		return setattr(self.instance, name)
