from app import app
from app.routes.calc_page_workflow import render_calc_page
from app.routes.lib import load_global_vars, get_client_ip
from flask import g, request
from flask_login import login_required

# For running and displaying models and dynamic text
from investment_models.pages.p2p import P2PVars
from text_lib import *

def html_vars(form, res):
    ans = {}
    ans['title'] = 'Home'
    ans['form'] = form
    ans['data'] = res.summary.applymap(signifigicant_figures_str)
    ans['metrics'] = res.metrics_descriptions
    ans['investments'] = res.investments_descriptions
    ans['dataframe'] = res.df_p2p.applymap(signifigicant_figures_str)
    ans['dataframe_name'] = 'P2P reinvest into saving'
    ans['capital'] = form.capital.data
    ans['years'] = form.years.data
    ans['p2p_rate'] = form.p2p_rate.data
    ans['savings_rate'] = form.savings_rate.data
    s = res.s_p2p_reinvest_savings # For the In plain english descriptions
    ans['payback_period'] = s['Payback period (years)']
    ans['payback_period_words'] = years_in_words(s['Payback period (years)'])
    ans['balance'] = int(s['Final investment value'])
    ans['roi'] = s['Investment increase (%)']
    ans['ci_equiv'] = s['Compound interest (%)']

    return apply_signifigicant_figures_str_to_dict(ans)

@app.route('/peer_to_peer', methods=['GET', 'POST'])
@login_required
def p2p_page():
    return render_calc_page(
        form_groups = ['base', 'savings', 'p2p'], 
        calc_name = 'p2p',
        ip = get_client_ip(app), 
        CalcVars = P2PVars, 
        html_file = 'p2p.html', 
        cache_name = 'p2p_page', 
        html_vars = html_vars,
        falsk_g = g,
        global_vars = {
            'intro':'content/p2p_page/intro.html',
            'in_plain_english':'content/p2p_page/in_plain_english.html',
            'full_model_description':'content/p2p_page/full_model_description.html'})