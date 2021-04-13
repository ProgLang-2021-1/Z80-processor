from utils.util import write_hex

def tags_to_dict(filename_tags)->dict:
	"""Reads file and returns a dictionary with the tags detected
	"""
	tags = {}
	with open(f'{filename_tags}', 'r') as f:
		for line in f:
			line =  line.rstrip()
			if len(line) > 0:
				tag, position = line.split(':')
				tags[tag] = int(position)
	return tags

def link(filename_loc:str, filename_tags:str, output_file='test.z80.bin'):
	org = None
	bytes_written = 0
	with open(filename_loc, 'r') as f:
		with open(f'output/{output_file}', 'wb') as fout:
			tags = tags_to_dict(filename_tags)
			for line in f:
				line = line.rstrip()

				# if tag is detected
				if len(match := line.split('\t')) == 3:
					instruction, pc, tag = match

					if instruction != 'CD':
						# e must is expresed as byte in two's complement
						e = '{:02X}'.format((~(int(pc) - tags[tag]) + 1 ) & 0xFF)
						line = instruction + e
					else:
						addr = '{:04X}'.format(tags[tag]+org)
						line = instruction + addr[2:] + addr[:2]

				while len(line) > 0:
					byte = line[:2]
					line = line[2:]
					if bytes_written == 0:
						org = int(f'0x{line}{byte}', 16)
					write_hex(fout, byte, True)
					bytes_written +=2
