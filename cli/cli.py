from rich.console import Console
from rich.table import Table
from rich import box
import os
import platform
import re

from assembler.assembler import assemble_from_file
from linker.linker import link
from loader.loader import load

from utils.cli import *

def runcli():
	if not os.path.exists('output'):
		os.makedirs('output')
	cls()
	get_title_module()
	proccess = print_main_options()

	while proccess != 'q':
		cls()
		get_title_module()

		if proccess == 'c':
			console.print('Not implemented yet', justify='center')
		elif proccess == 'a':
			filename = console.input(prompt='====> examples/')
			filename = filename if ".z80.asm" in filename else f'{filename}.z80.asm'
			assemble_from_file(f'examples/{filename}')
			console.print(f'Assembling: examples/{filename}')
			console.print('File created at: output/test.z80.loc')
			console.print('File created at: output/test.z80.loc.tag')
		elif proccess == 'l':
			console.print('Linking from: output/test.z80.loc')
			console.print('Linking from: output/test.z80.loc.tag')
			console.input(prompt='Press Enter to confirm...')
			link('output/test.z80.loc', 'output/test.z80.loc.tag')
		elif proccess == 'al':
			filename = console.input(prompt='====> examples/')
			filename = filename if ".z80.asm" in filename else f'{filename}.z80.asm'
			assemble_from_file(f'examples/{filename}')
			console.print(f'Assembling: examples/{filename}')
			console.print('File created at: output/test.z80.loc')
			console.print('File created at: output/test.z80.loc.tag')
			console.print('Linking from: output/test.z80.loc')
			console.print('Linking from: output/test.z80.loc.tag')
			link('output/test.z80.loc', 'output/test.z80.loc.tag')
		elif proccess == 'r':
			cls()
			x = printprocessor()
			while x != 'q' and x != 'b':
				cls()
				if x == 's':
					Z80().process()
				elif x == 'p':
					while (Z80().process()):
						pass
				elif x == 'l':
					printprocessor(False)
					load('output/test.z80.bin')
					cls()
					console.print('Memory loaded from output/test.z80.bin')
				x = printprocessor()
			if x == 'q':
				break
			cls()
			get_title_module()
		proccess = print_main_options()
	cls()
	get_title_module()
	console.print('Z80 Closed', justify='center')
