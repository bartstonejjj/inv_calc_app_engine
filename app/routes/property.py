from app import app
from app.forms import create_investment_parameters_form
from app.routes.lib import get_client_ip
from app.routes.calc_lib import safe_read_json, get_html_vars
from app.routes.calc_page_workflow import render_calc_page
from flask import g
from flask_login import login_required


# rebuild_FundVars from Cloud Run response
def rebuild_HomeBuyingVars(resp, form):
    """
    Rebuilds a FundVars-like object from the JSON response returned by Cloud Run.
    Safely handles nested DataFrames, SVGs, and html_vars, and reconstructs a form object.
    """
    from types import SimpleNamespace

    data = resp.json()
    res = SimpleNamespace()

    # # --- Core FundVars reconstruction --- (NOT SENT BY CLOUD RUN)
    # res.summary = safe_read_json(data.get("summary"))
    # res.metrics_descriptions = data.get("metrics_descriptions", {})
    # res.s_fund = data.get("s_fund", {})
    #
    # # --- What-if DataFrames ---
    # res.whatif_dfs = {k: safe_read_json(v) for k, v in data.get("whatif_dfs", {}).items()}
    #
    # # --- Inputs ---
    # res.inputs = data.get("inputs", {})

    res.html_vars = get_html_vars(data, form)
    return res


@app.route('/property', methods=['GET', 'POST'])
@login_required
def property_page():
    form = create_investment_parameters_form(groups=['base', 'property'])
    return render_calc_page(
        cloud_run_route='calc_property',
        calc_name = 'property',
        ip = get_client_ip(app), 
        rebuilder = rebuild_HomeBuyingVars,
        form = form,
        html_file = 'property.html', 
        cache_name = 'property_page',
        falsk_g = g,
        global_vars = {
            'intro':'content/property_page/intro.html',
            'in_plain_english':'content/property_page/in_plain_english.html',
            'full_model_description':'content/property_page/full_model_description.html',
            'whatif_intro':'content/property_page/whatif_intro.html'},
        )