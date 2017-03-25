## Bash CheatSheet


1. Bash is the program on top of `Shell` - you can think of it as a text-based Interface for your computer. As it is text-based, every action :

1) takes small amount of memory, this is very useful to work over the network. Indeed, most of the manual control over servers works through the bash or something similar.

2) Can be easily recorded, combined, stored (as `.sh` files, for example) and re-run.

Also, note that Bash gives you access to many third-party [other] programs, such as python, git, etc, etc.

## Main Commands

- `cd` Moves you to the different directory. For example: 	
	- `cd directory_1/directory2` 
	- `cd ../` (go one level up)
- `pwd` - prints current path
- `ls` - print list of all files and directories in this folder. You can also use `ls -l` to print them as table, with memory, dates, etc.
- `open` {path} - opens current folder or folder you'll add in MAC's Finder
- `man [command]` - opens help (manual) on the command, For example:
	- `man cd`
- `mv [file] [to]` Moves file
- `cp [file] [to]` Copies file
- `rm [file]` Removes file/directory. Attention: you CANT revert this action, it will not move file to the trash bin~
- `mkdir [directory]` creates new directory. For example:
	- `mkdir MyProject`
	- `mkdir MyProject/{inbox,out,code,data}` Creates 4 folders within `MyProject` folder. 
	- `mkdir Countries/{Russia,US,UK,Sweden}/{Capital,Boundaries,Stats}` Creates 3 folders for each of 4 countries within `Countries` folder
- `touch [file]` creates empty file of the given name, For example:
	- `touch project.ai`
	- `touch myProject/README.md`
- `nano README.md` opens file in the simple text editor (nano). Use `Cntrl+O` to save file after edit, `Cntrl+X` to close.
- `head file` will open first lines of the file. *Note: this is made in smart way, so it can open both small and gigantic file with the same effort*. Very handy to lookup csv headers or just take a look at what data is in there.
- `tail file` - similar to head, bit shows last lines.
- `ln -s [source] [link name]` - creates symbolic link (think: icon) for the file that stays somewhere else. All systems will think it is here as well. Works for folders as well.
- `echo text` - print something to the command line.
- `gresp` - filter incoming (through pipe) text and keep only matching lines. For example:
	- `pip freeze | gresp "geopandas"` gets list of all packages installed through `pip` , then filters to those where we have `geopandas` text presented.
	- `ls -l | gresp "2017"` shows only files/folders within given folder with `2017` in the name   

## Also

- `bash [bashfile.sh]` makes bash to run file with the script
- `python [file.py]` makes python to run python code in the file.
- `git pull` gets most recent version of this repo from github
- `git add .` adds all new files / changes to the repository, ready to commit
- `git status` shows current status of the repo
- `git history` shows history of commits
- `git commit -m "My Message"` creates a commit (savepoint)
- `git push` sends last commit to the github repository

## Ticks and Tricks

### 1. Auto-Fill

Any time you write command in bash, you can use tab to give some clues on what should be next. By default, if there is no alternative, it will fill the line down to the moment when it is not sure. If there  are a few options, use tab two times and it will show them.

For example, start writing `ech` and then press TAB - it will fill out `echo ` for you.

This works perfectly for paths as well. try to write with `cd ../`  and press TAB two times.

### 2. Asterix / Wild card

`*`, or wildcard, represent "anything" in any UNIX path. for example, you can try `cd ~/*/` and press tab - it will show ALL the folders within two levels down from the root. You can use the same for filenames, like `ls -l *.ai`, that will show info for all Adobe Illustrator files, or `rm *.txt` to remove ALL the .txt files in the folder

Funny fact: In the ANCII table every char has its number. Number for asterics is `42`. That is one of the explanations for the answer computer gave in `Hitchhiker's guide to Galaxy`: Purpose of Life is * [whatever you want it to be].

### 3. Bash_profile
You can store your variables (called Environment variables) and name your custom functions in the hidden file `~/.bash_profile`. Every time you reboot your system or run `source ~/.bash_profile` system will "learn" those functions and variables. This way you can create a comfortable set of personalized tools (for example, text substitition of `icons` on the desktop). You can open and edit this file with nano:
`nano ~/.bash_profile`.

Here is a part of my `~/.bash_profile`:
```bash
alias ipy="jupyter notebook" # I am lazy to type two words. now I can write only 3 letters.

export AUD="/Users/casy/Dropbox/personal_projects/aud/MD"
alias aud="cd ;cd $AUD" # here I store AUD as variable, and use `aud` command to go to the AUD folder, from anywhere.

export EDITOR='subl -w' # that will make sublime your default text editor. after that, you'll. be able to use `subl ~/.bash_profile`
```

Dont forget to type `source ~/.bash_profile` after you change the file (or reboot instead).

### 4. command (Mac-specific)

if you name your shell script as `script_name.command` instead of `script_name.sh`, mac will run it with terminal any time you click on the file in finder. 