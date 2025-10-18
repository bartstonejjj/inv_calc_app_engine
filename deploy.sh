#! /bin/bash
gcloud auth activate-service-account --key-file="$HOME/inv_calc_gcp_key.json"
gcloud config set project inv-calc-gcp
gcloud app deploy app.yaml
