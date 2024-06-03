"""Create documents in /doc folder using pdoc
"""

import os
import shlex
import shutil
import sys
from pathlib import Path

from pdoc.__main__ import cli

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    shutil.rmtree("doc", ignore_errors=True)
    cmd = "pdoc pycnnum test -d google -o doc --math"
    sys.argv = shlex.split(cmd)
    cli()
