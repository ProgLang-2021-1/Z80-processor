from processor.Z80 import Z80
from utils.Debug import Debug
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
		def memReq(self):
			from processor.Memory import Memory

			Debug().newLog('Memory read request')
			Memory().getMemory()
		
		def memUpdate(self):
			from processor.Memory import Memory

			Debug().newLog('Memory write request')
			Memory().setMemory()


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
				Debug().newLog('\tNew data bus entry: {:02X}'.format(data))

		@property
		def address(self):
			return self.__address

		@address.setter
		def address(self, address):
			if 0 <= address <= 0xFFFF:
				self.__address = address
				Debug().newLog('\tNew address bus entry: {:04X}'.format(address))
		
	instance = None

	def __new__(cls):	# __new__ always a classmethod
		if not Bus.instance:
			Bus.instance = Bus.__Bus()
		return Bus.instance

	def __getattr__(self, name):
		return getattr(self.instance, name)

	def __setattr__(self, name):
		return setattr(self.instance, name)
