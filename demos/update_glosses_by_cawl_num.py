import sys
import tracemalloc
from pathlib import Path
# from tabulate import tabulate

sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
import lift_utils  # noqa: E402
from lift_utils import Lexicon  # noqa: E402


def main():
    gbanu_lift = '~/lift/Gbanu FLEx LIFT export/FLEx LIFT export.lift'
    sango_lift = Path(__file__).parents[1] / 'tests' / 'data' / 'sango' / 'sango.lift'  # noqa: E501

    # Get Sango lexical-unit text from Sango LIFT.
    sango_glosses = {f"{n:04d}": None for n in range(1, 1701)}
    sango_lex = Lexicon(sango_lift)
    for cawl in sango_glosses.keys():
        glosses = []
        senses = sango_lex.find_all(cawl, field='CAWL', match_type='exact')
        # if len(senses) > 1:
        #     print(f"Warning")
        for s in senses:
            entry = sango_lex.get_item_parent_by_id(s.id)
            if not isinstance(entry, lift_utils.lexicon.Entry):
                entry = sango_lex.get_item_parent_by_id(entry.id)
            glosses.append(entry.lexical_unit.get_form_by_lang('sg'))
        # if len(glosses) > 1:
        #     # continue
        if glosses and glosses[0] is not None:
            sango_glosses[cawl] = str(glosses[0])
    del sango_lex

    # Apply Sango text to Sango glosses in each matching sense.
    gbanu_lex = Lexicon(gbanu_lift)
    for s in gbanu_lex.find_all(field="CAWL"):
        cawl = None
        for f in s.field_items:
            if f.type == 'CAWL':
                cawl = str(f.form_items[0].text)
        if cawl:
            new_gloss = sango_glosses.get(cawl)
        if new_gloss:
            add = True
            for i, g in enumerate(s.gloss_items[:]):
                if g.lang == 'sg':
                    if str(g.text) == new_gloss:
                        add = False
                    else:
                        del s.gloss_items[i]
            if add:
                s.add_gloss(lang='sg', text=new_gloss)
                p = gbanu_lex.get_item_parent_by_id(s.id)
                p.set_date_modified()
                if isinstance(p, lift_utils.lexicon.Sense):
                    e = gbanu_lex.get_item_parent_by_id(p.id)
                    e.set_date_modified()

    # Save to output file.
    gbanu_lex.to_lift('~/gbanu_sg.lift')
    
    # Show memory use, if traced.
    if tracemalloc.is_tracing():
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        for stat in top_stats[:20]:
            print(stat)


if __name__ == '__main__':
    main()
