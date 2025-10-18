from app import app
from app.forms import create_investment_parameters_form
from app.routes.lib import load_global_vars, get_model_labels, get_client_ip
from app.routes.calc_page_workflow import render_calc_page
from flask import g, render_template, request
from flask_login import login_required
from app.routes.plot import create_whatif_df_svg

# For running and displaying models and dynamic text
from investment_models.pages.fund import FundVars
from text_lib import *
from flask import session

def html_vars(form, res):
    ans = {}
    ans['title'] = 'Home'
    ans['form'] = form
    ans['data'] = res.summary.applymap(signifigicant_figures_str)
    ans['metrics'] = res.metrics_descriptions
    ans['dataframe'] = res.df.applymap(signifigicant_figures_str)
    ans['dataframe_name'] = 'Fund'
    ans['capital'] = form.capital.data
    ans['years'] = form.years.data
    ans['earnings'] = form.earnings.data
    ans['mgmt_fee'] = form.mgmt_fee.data
    ans['annual_fee'] = form.annual_fee.data
    s = res.s_fund # For the In plain english descriptions
    ans['payback_period'] = s['Payback period (years)']
    ans['payback_period_words'] = years_in_words(s['Payback period (years)'])
    ans['balance'] = int(s['Final investment value'])
    ans['roi'] = s['Investment increase (%)']
    ans['compound_interest'] = s['Compound interest (%)']

    # Generate SVG for whatif plots
    for k, v in res.whatif_dfs.items():
        ans[k + '_whatif_plot'] = create_whatif_df_svg(
            page = 'fund', 
            variable = k, 
            marker_y = 'Fund balance', 
            y_label = 'Final investment value\nFund'
        )

    return apply_signifigicant_figures_str_to_dict(ans)

def update_session_var(res):
    # Add session variables for whatif plots
    session['fund']['whatif_dfs'] = res.whatif_dfs
    session['fund']['Fund balance'] = res.summary['Fund']['Final investment value']
    session['fund']['labels'] = get_model_labels('fund')

    # Add latest investment_model inputs
    session['fund']['model_inputs'] = {}
    for k, v in res.inputs.items():
        session['fund']['model_inputs'][k] = v

@app.route('/fund', methods=['GET', 'POST'])
@login_required
def fund_page():
    form = create_investment_parameters_form(groups=['base', 'fund'])
    return render_calc_page(
        form = form,
        calc_name = 'fund',
        ip = get_client_ip(app),
        CalcVars = FundVars,
        html_file = 'fund.html',
        cache_name = 'fund_page',
        html_vars = html_vars,
        falsk_g = g,
        global_vars = {
            'intro':'content/fund_page/intro.html',
            'in_plain_english':'content/fund_page/in_plain_english.html',
            'full_model_description':'content/fund_page/full_model_description.html',
            'whatif_intro':'content/fund_page/whatif_intro.html'},
        session_var = 'fund',
        update_session_var = update_session_var)


# import requests
# from flask import Response
#
# @app.route('/fund', methods=['GET', 'POST'])
# @login_required
# def fund_page():
#     print('app engine')
#     resp = requests.get("http://127.0.0.1:5001/fund")
#     return Response(resp.text, mimetype='text/html')
