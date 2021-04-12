from rich.console import Console
from rich.table import Table
from rich import box
from rich.box import Box
import os
import platform
import re

from processor.Z80 import Z80
from processor.Memory import Memory
from processor.Bus import Bus
from utils.Debug import Debug

console = Console()

CUSTOM_ROUNDED: Box = Box(
    """\
╭──╮
│  │
├──┤
│  │
├──┤
├──┤
│  │
╰──╯
"""
)

def cls():
	if platform.system() == 'Windows':
		return os.system('cls')
	return os.system('clear')


def get_title_module():
	console.print(r'[bold white]╭─────────────────────────────────────────────────────────╮[/bold white]', justify='center')
	console.print(r'[bold white]|             __________ ______ _______                   |[/bold white]', justify='center')
	console.print(r'[bold white]|             \____    //  __  \\   _  \                  |[/bold white]', justify='center')
	console.print(r'[bold white]|               /     / >      </  /_\  \                 |[/bold white]', justify='center')
	console.print(r'[bold white]|              /     /_/   --   \  \_/   \                |[/bold white]', justify='center')
	console.print(r'[bold white]|             /_______ \______  /\_____  /                |[/bold white]', justify='center')
	console.print(r'[bold white]|                     \/      \/       \/                 |[/bold white]', justify='center')
	console.print(r'[bold white]| ___________             .__          __                 |[/bold white]', justify='center')
	console.print(r'[bold white]| \_   _____/ _____  __ __|  | _____ _/  |_  ___________  |[/bold white]', justify='center')
	console.print(r'[bold white]|  |    __)_ /     \|  |  \  | \__  \\   __\/  _ \_  __ \ |[/bold white]', justify='center')
	console.print(r'[bold white]|  |        \  Y Y  \  |  /  |__/ __ \|  | (  <_> )  | \/ |[/bold white]', justify='center')
	console.print(r'[bold white]| /_______  /__|_|  /____/|____(____  /__|  \____/|__|    |[/bold white]', justify='center')
	console.print(r'[bold white]|         \/      \/                \/                    |[/bold white]', justify='center')
	console.print(r'[bold white]╰─────────────────────────────────────────────────────────╯[/bold white]', justify='center')


def register(name1, name2 = '', isflag = False, numtype = 'X16'):
	if name2 != '':
		return ('[bold blue]{0:<2}{1:<2}[/bold blue] = {{{0}:02X}} {{{1}:02X}}').format(name1, name2).format(**Z80().registers)
	elif numtype == 'X8':
		return ('[bold blue]{0:<4}[/bold blue] = {{{0}:02X}}').format(name1).format(**Z80().registers)
	elif numtype == 'b8':
		return ('[bold blue]{0:<4}[/bold blue] = {{{0}:08b}}').format(name1).format(**Z80().registers)
	elif isflag:
		return ('[bold blue]{0:<2}[/bold blue] = ').format(name1)+'   '.join('{{{0}:08b}}'.format(name1).format(**Z80().registers))
	return ('[bold blue]{0:<4}[/bold blue] = {{{0}:04X}} ').format(name1).format(**Z80().registers)

def get_register_module():
	table = Table(title='Z80', width=70, show_header=False, box=CUSTOM_ROUNDED)

	table.add_column(' ', justify='center')
	table.add_column(' ', justify='center')

	table.add_row('[bold green]Program Control[/bold green]', '[bold green]Flag Bits[/bold green]')
	table.add_row(' ', '[bold cyan]     S   Z   -   H   -  P/V  N   C[/bold cyan]')
	table.add_row(register('PC'),register('F', isflag=True))
	table.add_row(register('SP'),register('F\'', isflag=True))
	table.add_row('[bold green]General Registers[/bold green]', '[bold green]Alternate Registers[/bold green]')
	table.add_row(register('A','F'),register('A\'','F\''))
	table.add_row(register('B','C'),register('B\'','C\''))
	table.add_row(register('D','E'),register('D\'','E\''))
	table.add_row(register('H','L'),register('H\'','L\''))
	table.add_row('[bold green]Index Registers[/bold green]', '[bold green]Hardware Control[/bold green]')
	table.add_row(register('IX'),register('I','R'))
	table.add_row(register('IY'),'')
	return table

def check_memory_row(row):
	mem = ''
	for j in range(0, 16):
		if (row + j) in Memory().memory.keys():
			if (row + j) == Z80().getRegister('PC'):
				mem += '[bold red]{:02X} [/bold red]'.format(Memory().memory[row + j])
			else:
				mem += '{:02X} '.format(Memory().memory[row + j])
		else:
			if (row + j) == Z80().registers['PC']:
				mem += '[bold red]{:02X} [/bold red]'.format(0)
			else:
				mem += '{:02X} '.format(0)
	return mem
def get_memory_module():
	table = Table(title='Memory', width=70, box=CUSTOM_ROUNDED)
	table.add_column('[bold blue]Offset[/bold blue]', justify='right')
	table.add_column('[bold green]00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F [/bold green]', justify='left')
	for i in range(0, 0xFFF):
		if match := re.search(r'((?!(00 ){16})((\[.*\])?[0-9A-F]{2} (\[/.*\])?){16})',check_memory_row(i<<4)):   
			table.add_row('[bold green]{:04X}[/bold green]'.format(i<<4),match.group(0))
	return table

def get_bus_module():
	table = Table(title='Buses', width=70, box=CUSTOM_ROUNDED)
	table.add_column('[bold green]Data Bus[/bold green]', justify='center')
	table.add_column('[bold green]Address Bus[/bold green]', justify='center')
	table.add_row('{:02X}'.format(Bus().data),'{:04X}'.format(Bus().address))
	return table

def print_main_options():
	console.print('[{0}r{1}]un [{0}c{1}]ompile [{0}a{1}]ssemble [{0}q{1}]uit'.format('[bold green]','[/bold green]'),justify='center')
	return console.input(prompt='====> ')

def printprocessor():
	console.print('Last processed function = ',Debug().lastFunction, justify='center')
	console.print(get_register_module(), justify='center')
	console.print(get_bus_module(), justify='center')
	console.print(get_memory_module(), justify='center')
	console.print('[{0}s{1}]tep [{0}p{1}]rocess [{0}l{1}]oad memory [{0}b{1}]ack [{0}q{1}]uit'.format('[bold green]','[/bold green]'),justify='center')
	return console.input(prompt='====> ')
