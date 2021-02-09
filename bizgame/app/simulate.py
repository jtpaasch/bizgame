"""For simulating a round of buying."""

from . import constant
from . import buyers

from .utils import files
from .utils import pretty
from .utils import query
from .utils import result

def mk_part(idx, part_id, rnd, order):
    """Create a part record for the products table."""
    lookup = "=VLOOKUP({},Supplier_parts!$A$2:$Z$1000,{},FALSE)"
    col = "C{}".format(idx + 1)
    supplier_id = lookup.format(col, 2)
    supplier_name = lookup.format(col, 3)
    part_variant_id = lookup.format(col, 4)
    part_variant_name = lookup.format(col, 5)
    part_type_id = lookup.format(col, 6)
    part_type_name = lookup.format(col, 7)
    sell_price = lookup.format(col, 8)
    return {
        "Round": rnd,
        "Company_ID": order["Company_ID"],
        "Supplier_part_ID": part_id,
        "Supplier_ID": supplier_id,
        "Supplier_name": supplier_name,
        "Part_variant_ID": part_variant_id,
        "Part_variant_name": part_variant_name,
        "Part_type_ID": part_type_id,
        "Part_type_name": part_type_name,
        "Sell_price": sell_price,
    }

def is_valid_order(order, catalogue):
    part_types = constant.part_types
    part_id = order["Heating_element"]
    part = query.find(catalogue["value"], "ID", part_id)
    part_type_id = int(part["Part_type_ID"])
    part_type = query.find(part_types, "Name", "Heating element")
    correct_id = part_type["ID"]
    if part_type_id != correct_id:
        print("NOT A HEATING ELEMENT!")
        print(order)
        print(part)
        return False
    part_id = order["Heating_bowl"]
    part = query.find(catalogue["value"], "ID", part_id)
    part_type_id = int(part["Part_type_ID"])
    part_type = query.find(part_types, "Name", "Heating bowl")
    correct_id = part_type["ID"]
    if part_type_id != correct_id:
        print("NOT A HEATING BOWL!")
        print(order)
        print(part)
        return False
    part_id = order["Interface"]
    part = query.find(catalogue["value"], "ID", part_id)
    part_type_id = int(part["Part_type_ID"])
    part_type = query.find(part_types, "Name", "Interface")
    correct_id = part_type["ID"]
    if part_type_id != correct_id:
        print("NOT AN INTERFACE!")
        print(order)
        print(part)
        return False
    part_id = order["Power_unit"]
    part = query.find(catalogue["value"], "ID", part_id)
    part_type_id = int(part["Part_type_ID"])
    part_type = query.find(part_types, "Name", "Power unit")
    correct_id = part_type["ID"]
    if part_type_id != correct_id:
        print("NOT A POWER UNIT!")
        print(order)
        print(part)
        return False
    return True

def mk_products(records, rnd, orders, catalogue):
    """Build the products table data."""
    output = []
    idx = len(records) + 1
    for order in orders:
        print("---- Processing order -------------")
        if not is_valid_order(order, catalogue):
            print("     NOT VALID, SKIPPING")
            continue
        else:
            print("     Ok")
        part_id = order["Heating_element"]
        datum = mk_part(idx, part_id, rnd, order)
        output.append(datum)
        idx = idx + 1
        part_id = order["Heating_bowl"]
        datum = mk_part(idx, part_id, rnd, order)
        output.append(datum)
        idx = idx + 1
        part_id = order["Interface"]
        datum = mk_part(idx, part_id, rnd, order)
        output.append(datum)
        idx = idx + 1
        part_id = order["Power_unit"]
        datum = mk_part(idx, part_id, rnd, order)
        output.append(datum)
        idx = idx + 1
    return output

def mk_production(records, rnd, orders, financials):
    """Build the production table data."""
    output = []
    idx = len(records) + 1
    criteria_1 = "Products!$A$2:$A$10000,A{}"
    criteria_2 = "Products!$B$2:$B$10000,B{}"
    lookup = "=SUMIFS(Products!$J$2:$J$10000,{},{})"
    lookup_2 = "=C{}*E{}"
    for order in orders:
        row = idx + 1
        slot_1 = criteria_1.format(row)
        slot_2 = criteria_2.format(row)
        cost_per_unit = lookup.format(slot_1, slot_2)
        cost_all_units = lookup_2.format(row, row)
        company_id = order["Company_ID"]
        datum = {
            "Round": rnd,
            "Company_ID": company_id,
            "Units": order["Num_units"],
            "Sell_price": order["Sell_price"],
            "Cost_per_unit": cost_per_unit,
            "Cost_all_units": cost_all_units,
            "Available_capital": pretty.usd(financials[company_id]),
        }
        output.append(datum)
        idx = idx + 1
    return output

