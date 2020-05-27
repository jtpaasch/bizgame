"""Utilities for formatting and printing data."""

import os
import random

def usd(n):
    """Convert a number into a USD currency string."""
    return "${:.2f}".format(n)

def float_of_usd(n):
    """Convert a USD currency string into a number."""
    datum = n.replace(",", "")
    if datum[0:1] == "$":
        datum = datum[1:]
    return float(datum)

def random_price(min_price, max_price):
    """Pick a random price between a min and a max."""
    selection = random.uniform(float(min_price), float(max_price))
    return usd(selection)

def pad(value, width):
    """Pads a value with spaces to make the string a certain width."""
    value_width = len(str(value))
    if value_width > width:
        return value
    else:
        padding = width - value_width
        return "{}{}".format(value, " " * padding)

def table(data):
    """Print a dictionary as a table."""
    if len(data) == 0:
        return ""
    sample = data[0]
    headers = sample.keys()
    widths = {k: 0 for k in headers}
    for header in headers:
          best = widths[header]
          size = len(header)
          if size > best:
              widths[header] = size
    for row in data:
        for k, v in row.items():
            best = widths[k]
            size = len(str(v))
            if size > best:
                widths[k] = size
    out = []
    inner_rule = "+".join(["-" * (wd + 2) for wd in widths.values() ])
    rule = "+{}+".format(inner_rule)
    inner_header = " | ".join(
        [pad(k.upper(), widths[k]) for k in headers])
    header = "| {} |".format(inner_header)
    out.append(rule)
    out.append(header)
    out.append(rule)
    for row in data:
        inner_content = " | ".join(
                [pad(v, widths[k]) for k, v in row.items()])
        content = "| {} |".format(inner_content)
        out.append(content)
        out.append(rule)
    return os.linesep.join(out)
