"""Utilities for querying data."""

from .. import constant
from . import files
from . import pretty
from . import result

class NoMatch(Exception):
    """Raise when no match is found."""
    pass

class TooManyMatches(Exception):
    """Raise when too many matches are found."""
    pass

def select(records, field, value):
    """Find rows in a set of records."""
    selector = lambda x: x[field] == value
    return list(filter(selector, records))

def find(records, field, value):
    """Find a row in a set of records."""
    matches = select(records, field, value)
    if len(matches) == 0:
        msg = "No record with {} = '{}'".format(field, value)
        raise NoMatch(msg)
    elif len(matches) > 1:
        msg = "Too many records with {} = '{}'".format(field, value)
        raise TooManyMatches(msg)
    else:
        return matches[0]

def mk_catalogue(part_types, part_variants, suppliers, supplier_parts):
    """Build the parts catalogue."""
    output = []
    for part in supplier_parts:
        idx = part["ID"]
        supplier_id = part["Supplier_ID"]
        supplier = find(suppliers, "ID", supplier_id)
        variant_id = part["Part_variant_ID"]
        variant = find(part_variants, "ID", variant_id)
        part_type_id = variant["Part_type_ID"]
        part_type = find(part_types, "ID", part_type_id)
        sell_price = pretty.float_of_usd(part["Sell_price"])
        datum = {
            "ID": idx,
            "Supplier_ID": supplier_id,
            "Supplier_name": supplier["Name"],
            "Part_variant_ID": variant_id,
            "Part_variant_name": variant["Name"],
            "Part_type_ID": part_type_id,
            "Part_type_name": part_type["Name"],
            "Sell_price": sell_price,
        }
        output.append(datum)
    return output

def catalogue(data, rnd):
    """Build the parts catalogue for a specific round."""
    filepath = files.table_filepath(data, rnd, "part_types")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    part_types = result.v(r)

    filepath = files.table_filepath(data, rnd, "part_variants")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    part_variants = result.v(r)
    
    filepath = files.table_filepath(data, rnd, "suppliers")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    suppliers = result.v(r)
    
    filepath = files.table_filepath(data, rnd, "supplier_parts")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    supplier_parts = result.v(r)

    r = mk_catalogue(part_types, part_variants, suppliers, supplier_parts)
    return result.ok(r)

def mk_products(rnd, companies, products, production, parts):
    """Build the products for a round."""
    output = []
    rnd = str(rnd)
    product_data = select(products, "Round", rnd)
    for company in companies:
        product_parts = select(product_data, "Company_ID", company["ID"])
        if len(product_parts) == 0:
            continue
        orders = select(production, "Company_ID", company["ID"])
        order = find(orders, "Round", rnd)
        product = {
            "Company_ID": company["ID"],
            "Units": order["Units"],
            "Sell_price": pretty.float_of_usd(order["Sell_price"]),
            "Parts": [],
            "Cost": None,
        }
        cost = 0
        for part in product_parts:
            part_id = part["Supplier_part_ID"]
            part = find(parts, "ID", part_id)
            product["Parts"].append(part)
            cost = cost + part["Sell_price"]
        product["Cost"] = cost
        output.append(product)
    return output

def products(data, rnd):
    """Build the products for a round."""
    r = catalogue(data, rnd)
    if result.is_error(r):
        return r
    parts = result.v(r)

    filepath = files.table_filepath(data, rnd, "companies")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    companies = result.v(r)

    filepath = files.table_filepath(data, rnd, "products")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    products = result.v(r)

    filepath = files.table_filepath(data, rnd, "production")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    production = result.v(r)

    r = mk_products(rnd, companies, products, production, parts)
    return result.ok(r)

def latest_capital(revenue, rnd, company_id):
    """Find the latest record of capital for a company."""
    prev_rnd = rnd - 1
    output = constant.capital
    if prev_rnd < 2:
        return output
    records = select(revenue, "Round", str(prev_rnd))
    try:
        record = find(records, "Company_ID", company_id)
        output = pretty.float_of_usd(record["Capital"])
        return output
    except NoMatch:
        return latest_capital(revenue, prev_rnd, company_id)

def financials(data, rnd):
    """Get financial data for the round."""
    filepath = files.table_filepath(data, rnd, "companies")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    companies = result.v(r)

    filepath = files.table_filepath(data, rnd, "revenue")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    revenue = result.v(r)

    output = {}
    for company in companies:
        company_id = company["ID"]
        capital = latest_capital(revenue, rnd, company_id)
        output[company_id] = capital
    return result.ok(output)
