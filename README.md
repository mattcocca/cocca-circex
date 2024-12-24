# Cocca CircEx

Tinkering with an Adafruit **Circ**uit Playground **Ex**press board

This repo contains multiple projects which can be run on the Adafruit Circuit Playground Express board, mostly utilizing CircuitPython, mostly for learning about the CircuitPython/Micropython as well as hopefully having some fun!

## Project List
**DataLogger** - Read from all the onboard sensors, and maybe eventually log them to a file


## Organization
Each project should have it's own directory at the top level of the repository which contains a `README.md` detailing the purpose and use of the project as well as any relevant notes, it's code (`code.py`, `code.txt`, `main.py`, `main.txt`, or other files if it is not CircuitPython), optionally a `lib` directory can be created for storage of micropython libraries/modules that are relevant to a particular project.

Tools and scripts that are useful for development can be stored in the `build` directory

**Example file tree**
cocca-circex
├─ README.md (the file you're reading right now)
├─ build
│  ├── README.md
│  └── dev-scripts 
└─ Project
   ├── README.md
   ├── code.py
   └── lib
       ├── library_code.py 
       └── library_code.mpy
