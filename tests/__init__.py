import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from lift_utils import Lexicon  # noqa: E402

DATA_PATH = Path(__file__).parent / "data"
LEXICON = Lexicon(DATA_PATH / "sango" / "sango.lift")
