def write_byte(fout, string: str, base=2, pattern='*', in_bytes=False):
	result = '{0:0{1}X}'.format(int(pattern.replace('*', string), base), 2)

	if in_bytes:
		fout.write(bytes.fromhex(result))
	else:
		fout.write(result)

	return 1


def write_hex(fout, hexstring: str, in_bytes=False):
	return write_byte(fout, hexstring, 16, in_bytes=in_bytes)
