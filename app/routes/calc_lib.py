import json
import pandas as pd


# --- Helper: safely decode DataFrame or leave plain value ---
def safe_read_json(obj):
    if obj is None:
        return None
    if isinstance(obj, str):
        try:
            data = json.loads(obj)
            # Detect Pandas JSON orient='split'
            if isinstance(data, dict) and "columns" in data and "data" in data:
                return [dict(zip(data["columns"], row)) for row in data["data"]]
            return data
        except Exception:
            return obj
    return obj


def decode_if_json(obj):
    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except json.JSONDecodeError:
            return obj
    return obj


def get_html_vars(data, form):
    """
    Rebuilds HTML variables returned from Cloud Run without using pandas.
    Safely decodes JSON-like strings (e.g., dicts or lists) and keeps SVG/text untouched.
    """
    html_vars_raw = data.get("html_vars", {}) or {}
    html_vars = {}

    for k, v in html_vars_raw.items():
        # --- Handle strings first ---
        if isinstance(v, str):
            # SVGs: leave untouched
            if v.strip().startswith("<svg"):
                html_vars[k] = v
                continue

            # Try JSON decoding
            try:
                decoded = json.loads(v)
                html_vars[k] = decoded
            except (json.JSONDecodeError, TypeError):
                # Not JSON — just store raw string
                html_vars[k] = v
        else:
            # Already a Python object (dict, list, number, etc.)
            html_vars[k] = v

    # Attach form for template rendering
    html_vars["form"] = form
    return html_vars


def rebuild_CalcVars(resp, form):
    """
    Rebuilds a FundVars-like object from the JSON response returned by Cloud Run.
    Safely handles nested DataFrames, SVGs, and html_vars, and reconstructs a form object.
    """
    from types import SimpleNamespace

    data = resp.json()
    res = SimpleNamespace()

    res.html_vars = get_html_vars(data, form)
    return res