import re
from utils.enums import Register, FlagCC
from utils.util import write_hex, write_byte
from assembler.regex import *


def assemble_from_file(input_file, output_file='test.z80.loc'):
	tags = {}
	pc = 0

	with open(f'{input_file}', 'r') as f:
		with open(f'output/{output_file}', 'w') as fout:
			for line in f:

				# Capitalization agnostic
				line = line.upper()

				# The first 2 bytes must be ORG
				if re.match(f'^{line_ending}$', line):
					continue

				if (match := re.match(ORG, line)) and pc == 0:
					pc += write_hex(fout, match.group('n2'))
					pc += write_hex(fout, match.group('n1'))
					fout.write('\n')
					continue

				elif pc == 0 and (re.match(f'^{line_ending}$', line) is None):
					pc += write_hex(fout, '00')
					pc += write_hex(fout, '00')
					fout.write('\n')

				if match := re.match(TAG, line):
					# fout.write(match.group(1) + ':')
					tags[match.group(1)] = pc

				elif match := re.match(LD_R_N, line):  # LD reg, num_8
					pc += write_byte(fout, Register[match.group('r')].value, pattern='0b00*110')
					pc += write_hex(fout, match.group('n'))

				elif match := re.match(LD_R_R, line):  # LD reg, reg
					pc += write_byte(fout, Register[match.group('r1')].value + Register[match.group('r2')].value,
									 pattern='0b01*')

				elif match := re.match(LD_DD_NN, line):  # LD dd, num_16
					pc += write_byte(fout, Register[match.group('dd')].value, pattern='0b00*0001')
					pc += write_hex(fout, match.group('n2'))
					pc += write_hex(fout, match.group('n1'))

				elif match := re.match(LD__NN__A, line):  # LD (nn), A
					pc += write_hex(fout, '32')
					pc += write_hex(fout, match.group('n2'))
					pc += write_hex(fout, match.group('n1'))

				elif match := re.match(CP_R, line):  # SUB reg
					pc += write_byte(fout, Register[match.group('r')].value, pattern='0b10111*')

				elif match := re.match(CPL, line):  # CPL
					pc += write_hex(fout, '2F')

				elif match := re.match(SUB_R, line):  # SUB reg
					pc += write_byte(fout, Register[match.group('r')].value, pattern='0b10010*')

				elif match := re.match(ADD_A_R, line):  # ADD A, reg
					pc += write_byte(fout, Register[match.group('r')].value, pattern='0b10000*')

				elif match := re.match(ADD_A__HL_, line):  # ADD A, (HL)
					pc += write_hex(fout, '86')

				elif match := re.match(HALT, line):  # HALT
					pc += write_hex(fout, '76')

				elif match := re.match(RET_CC, line):
					pc += write_byte(fout, FlagCC[match.group('cc')].value, pattern='0b11*000')

				elif match := re.match(JR_C_TAG, line):
					pc += write_hex(fout, '38')
					fout.write(f'\t{pc}\t{match.group("tag")}')

				elif match := re.match(JR_TAG, line):
					pc += write_hex(fout, '18')
					fout.write(f'\t{pc}\t{match.group("tag")}')

				if match:
					if match.group(1) not in tags.keys():
						fout.write('\n')

	# Output tags position into a file
	# This is helpful when resolving relative positions
	from os.path import basename
	with open(f'output/{basename(output_file)}.tag', 'w') as f_tag_out:
		for tag, pos in tags.items():
			f_tag_out.write(f'{tag}:{pos}\n')