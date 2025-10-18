import pandas as pd


# --- Helper: safely decode DataFrame or leave plain value ---
def safe_read_json(obj):
    if isinstance(obj, str):
        try:
            return pd.read_json(obj)
        except ValueError:
            return obj
    return obj


# --- html_vars reconstruction ---
def get_html_vars(data, form):
    html_vars_raw = data.get("html_vars", {})
    html_vars = {}

    for k, v in html_vars_raw.items():
        if isinstance(v, str):
            if v.strip().startswith("<svg"):
                html_vars[k] = v
            else:
                try:
                    html_vars[k] = pd.read_json(v)
                except Exception:
                    html_vars[k] = v
        else:
            html_vars[k] = v

    html_vars["form"] = form
    return html_vars