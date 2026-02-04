import sys
import tracemalloc
from pathlib import Path

from tabulate import tabulate

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
import lift_utils  # noqa: E402
from lift_utils import Lexicon  # noqa: E402


def main():
    lift = Path(__file__).parents[1] / "tests" / "data" / "sango" / "sango.lift"  # noqa: E501
    lexicon = Lexicon(lift)
    senses = lexicon.find_all("Adverbe", field="grammatical-info")
    table = []
    for s in senses:
        entry = s.parent_item
        if not isinstance(entry, lift_utils.lexicon.Entry):
            entry = entry.parent_item
        row = [str(entry.lexical_unit), str(s.grammatical_info), s.get_gloss(), s.id]
        table.append(row)
    table.sort(key=lambda x: x[0])  # sort rows by 1st row item: 'gloss' text
    print(tabulate(table))

    # Show memory use, if traced.
    if tracemalloc.is_tracing():
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics("lineno")
        for stat in top_stats[:20]:
            print(stat)


if __name__ == "__main__":
    main()
