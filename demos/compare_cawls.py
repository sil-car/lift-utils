import multiprocessing as mp
import sys
import tracemalloc
from pathlib import Path

from tabulate import tabulate

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from lift_utils.demos import lexical_units_from_lift


def main():
    lifts = [
        "~/lift/Bhogoto FLEx LIFT export/Bhogoto FLEx LIFT export.lift",
        "~/lift/Gbagiri FLEx LIFT export/FLEx LIFT export.lift",
        "~/lift/Gbanu FLEx LIFT export/FLEx LIFT export.lift",
    ]
    cawls = [f"{n:04d}" for n in range(1, 1701)]  # CAWL numbers, 0001 to 1700
    with mp.Pool(3) as p:  # use multiprocessing to handle 3 files at once
        lus_by_lex = p.starmap(
            lexical_units_from_lift, ((lift, cawls) for lift in lifts)
        )  # noqa: E501
    table = zip(cawls, *lus_by_lex)  # convert "columns" to "rows" for table
    print(tabulate(table))

    # Show memory use, if traced.
    if tracemalloc.is_tracing():
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics("lineno")
        for stat in top_stats[:20]:
            print(stat)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
