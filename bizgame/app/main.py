"""The main entry point for the application."""

from . import companies
from . import industry
from . import show
from . import simulate
from .utils import result

def show_table(log, config):
    """Handler for showing a table."""
    r = show.table(config["data"], config["round"], config["table"])
    if result.is_ok(r):
        log(result.v(r))
        return result.ok()
    else:
        return r

def generate_companies(log, config):
    """Handler for generating companies."""
    return companies.generate(config["data"], config["CEOs"])

def generate_industry(log, config):
    """Handler for generating industry."""
    return industry.generate(config["data"])

def simulate_buying(log, config):
    """Handler for simulating a round of buying."""
    return simulate.buying(config["data"], config["round"])

def run(log, config):
    """Starts the application."""
    if config["action"] == "show":
        return show_table(log, config)
    elif config["action"] == "companies":
        return generate_companies(log, config)
    elif config["action"] == "industry":
        return generate_industry(log, config)
    elif config["action"] == "simulate":
        return simulate_buying(log, config)
    else:
        return result.error("Unknown action. Nothing to do.")

