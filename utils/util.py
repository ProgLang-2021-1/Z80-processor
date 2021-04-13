def write_byte(fout, string: str, base=2, pattern='*'):
	result = '{0:0{1}X}'.format(int(pattern.replace('*', string), base), 2)
	# fout.write(bytes.fromhex(result))
	fout.write(result)
	return 1


def write_hex(fout, hexstring: str):
	return write_byte(fout, hexstring, 16)
