"""A simple result type/module."""

def ok(v=""):
    """Build an `Ok` result."""
    return {"variant": "ok", "value": v, "error": None}

def error(e):
    """Build an `Error` result."""
    return {"variant": "error", "value": None, "error": e}

def is_ok(result):
    """Check if the result is `Ok`."""
    return result["variant"] == "ok"

def is_error(result):
    """Check if the result is `Error`."""
    return result["variant"] == "error"

def v(result):
    """Get the value embedded in the result."""
    return result["value"]

def e(result):
    """Get the error embedded in the result."""
    return result["error"]
