from __future__ import annotations

import sys
from ._about import __banner__


def version():
    sys.stdout.write(f"{__banner__}\n")
    sys.exit(0)
