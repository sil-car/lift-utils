import sys
import tracemalloc
from pathlib import Path
from tabulate import tabulate

sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from lift_utils import Lexicon  # noqa: E402


def main():
    lifts = [
        '~/lift/Bhogoto FLEx LIFT export/Bhogoto FLEx LIFT export.lift',
        '~/lift/Gbagiri FLEx LIFT export/FLEx LIFT export.lift',
        '~/lift/Gbanu FLEx LIFT export/FLEx LIFT export.lift',
    ]
    lexicons = [Lexicon(lift) for lift in lifts]
    table = []
    for n in range(1, 1701):  # CAWL number range
        cawl = f"{n:04d}"
        row = [cawl]
        for lex in lexicons:
            lu = None
            item = lex.find(cawl, field='CAWL', match_type='exact')
            if item and item.id:
                parent = lex.get_item_parent_by_id(item.id)
                if parent:
                    lu = parent.lexical_unit
            row.append(lu)
        table.append(row)
    print(tabulate(table))

    # Show memory use, if traced.
    if tracemalloc.is_tracing():
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        for stat in top_stats[:20]:
            print(stat)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
