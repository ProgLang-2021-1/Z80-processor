from enum import Enum


class Register(Enum):
	A = '111'
	B = '000'
	C = '001'
	D = '010'
	E = '011'
	H = '100'
	L = '101'
	BC = '00'
	DE = '01'
	HL = '10'
	SP = '11'
	AF = '11'