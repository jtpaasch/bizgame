"""Constants for the app."""

capital = 100000
"""Amount of capital companies get to start with."""

num_suppliers = 12
"""Number of suppliers to have in the industry."""

num_part_alternatives = 5
"""Number of alternatives offered by suppliers for any given part.""" 

num_customers = 1000
"""Number of customers on the market."""

customer_min_cash = 200
customer_max_cash = 2500
"""Min and max amount customers are willing to spend on the product."""

part_types = [
    {
        "ID": 1,
        "Name": "Heating element",
    },
    {
        "ID": 2,
        "Name": "Heating bowl",
    },
    {
        "ID": 3,
        "Name": "Interface",
    },
    {
        "ID": 4,
        "Name": "Power unit",
    },
]
"""Every product needs one of these types of parts in it."""

part_variants = [
    {
        "ID": 1,
        "Name": "Standard",
        "Part_type_ID": 1,
        "Min_price": 10.00,
        "Max_price": 20.00,
    },
    {
        "ID": 2,
        "Name": "Durable",
        "Part_type_ID": 1,
        "Min_price": 30.00,
        "Max_price": 40.00,
    },
    {
        "ID": 3,
        "Name": "Super",
        "Part_type_ID": 1,
        "Min_price": 100.00,
        "Max_price": 500.00,
    },
    {
        "ID": 4,
        "Name": "Plastic",
        "Part_type_ID": 2,
        "Min_price": 10.00,
        "Max_price": 20.00,
    },
    {
        "ID": 5,
        "Name": "Removable plastic",
        "Part_type_ID": 2,
        "Min_price": 15.00,
        "Max_price": 25.00,
    },
    {
        "ID": 6,
        "Name": "Steel",
        "Part_type_ID": 2,
        "Min_price": 50.00,
        "Max_price": 100.00,
    },
    {
        "ID": 7,
        "Name": "Removable steel",
        "Part_type_ID": 2,
        "Min_price": 50.00,
        "Max_price": 125.00,
    },
    {
        "ID": 8,
        "Name": "Ceramic",
        "Part_type_ID": 2,
        "Min_price": 75.00,
        "Max_price": 150.00,
    },
    {
        "ID": 9,
        "Name": "Removable ceramic",
        "Part_type_ID": 2,
        "Min_price": 125.00,
        "Max_price": 200.00,
    },
    {
        "ID": 10,
        "Name": "Analog",
        "Part_type_ID": 3,
        "Min_price": 10.00,
        "Max_price": 100.00,
    },
    {
        "ID": 11,
        "Name": "Digital",
        "Part_type_ID": 3,
        "Min_price": 10.00,
        "Max_price": 20.00,
    },
    {
        "ID": 12,
        "Name": "Touchscreen",
        "Part_type_ID": 3,
        "Min_price": 100.00,
        "Max_price": 500.00,
    },
    {
        "ID": 13,
        "Name": "Standard plug",
        "Part_type_ID": 4,
        "Min_price": 5.00,
        "Max_price": 25.00,
    },
    {
        "ID": 14,
        "Name": "Rechargeable battery",
        "Part_type_ID": 4,
        "Min_price": 25.00,
        "Max_price": 150.00,
    },
]
"""Variations on the essential part types."""
