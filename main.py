from assembler.assembler import assemble_from_file
from linker.linker import link

if __name__ == '__main__':
	assemble_from_file('examples/euclides.z80.asm')
	link('output/test.z80.loc','output/test.z80.loc.tag')
