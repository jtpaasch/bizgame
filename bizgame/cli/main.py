"""The CLI."""

import logging
import sys

from . import args
from ..app import main
from ..app.utils import result

def get_logger():
    """Get a stdout logger."""
    name = "main-log"
    fmt = "%(message)s"
    formatter = logging.Formatter(fmt)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    log = logging.getLogger(name)
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    return log

def cli():
    """The entry point to the CLI."""
    log = get_logger()
    config = args.parse()
    r = main.run(log.info, config)
    if result.is_ok(r):
        v = result.v(r).strip()
        if v:
            log.info(v)
    else:
        exit(result.e(r))
