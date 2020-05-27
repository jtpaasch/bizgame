"""For handling the companies table."""

from .utils import files
from .utils import nouns
from .utils import result

def has_correct_data(CEOs, records):
    """Check if the data from a CEOs.tsv file has the right data."""
    if len(records) < 1:
        msg = "File empty: {}".format(CEOs)
        return result.error(msg)
    else:
        first_row = records[0]
        if first_row.get("Name"):
            return result.ok()
        else:
            msg = "No 'Name' column in: {}".format(CEOs)
            return result.error(msg)

def mk_companies(records):
    """Generate a companies table."""
    output = []
    for idx, record in enumerate(records):
        ceo = record["Name"]
        company = nouns.fresh_name(2)
        datum = {"ID": idx + 1, "Company": company, "CEO": ceo}
        output.append(datum)
    return output

def generate(data, CEOs):
    """Generate a list of companies."""
    r = files.get_data(CEOs)
    if result.is_error(r):
        return r
    else:
        records = result.v(r)
        r = has_correct_data(CEOs, records)
        if result.is_error(r):
            return r
        else:
            companies = mk_companies(records)
            filepath = files.table_filepath(data, 1, "companies")
            files.write_data(filepath, companies)
            return result.ok()
