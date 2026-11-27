# Makes `import hil_sim` and `import m3sim` work when pytest runs from the module root.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "standins" / "hil"))
