from app import app
from app.forms import create_investment_parameters_form
from app.routes.lib import get_client_ip
from app.routes.calc_lib import rebuild_CalcVars
from app.routes.calc_page_workflow import render_calc_page
from flask import g
from flask_login import login_required


@app.route('/fund', methods=['GET', 'POST'])
@login_required
def fund_page():
    form = create_investment_parameters_form(groups=['base', 'fund'])
    return render_calc_page(
        cloud_run_route = 'calc_fund',
        rebuilder = rebuild_CalcVars,
        form = form,
        calc_name = 'fund',
        ip = get_client_ip(app),
        html_file = 'fund.html',
        cache_name = 'fund_page',
        falsk_g = g,
        global_vars = {
            'intro':'content/fund_page/intro.html',
            'in_plain_english':'content/fund_page/in_plain_english.html',
            'full_model_description':'content/fund_page/full_model_description.html',
            'whatif_intro':'content/fund_page/whatif_intro.html'},
    )