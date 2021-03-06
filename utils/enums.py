from enum import Enum

class Register(Enum):
	B = '000'
	C = '001'
	D = '010'
	E = '011'
	H = '100'
	L = '101'
	A = '111'
	BC = '00'
	DE = '01'
	HL = '10'
	SP = '11'
	AF = '11'


class Flags(Enum):
	S = 1 << 7
	Z = 1 << 6
	H = 1 << 4
	P = 1 << 2
	N = 1 << 1
	C = 1 << 0

class FlagCC(Enum):
	NZ = '000'
	Z =  '001'
	NC = '010'
	C =  '011'
	PO = '100'
	PE = '101'
	P =  '110'
	M =  '111'
