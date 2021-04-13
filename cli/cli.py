from rich.console import Console
from rich.table import Table
from rich import box
import os
import platform
import re

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
			console.print('Not implemented yet', justify='center')
			# console.print('Please enter file name', justify='center')
			# filename = console.input(prompt='====> ')
			# assemble(filename)
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
					console.print('Not implemented yet', justify='center')
					# loadmemory()
					# Z80().currentfunction = 'Instructions Loaded in Memory'
				x = printprocessor()
			if x == 'q':
				break
			cls()
			get_title_module()
		proccess = print_main_options()
	cls()
	get_title_module()
	console.print('Z80 Closed', justify='center')
