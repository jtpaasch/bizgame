"""Handles buyers/purchasing."""

from .utils import pretty
from .utils import query

def candidates_by_supplier(products, values):
    """Find candidates by supplier parts."""
    output = []
    for product in products:
        is_candidate = True
        for value in values:
            idx = value["Supplier_part_ID"]
            matches = query.select(product["Parts"], "ID", idx)
            if not matches:
                is_candidate = False
                break
        if is_candidate:
            output.append(product)
    return sorted(output, key=lambda record: record["Sell_price"])

def candidates_by_variant(products, values):
    """Find candidates by part variants."""
    output = []
    for product in products:
        is_candidate = True
        for value in values:
            idx = value["Part_variant_ID"]
            matches = query.select(product["Parts"], "Part_variant_ID", idx)
            if not matches:
                is_candidate = False
                break
        if is_candidate:
            output.append(product)
    return sorted(output, key=lambda record: record["Sell_price"])

def next_available(customer, candidates, available):
    """Find the first affordable and available candidate."""
    while len(candidates) > 0:
        units_available = available[candidates[0]["Company_ID"]]
        if units_available > 0:
            sell_price = candidates[0]["Sell_price"]
            cash = pretty.float_of_usd(customer["Cash"])
            if sell_price <= cash:
                return candidates[0]
        candidates = candidates[1:]
    return None

def buy(customer, products, values, inventory):
    """Select a product for a customer."""
    vals = sorted(values, key=lambda record: record["Weight"])

    # Find a product with supplier parts the customer values.
    selected_values = vals[:]
    while len(selected_values) > 0:
        candidates = candidates_by_supplier(products, selected_values)
        if candidates:
            candidate = next_available(customer, candidates, inventory)
            if candidate:
                return candidate
        selected_values = selected_values[1:]

    # If we couldn't find a product with the right supplier parts,
    # then find a product with part variants the customer values.
    selected_values = vals[:]
    while len(selected_values) > 0:
        candidates = candidates_by_variant(products, selected_values)
        if candidates:
            candidate = next_available(customer, candidates, inventory)
            if candidate:
                return candidate
        selected_values = selected_values[1:]

    # If we're here, we couldn't find a product the customer likes.
    return None
