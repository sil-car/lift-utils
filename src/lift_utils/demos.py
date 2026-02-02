"""Functions needed to run demo scripts."""

from .lexicon import Lexicon


def lexical_units_from_lift(lift, cawls):
    lex = Lexicon(lift)
    lexical_units = []
    for cawl in cawls:
        lexical_unit = None
        item = lex.find(cawl, field="CAWL", match_type="exact")
        if item and item.id:
            # parent = lex.get_item_parent_by_id(item.id)
            parent = item.parent
            if parent:
                lexical_unit = parent.lexical_unit
        lexical_units.append(lexical_unit)
    return lexical_units
