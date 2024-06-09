# Setting up Coding Environment

### Python Version
Try to install the latest python - this was written in python 3.12

Significant speed increase past python 3.11

### Installing packages via command line
Call python, could be py, python, or direct path to exe

>py -m pip install -r requirements.txt
>python -m pip install -r requirements.txt
etc...

should automatically install relevant packages

### Virtual Environments
Standard practice if desired

to create 

>py -m venv .venv

to activate

>.venv/Scripts/activate

# Overview

3 Main Classes
- Blade
- Imager
- Fan

### Blade

Handles instantiation of a fan blade, customizable with number of leds, how to space leds, margins on either end

Contains LED positions in real space (x,y) and RGB values for each LED at any given moment

### Imager

Handles image loading and mapping from real space to img space (x,y) -> (imgx, imgy)

Takes an instance of a blade to calculate conversion factor and other relevant data

Currently supports 3 types of image output:
- Inscribed: Full image inside Fan Space
- Circumscribed Top/Bot: Lines Image up such that Top/Bot reach edges of fan, sides may or may not be inside Fan Space
- Circumscribed Left/Right: Lines Image up such that Left/Right reach edges of fan, top/bot may or may not be inside Fan Space

Mapping output indices is can be negative if position is out of image range, this means they are invalid, keep that in mind when setting RGB values

Right now iamges are force loaded as RGB, A channel is scrapped

### Fan

Main class that instantiates blades and an imager

Has function that updates LED values in each blade based on some delta time

Several debug functions to help analyze potential settings and configurations for a prototype

# Simulation
Refer to '.debug/simulation.ipynb' for a jupyter notebook that performs a demo and some data analysis

Try testing with preferred image and image output mode i.e inscribed, etc...

Processes some information dependeont on hardware setup, ideally will tell us info on micro controller

# Miscellanious
Any helper functions that could be useful between files can be found under '/misc'

By importing all the functions onto '/misc/load_misc', it acts as a master file with all the functions in it for easy import

If functions are added make sure to add them to that file for easy access later