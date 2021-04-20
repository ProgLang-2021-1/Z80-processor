# Z80 emulator

## Instrucciones para su ejecución
1. Clonar el repositorio o descargar el archivo .zip
2. Ubíquese dentro del directorio creado y ejecute una ventana de comandos allí ingrese lo siguiente:

    a. pip install -r requirements.txt (se recomienda el uso de una virtual enviroment)

    b. python main.py

verá entonces:
![z80_Start](https://i.imgur.com/cX3t7Qr.png)
En el cli tenemos las siguientes opciones que se deben ejecutar en el siguiente orden
* assemble [a]: escriba a, luego enter
  se le pedirá el nombre del programa *.z80.asm, en nuestro caso usaremos e_div.z80.asm

     El nombre puede o no tener la extensión
     este paso genera los archivos relocalizables .loc y .tag
     ![z80_assemble](https://i.imgur.com/9RYokW0.png)
luego de cargar el archivo proceda a generar el enlazamiento

* Link [L]: a partir de los archivos generados por el programa en el paso anterior resuelve las posiciones relocalizables

     ![z80_link](https://i.imgur.com/Txaq1lQ.png)
una vez ensamblado y enlazado, se efectúa la carga del programa en la memoria, para ello seguiremos en:

* Run [r]: le mostrará la situación actual del sistema en 3 partes principales:

    Z80 cuenta con todos los registros

    Buses muestra el último dato que se encuentra en cada bus al finalizar cada proceso

    Memory muestra aquellas posiciones de memoria que se encuentren inicializadas o referenciadas ya sea por PC o SP

    ![z80_run](https://i.imgur.com/Afouph2.png)
    En la imagen anterior se puede notar cómo la memoria se encuentra vacía, por lo que una vez más deberá ingresar “l” para cargar definitivamente el programa en memoria:

    * Load [l]: carga el programa ensamblado y enlazado
    ![z80_load](https://i.imgur.com/Yz8DBYA.png)

    Para procesar cuenta con 2 opciones

    * Step [s]: una visualización paso a paso de cada las instrucciones, procesa la instrucción actual en PC

    * Process [p]: ejecuta todo el programa hasta que finalize ya sea porque no existe la instruccion en el PC o el programa llego a la instruccion HALT.
    ![z80_process](https://i.imgur.com/i4Y6qb2.png)

    Al terminar de procesar se resaltará cada cambio que suceda en el procesador.

## Project struct

```
Repo
├─── assembler
│   ├─── __init__.py
│   └─── assembler.py
├─── linker
│   ├─── __init__.py
│   └─── linker.py
├─── loade
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

