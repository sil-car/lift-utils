import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

DATA_PATH = Path(__file__).parent / "data"
SANGO_LIFT = DATA_PATH / "sango" / "sango.lift"
