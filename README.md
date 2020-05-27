# bizgame

A simple business simulation game.

Below are instructions for generating the data for each round of a game.
The data is kept in `.tsv` files (tab-separated values files), but you
can import that data into Excel/Google Sheets workbooks for easier
presentation to others.


## Installation

Make sure you have Python 3.7 or higher. 

Clone the repo, `cd` into it, and pip install. For example:

    cd ~/code
    git clone https://github.com/jtpaasch/bizgame.git
    cd bizgame
    python3 -m venv venv
    source venv/bin/activate
    pip install -u pip
    pip install -e .


## Usage

Create a directory somewhere for the game data, e.g.,:

    mkdir -p ~/bizgame

Create a tab-separated values file called `~/bizgame/CEOs.tsv` which has 
one column called 'Name' and any number of names for the CEOs, e.g.:

    Name
    Alice Johansen
    Bob Thurston
    Carol Carolina
    ...

Generate a list of companies from that data:

    bizgame companies generate --data ~/bizgame --CEOs ~/bizgame/CEOs.tsv

You can view the table it created:

    bizgame show companies --data ~/bizgame --round 1

Generate the industry data:

    bizgame industry generate --data ~/bizgame

You can see the new data at:

    ~/bizgame/1/output

To simulate the next round, first create a tab-separated values file called
`~/bizgame/2/input/orders.tsv`, which contains a manufacturing order for 
each company that looks something like this:

    Round  Company_ID  Heating_element Heating_bowl Interface Power_unit Num_units Sell_price
    2      1           1               16           46        61         100       $250.00
    2      2           2               18           47        62         35        $599.99
    ...

The heating element, heating bowl, interface, and power unit cells should 
be filled in with IDs from `~/bizgame/2/output/supplier_parts.tsv`.

Once you have created that `orders.tsv` file, you can simulate a round of 
buying with this command:

    bizgame simulate buying --data ~/bizgame --round 2

You can then see the new data at:

    ~/bizgame/2/output

There is help/usage for the command and all of its subcommands:

    bizgame --help
    bizgame show --help
    ...


