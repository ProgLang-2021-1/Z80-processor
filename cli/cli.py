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
			assemble_from_file(f'examples/{filename}')
		elif proccess == 'l':
			console.input(prompt='====> output/test.z80.loc\t')
			console.input(prompt='====> output/test.z80.loc.tag\t')
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
					console.input(prompt='====> output/test.z80.bin\t')
					load('output/test.z80.bin')
					cls()
				x = printprocessor()
			if x == 'q':
				break
			cls()
			get_title_module()
		proccess = print_main_options()
	cls()
	get_title_module()
	console.print('Z80 Closed', justify='center')
