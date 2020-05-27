"""Parses command line arguments."""

import argparse

def parse():
    """Build a config record from the CLI arguments."""
    desc = "A business simulation game."
    data_opt = "--data"
    data_help = "/path/to/dir to store .tsv files"
    round_opt = "--round"
    round_help = "Round number"

    parser = argparse.ArgumentParser(description=desc)
    subparsers = parser.add_subparsers(
            dest="subcommand", help="subcommand help", required=True)

    show = subparsers.add_parser("show", help="show help")
    show.add_argument("table", help="Name of the table to show")
    show.add_argument(data_opt, help=data_help, required=True)
    show.add_argument(round_opt, help=round_help, type=int, required=True)
    show.set_defaults(action="show")

    companies = subparsers.add_parser("companies", help="companies help")
    companies.add_argument("generate", help="Generate companies")
    companies.add_argument("--CEOs", help="/path/to/ceos.tsv", required=True)
    companies.add_argument(data_opt, help=data_help, required=True)
    companies.set_defaults(action="companies")

    industry = subparsers.add_parser("industry", help="industry help")
    industry.add_argument("generate", help="Generate the industry")
    industry.add_argument(data_opt, help=data_help, required=True)
    industry.set_defaults(action="industry")

    simulate = subparsers.add_parser("simulate", help="simulate help")
    simulate.add_argument("buying", help="Simulate a round of buying")
    simulate.add_argument(data_opt, help=data_help, required=True)
    simulate.add_argument(round_opt, help=round_help, type=int, required=True)
    simulate.set_defaults(action="simulate")

    args = parser.parse_args()

    config = {}
    if args.action == "show":
        config["action"] = args.action
        config["table"] = args.table
        config["round"] = args.round
        config["data"] = args.data
    elif args.action == "companies":
        config["action"] = args.action
        config["CEOs"] = args.CEOs
        config["data"] = args.data
    elif args.action == "industry":
        config["action"] = args.action
        config["data"] = args.data
    elif args.action == "simulate":
        config["action"] = args.action
        config["data"] = args.data
        config["round"] = args.round
    else:
        exit("Unknown arguments. See --help.")

    return config
