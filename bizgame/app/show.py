"""For showing tables."""

from .utils import files
from .utils import pretty
from .utils import result

def table(data, rnd, name):
    """Display a table."""
    filepath = files.table_filepath(data, rnd, name)
    r = files.get_data(filepath)
    if result.is_ok(r):
        records = result.v(r)
        output = pretty.table(records)
        return result.ok(output)
    else:
        return r
