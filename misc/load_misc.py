'''
Master file with all misc functions for easy Python import
'''

#Allows script to run locally, adds entire directory to path
from pathlib import Path
import sys
root = Path(__file__).parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root.parent) not in sys.path:
    sys.path.append(str(root.parent))

from misc.conversion import rads, degs
from misc.HiddenPrints import HiddenPrints