def mk_sales(rnd, customers, values, products):
    """Build the sales table data."""
    output = []
    inventory = {x["Company_ID"]: int(x["Units"]) for x in products}
    for customer in customers:
        customer_id = customer["ID"]
        vals = query.select(values, "Customer_ID", customer_id)
        if vals:
            purchase = buyers.buy(customer, products, vals, inventory)
            if purchase:
                remaining = inventory[purchase["Company_ID"]] - 1
                inventory[purchase["Company_ID"]] = remaining
                datum = {
                    "Round": rnd,
                    "Customer_ID": customer_id,
                    "Company_ID": purchase["Company_ID"],
                    "Purchase_price": pretty.usd(purchase["Sell_price"]),
                }
                output.append(datum)
    return output

def mk_revenue(rnd, products, purchases, financials):
    """Build the revenue table data."""
    output = []
    for product in products:
        company_id = product["Company_ID"]
        sales = query.select(purchases, "Company_ID", company_id)
        sales = query.select(sales, "Round", rnd)
        units_sold = len(sales)
        total_sales = 0
        if sales:
            prices = [pretty.float_of_usd(x["Purchase_price"]) for x in sales]
            total_sales = sum(prices)
        total_costs = int(product["Units"]) * product["Cost"]
        profit = total_sales - total_costs
        capital = financials[company_id] + profit
        datum = {
            "Company_ID": company_id,
            "Round": rnd,
            "Cost_per_unit": pretty.usd(product["Cost"]),
            "Units_manufactured": product["Units"],
            "Total_costs": pretty.usd(total_costs),
            "Sell_price": pretty.usd(product["Sell_price"]),
            "Units_sold": units_sold,
            "Sales": pretty.usd(total_sales),
            "Profit": pretty.usd(profit),
            "Capital": pretty.usd(capital),
        }
        output.append(datum)
    return output

def buying(data, rnd):
    """Simulate a round of buying."""
    if rnd == 1:
        msg = "Cannot simulate buying for round 1. Only round 2 and up."
        return result.error(msg)

    # There's no simulation history before round 2.
    append = False if rnd == 2 else True

    # Get financial data.
    r = query.financials(data, rnd)
    if result.is_error(r):
        return r
    financials = result.v(r)

    # Get the catalogue
    catalogue = query.catalogue(data, rnd)

    # Get the orders.
    orders_input = files.input_filepath(data, rnd, "orders")
    r = files.get_data(orders_input)
    if result.is_error(r):
        return r
    orders = result.v(r)

    # Get any previous product records.
    records = []
    if append:
        filepath = files.table_filepath(data, rnd, "products")
        r = files.get_data(filepath)
        if result.is_error(r):
            return r
        records = result.v(r)

    # Build the product data.
    products = mk_products(records, rnd, orders, catalogue)
    filepath = files.table_filepath(data, rnd, "products")
    files.write_data(filepath, products, append=append)

    # Get any previous production records.
    records = []
    if append:
        filepath = files.table_filepath(data, rnd, "production")
        r = files.get_data(filepath)
        if result.is_error(r):
            return r
        records = result.v(r)

    # Build the production data.
    production = mk_production(records, rnd, orders, financials)
    filepath = files.table_filepath(data, rnd, "production")
    files.write_data(filepath, production, append=append)

    # Get the customers
    filepath = files.table_filepath(data, rnd, "customers")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    customers = result.v(r)

    # Get the customer values
    filepath = files.table_filepath(data, rnd, "customer_values")
    r = files.get_data(filepath)
    if result.is_error(r):
        return r
    values = result.v(r)

    # Get product data for this round.
    r = query.products(data, rnd)
    if result.is_error(r):
        return r
    products = result.v(r)

    # Build the purchases data.
    purchases = mk_sales(rnd, customers, values, products)
    filepath = files.table_filepath(data, rnd, "purchases")
    files.write_data(filepath, purchases, append=append)

    # Build the revenue data.
    revenue = mk_revenue(rnd, products, purchases, financials)
    filepath = files.table_filepath(data, rnd, "revenue")
    files.write_data(filepath, revenue, append=append)

    # Create the baseline data for the next round.
    files.new_round(data, rnd + 1)

    return result.ok()
