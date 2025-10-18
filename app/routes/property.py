from app import app
from app.forms import create_investment_parameters_form
from app.routes.lib import load_global_vars, get_model_labels, get_client_ip
from app.routes.calc_page_workflow import render_calc_page
from flask import g, render_template, request
from flask_login import login_required
from app.routes.plot import create_whatif_df_svg

# For running and displaying models and dynamic text
from investment_models.pages.property import HomeBuyingVars
from text_lib import *
from flask import session

import pandas as pd

def html_vars(form, res):
    ans = {}
    ans['title'] = 'Home'
    ans['form'] = form
    ans['data'] = res.summary.applymap(signifigicant_figures_str)
    ans['metrics'] = res.metrics_descriptions
    ans['dataframe'] = res.df.applymap(signifigicant_figures_str)
    ans['dataframe_name'] = 'Buying your home'
    ans['capital'] = form.capital.data
    ans['years'] = form.years.data
    ans['property_cost'] = form.property_cost.data
    ans['mortgage_rate'] = form.mortgage_rate.data
    ans['property_growth'] = form.property_growth.data
    ans['mortgage_years'] = form.mortgage_years.data
    ans['rent_or_buy'] = res.rent_or_buy
    ans['payback_period'] = res.payback_period
    ans['payback_period_words'] = years_in_words(res.payback_period)
    ans['non_home_returns'] = form.non_home_returns.data
    ans['principal'] = res.principal
    ans['monthly_repayment'] = int(res.monthly_repayment)
    ans['balance'] = int(res.summary['Buy home']['Final investment value'])
    ans['roi_buy'] = res.summary['Buy home']['Investment increase (%)']
    ans['ci_equiv'] = res.summary['Buy home']['Compound interest (%)']
    ans['roi_rent'] = res.summary['Rent home']['Investment increase (%)']
    ans['balance_diff'] = int(abs(res.summary['Buy home']['Final investment value'] - \
        res.summary['Rent home']['Final investment value']))
    ans['roi_diff'] = int(abs(res.summary['Buy home']['Investment increase (%)'] - \
        res.summary['Rent home']['Investment increase (%)']))

    # Generate SVG for whatif plots
    for k, v in res.whatif_dfs.items():
        ans[k + '_whatif_plot'] = create_whatif_df_svg(
            page = 'property', 
            variable = k, 
            hline = 'Rent balance',
            hline_label = 'Final investment value\nRent home', 
            marker_y = 'Buy balance', 
            y_label = 'Final investment value\nBuy home'
        )

    return apply_signifigicant_figures_str_to_dict(ans)

def update_session_var(res):
    # Add session variables for whatif plots
    session['property']['whatif_dfs'] = res.whatif_dfs
    session['property']['Rent balance'] = res.summary['Rent home']['Final investment value']
    session['property']['Buy balance'] = res.summary['Buy home']['Final investment value']
    session['property']['labels'] = get_model_labels('property')

    # Add latest investment_model inputs
    session['property']['model_inputs'] = {}
    for k, v in res.inputs.items():
        session['property']['model_inputs'][k] = v

@app.route('/property', methods=['GET', 'POST'])
@login_required
def property_page():
    return render_calc_page(
        form_groups = ['base', 'property'], 
        calc_name = 'property',
        ip = get_client_ip(app), 
        CalcVars = HomeBuyingVars, 
        html_file = 'property.html', 
        cache_name = 'property_page', 
        html_vars = html_vars,
        falsk_g = g,
        global_vars = {
            'intro':'content/property_page/intro.html',
            'in_plain_english':'content/property_page/in_plain_english.html',
            'full_model_description':'content/property_page/full_model_description.html',
            'whatif_intro':'content/property_page/whatif_intro.html'},
        session_var = 'property',
        update_session_var = update_session_var)