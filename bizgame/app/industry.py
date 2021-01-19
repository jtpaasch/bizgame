"""For handling industry tables."""

import copy
import random

from . import constant

from .utils import files
from .utils import nouns
from .utils import pretty
from .utils import query
from .utils import result

def mk_part_types():
    """Generate part types data."""
    output = [record for record in constant.part_types]
    return output

def mk_part_variants():
    """Generate part variants data."""
    output = []
    for record in constant.part_variants:
        cell = "D{}".format(record["ID"] + 1)
        lookup = "=VLOOKUP({},Part_types!$A$2:$C$100,2,FALSE)".format(cell)
        datum = {
            "ID": record["ID"],
            "Name": record["Name"],
            "Part_type_name": lookup,
            "Part_type_ID": record["Part_type_ID"],
            "Min_price": pretty.usd(record["Min_price"]),
            "Max_price": pretty.usd(record["Max_price"]),
        }
        output.append(datum)
    return output

def mk_suppliers():
    """Generate the suppliers data."""
    output = []
    for i in range(constant.num_suppliers):
        datum = {"ID": i + 1, "Name": nouns.fresh_name(2)}
        output.append(datum)
    return output

def mk_supplier_parts(suppliers, part_variants):
    """Generate supplier parts data."""
    output = []
    idx = 1
    for variant in part_variants:
        min_price = pretty.float_of_usd(variant["Min_price"])
        max_price = pretty.float_of_usd(variant["Max_price"])
        suppliers_clone = copy.copy(suppliers)
        random.shuffle(suppliers_clone)
        for i in range(constant.num_part_alternatives):
            supplier = suppliers_clone[i]
            price = pretty.random_price(min_price, max_price)
            bcell = "B{}".format(idx + 1)
            dcell = "D{}".format(idx + 1)
            lookup_a = "=VLOOKUP({},Suppliers!$A$2:$C$100,{},FALSE)"
            lookup_b = "=VLOOKUP({},Part_variants!$A$2:$Z$1000,{},FALSE)"
            supplier_name = lookup_a.format(bcell, 2)
            part_type_id = lookup_b.format(dcell, 4)
            part_type_name = lookup_b.format(dcell, 3)
            part_variant_name = lookup_b.format(dcell, 2)
            datum = {
                "ID": idx,
                "Supplier_ID": supplier["ID"],
                "Supplier_name": supplier_name,
                "Part_variant_ID": variant["ID"],
                "Part_variant_name": part_variant_name,
                "Part_type_ID": part_type_id,
                "Part_type_name": part_type_name,
                "Sell_price": price,
            }
            output.append(datum)
            idx = idx + 1
    return output

def mk_customers():
    """Generate customers data."""
    output = []
    for i in range(constant.num_customers):
        cash = random.randint(
                constant.customer_min_cash, constant.customer_max_cash)
        cash -= cash % -100
        datum = {"ID": i + 1, "Cash": pretty.usd(cash)}
        output.append(datum)
    return output

def mk_customer_values(customers, part_types, catalogue):
    """Generate customer value data."""
    output = []
    idx = 1
    for customer in customers:
        for part_type in part_types:
            part_type_id = part_type["ID"]
            selector = lambda x: x["Part_type_ID"] == str(part_type_id)
            options = list(filter(selector, catalogue))
            choose = random.randint(0, 1)
            if choose:
                choice = random.randint(1, len(options) - 1)
                option = options[choice]
                weight = "{:.2f}".format(random.random())
                cell = "C{}".format(idx + 1)
                lookup = "=VLOOKUP({},Supplier_parts!$A$2:$Z$1000,{},FALSE)"
                supplier_id = lookup.format(cell, 2)
                supplier_name = lookup.format(cell, 3)
                part_variant_id = lookup.format(cell, 4)
                part_variant_name = lookup.format(cell, 5)
                part_type_id = lookup.format(cell, 6)
                part_type_name = lookup.format(cell, 7)
                datum = {
                    "ID": idx,
                    "Customer_ID": customer["ID"],
                    "Supplier_part_ID": option["ID"],
                    "Supplier_ID": supplier_id,
                    "Supplier_name": supplier_name,
                    "Part_variant_ID": part_variant_id,
                    "Part_variant_name": part_variant_name,
                    "Part_type_id": part_type_id,
                    "Part_type_name": part_type_name,
                    "Weight": weight,
                }
                output.append(datum)
                idx = idx + 1
    return output

def generate(data):
    """Generate industry tables."""
    part_types = mk_part_types()
    filepath = files.table_filepath(data, 1, "part_types")
    files.write_data(filepath, part_types)

    part_variants = mk_part_variants()
    filepath = files.table_filepath(data, 1, "part_variants")
    files.write_data(filepath, part_variants)

    suppliers = mk_suppliers()
    filepath = files.table_filepath(data, 1, "suppliers")
    files.write_data(filepath, suppliers)

    supplier_parts = mk_supplier_parts(suppliers, part_variants)
    filepath = files.table_filepath(data, 1, "supplier_parts")
    files.write_data(filepath, supplier_parts)

    customers = mk_customers()
    filepath = files.table_filepath(data, 1, "customers")
    files.write_data(filepath, customers)

    r = query.catalogue(data, 1)
    if result.is_error(r):
        return r
    catalogue = result.v(r)
    customer_values = mk_customer_values(customers, part_types, catalogue)
    filepath = files.table_filepath(data, 1, "customer_values")
    files.write_data(filepath, customer_values)

    files.new_round(data, 2)

    return result.ok()
