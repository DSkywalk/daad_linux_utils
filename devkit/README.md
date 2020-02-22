# devkit

My personal linux daad devkit, but you could easily adapt this to your env :+1:

Please download lastest binaries from the original repo:

   https://github.com/daad-adventure-writer/DRC/wiki#DOWNLOAD

## how to use
First edit activate.sh and modify DAADDEV to your devkit path.
    
and finally to load the enviroment:
    
    source devkit/activate.sh
    
you could add this build environment to Visual Code adding to your workspace settings:

    "terminal.integrated.shellArgs.linux": ["--init-file", "path/to/your/devkit/activate.sh"],

