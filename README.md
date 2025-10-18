# InvestmentCalculator_GCP
theinvestmentcalculator.com deployed over GCP



# Local

add environment variables in .env

download service key an set path to environement variable GOOGLE_APPLICATION_CREDENTIALS




# Production

add environment variables in app.yaml and dont check into code as it will contain secrets
duplicate app_template.yaml and check into code but without environment variables

add requirements.txt in requirements_local.txt also.


TODO - change secrets and re commit code