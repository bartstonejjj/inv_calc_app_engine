from app import app
from app.forms import create_investment_parameters_form
from app.routes.lib import get_client_ip
from app.routes.calc_page_workflow import render_calc_page
from flask import g
from flask_login import login_required


@app.route('/peer_to_peer', methods=['GET', 'POST'])
@login_required
def p2p_page():
    form = create_investment_parameters_form(groups=['base', 'savings', 'p2p'])
    return render_calc_page(
        cloud_run_route = 'calc_p2p',
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