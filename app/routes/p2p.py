from app import app
from app.forms import create_investment_parameters_form
from app.routes.lib import get_client_ip
from app.routes.calc_lib import safe_read_json, get_html_vars
from app.routes.calc_page_workflow import render_calc_page
from flask import g
from flask_login import login_required


# rebuild_FundVars from Cloud Run response
def rebuild_P2PVars(resp, form):
    """
    Rebuilds a FundVars-like object from the JSON response returned by Cloud Run.
    Safely handles nested DataFrames, SVGs, and html_vars, and reconstructs a form object.
    """
    from types import SimpleNamespace

    data = resp.json()
    res = SimpleNamespace()

    # --- Core FundVars reconstruction ---
    res.summary = safe_read_json(data.get("summary"))
    res.metrics_descriptions = data.get("metrics_descriptions", {})

    # --- Inputs ---
    res.inputs = data.get("inputs", {})

    res.html_vars = get_html_vars(data, form)
    return res


@app.route('/peer_to_peer', methods=['GET', 'POST'])
@login_required
def p2p_page():
    form = create_investment_parameters_form(groups=['base', 'savings', 'p2p'])
    return render_calc_page(
        cloud_run_route = 'calc_p2p',
        rebuilder = rebuild_P2PVars,
        form = form,
        calc_name = 'p2p',
        ip = get_client_ip(app),
        html_file = 'p2p.html', 
        cache_name = 'p2p_page',
        falsk_g = g,
        global_vars = {
            'intro':'content/p2p_page/intro.html',
            'in_plain_english':'content/p2p_page/in_plain_english.html',
            'full_model_description':'content/p2p_page/full_model_description.html'})