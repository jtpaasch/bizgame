"""Utilities for handling files."""

import csv
import shutil
from pathlib import Path
from . import result

input_subdir = "input"
output_subdir = "output"

def table_file(name):
    """Generate the filename for a table."""
    return "{}.tsv".format(name)

def mkdir(filepath):
    """Create a directory if it doesn't exist."""
    p = filepath.expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)

def rm(filepath):
    """Delete a file."""
    filepath.unlink()

def input_dir(data, rnd, create=True):
    """Get the data input directory for a specific round."""
    p = Path(data, str(rnd), input_subdir)
    if create:
        mkdir(p)
    return p

def output_dir(data, rnd, create=True):
    """Get the data output directory for a specific round."""
    p = Path(data, str(rnd), output_subdir)
    if create:
        mkdir(p)
    return p

def input_filepath(data, rnd, name):
    """Get the path to an input *.tsv file."""
    p = input_dir(data, rnd)
    return p / table_file(name)

def table_filepath(data, rnd, name):
    """Get the path to a table's *.tsv file."""
    p = output_dir(data, rnd)
    return p / table_file(name)

def new_round(data, rnd):
    """Copy the data from the previous round to a new round."""
    src = output_dir(data, rnd - 1, create=False)
    dst = output_dir(data, rnd, create=False)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)

def get_data(filepath):
    """Get table data."""
    data = []
    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter='\t')
            data = [row for row in reader]
    except FileNotFoundError:
        msg = "No such table/file: {}".format(filepath)
        return result.error(msg)
    return result.ok(data)

def write_data(filepath, records, append=False):
    """Write table data."""
    fieldnames = []
    if len(records) > 0:
        record = records[0]
        fieldnames = record.keys()
    mode = "a" if append else "w"
    with open(filepath, mode=mode, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        if append is False:
            writer.writeheader()
        for record in records:
            writer.writerow(record)
