# Z80 emulator

## Project struct

```
Repo
├─── assembler
│   ├─── __init__.py
│   └─── assembler.py
├─── linker
│   ├─── __init__.py
│   └─── linker.py
├─── loader
│   ├─── __init__.py
│   └─── loader.py
├─── processor
│   ├─── __init__.py
│   ├─── Z80.py
│   ├─── Buses.py
│   ├─── Memory.py
│   └─── instructions
│           ├─── __init__.py
│           ├─── ALU.py
│           ├─── load_exchange.py
│           ├─── rotate_shift.py
│           ├─── bit_manipulation.py
│           ├─── jump_call.py
│           └─── CPU_control.py
├─── utils
│   ├─── __init__.py
│   ├─── enums.py
│   ├─── cli.py
│   ├─── Debug.py 
│   └─── util.py
├─── CLI
│   ├─── __init__.py
│   └─── cli.py
├─── __init__.py
├─── main.py
├─── .gitignore
└─── README.md
```
