from app import app
from app.forms import create_investment_parameters_form
from app.routes.lib import get_client_ip
from app.routes.calc_page_workflow import render_calc_page
from flask import g
from flask_login import login_required


@app.route('/property', methods=['GET', 'POST'])
@login_required
def property_page():
    form = create_investment_parameters_form(groups=['base', 'property'])
    return render_calc_page(
        cloud_run_route='calc_property',
        calc_name = 'property',
        ip = get_client_ip(app),
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