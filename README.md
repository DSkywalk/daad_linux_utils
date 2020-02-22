# daad utils

Some utils writen in python for [daad/dsf](https://github.com/daad-adventure-writer). Also includes my linux [DEVKIT](https://github.com/DSkywalk/daad_utils/devkit) to build AMSTRAD CPC Adventures :+1:

# predrf

Preprocess DSF files.

Usage:

    predrf.py game.dsf -o build/game-processed.dsf

## new include token

Now you can add **#include** to your DSF files so their the contents of the *included file* are imported into your final DSF file.

### Example

*in main DSF file*

    ;------------------------------------------------------------------------------
    #include "sections/game-con.dsf"
    ;------------------------------------------------------------------------------

*sections/game-con.dsf contains*

    ;------- Connections
    /CON
    /0
    /1

*in main DSF file after apply*

    ;------------------------------------------------------------------------------
    ;------- Connections
    /CON
    /0
    /1
    ;------------------------------------------------------------------------------

## allow line endings in LTX section (like old SCE file)

*it converts*

    /LTX
    /0 "Location example text like this
    without having to use special tokens,
    as was done when using SCE
    bla bla bla"

*into*

    /LTX
    /0 "Location example text like this#nwithout having to use special tokens,#nas was done when using SCE#nbla bla bla"
