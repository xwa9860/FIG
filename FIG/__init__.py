import sys
from pathlib import Path # if you haven't already done so
root = str(Path(__file__).resolve().parents[1])
# Or
#   from os.path import dirname, abspath
#   root = dirname(dirname(abspath(__file__)))
sys.path.append(root)
