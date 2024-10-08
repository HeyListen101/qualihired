import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import streamlit as st

st.set_page_config(page_title='QualiHired', page_icon='qualihired_icon.png', layout='wide', initial_sidebar_state='collapsed', menu_items=None)
left, right = st.columns(2, gap='medium')

# Define universe of discourse (range) for technical and soft skills
technical_range = np.arange(0, 101, 2.5)
soft_range = np.arange(0, 101, 2.5)
employability_range = np.arange(0, 101, 2.5)

# Define linguistic variables: technical skills, soft skills, and employability
technical = ctrl.Antecedent(technical_range, 'Technical Skills')
soft = ctrl.Antecedent(soft_range, 'Soft Skills')
employability = ctrl.Consequent(employability_range, 'Employability')

# Define membership functions for technical skills
technical['Poor'] = fuzz.trapmf(technical_range, [0, 0, 30, 55])
technical['Fair'] = fuzz.trimf(technical_range, [50, 60, 70])
technical['Average'] = fuzz.trimf(technical_range, [62.5, 72.5, 82.5])
technical['Very Good'] = fuzz.trimf(technical_range, [80, 87.5, 95])
technical['Excellent'] = fuzz.trapmf(technical_range, [88, 94, 100, 100])

# Define membership functions for soft skills
soft['Poor'] = fuzz.trapmf(technical_range, [0, 0, 20, 60])
soft['Fair'] = fuzz.trimf(technical_range, [50, 60, 70])
soft['Average'] = fuzz.trimf(technical_range, [65, 75, 85])
soft['Very Good'] = fuzz.trimf(technical_range, [82.5, 87.5, 92.5])
soft ['Excellent'] = fuzz.trapmf(technical_range, [90, 95, 100, 100])

# Define membership functions for employability (output)
employability['Very Low'] = fuzz.trapmf(technical_range, [0, 0, 50, 65])
employability['Low'] = fuzz.trimf(technical_range, [60, 70, 80])
employability['Moderate'] = fuzz.trimf(technical_range, [75, 80, 85])
employability['High'] = fuzz.trimf(technical_range, [82.5, 87.5, 92.5])
employability['Very High'] = fuzz.trapmf(technical_range, [90, 95, 100, 100])

# Define fuzzy rules
rule1 = ctrl.Rule(technical['Poor'] & soft['Poor'], employability['Very Low'])
rule2 = ctrl.Rule(technical['Poor'] & soft['Fair'], employability['Very Low'])
rule3 = ctrl.Rule(technical['Poor'] & soft['Average'], employability['Very Low'])
rule4 = ctrl.Rule(technical['Poor'] & soft['Very Good'], employability['Low'])
rule5 = ctrl.Rule(technical['Poor'] & soft['Excellent'], employability['Moderate'])
rule6 = ctrl.Rule(technical['Fair'] & soft['Poor'], employability['Very Low'])
rule7 = ctrl.Rule(technical['Fair'] & soft['Fair'], employability['Very Low'])
rule8 = ctrl.Rule(technical['Fair'] & soft['Average'], employability['Low'])
rule9 = ctrl.Rule(technical['Fair'] & soft['Very Good'], employability['Moderate'])
rule10 = ctrl.Rule(technical['Fair'] & soft['Excellent'], employability['High'])
rule11 = ctrl.Rule(technical['Average'] & soft['Poor'], employability['Very Low'])
rule12 = ctrl.Rule(technical['Average'] & soft['Fair'], employability['Low'])
rule13 = ctrl.Rule(technical['Average'] & soft['Average'], employability['Moderate'])
rule14 = ctrl.Rule(technical['Average'] & soft['Very Good'], employability['Moderate'])
rule15 = ctrl.Rule(technical['Average'] & soft['Excellent'], employability['High'])
rule16 = ctrl.Rule(technical['Very Good'] & soft['Poor'], employability['Low'])
rule17 = ctrl.Rule(technical['Very Good'] & soft['Fair'], employability['Moderate'])
rule18 = ctrl.Rule(technical['Very Good'] & soft['Average'], employability['High'])
rule19 = ctrl.Rule(technical['Very Good'] & soft['Very Good'], employability['Very High'])
rule20 = ctrl.Rule(technical['Very Good'] & soft['Excellent'], employability['Very High'])
rule21 = ctrl.Rule(technical['Excellent'] & soft['Poor'], employability['Moderate'])
rule22 = ctrl.Rule(technical['Excellent'] & soft['Fair'], employability['High'])
rule23 = ctrl.Rule(technical['Excellent'] & soft['Average'], employability['Very High'])
rule24 = ctrl.Rule(technical['Excellent'] & soft['Very Good'], employability['Very High'])
rule25 = ctrl.Rule(technical['Excellent'] & soft['Excellent'], employability['Very High'])

# Create fuzzy control system
employability_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25])
employability_sim = ctrl.ControlSystemSimulation(employability_ctrl)

#Display welcome message
with left:
    st.title("Welcome to QualiHired \n :male-office-worker: :female-office-worker: :white_check_mark:")
    st.markdown("<div style='text-align: justify;'>This application uses a <strong>fuzzy logic control system</strong> to find out a job applicant\'s employability based on the rating of their technical and soft skills.</div><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: justify;'>Enter the applicant's ratings for each skill out of 100 and click the <strong>Calculate</strong> button to find out their employability rating.</div><br>", unsafe_allow_html=True)

with right:
    # Fuzzification: Provide input values
    with st.form('ratings'):
        employability_sim.input['Technical Skills'] = st.number_input('Rate the applicant\'s technical skills:', min_value=0, max_value=100)
        employability_sim.input['Soft Skills'] = st.number_input('Rate the applicant\'s soft skills:', min_value=0, max_value=100)
        calculate = st.form_submit_button('Calculate')

    if calculate:        
        # Apply fuzzy rules
        employability_sim.compute()

        # Defuzzification: Obtain crisp output
        output = employability_sim.output['Employability']
        membership_value = 0
        membership = None

        # Determine membership values for the crisp output
        employability_memberships = {
            'Very Low': fuzz.interp_membership(employability_range, employability['Very Low'].mf, output),
            'Low': fuzz.interp_membership(employability_range, employability['Low'].mf, output),
            'Moderate': fuzz.interp_membership(employability_range, employability['Moderate'].mf, output),
            'High': fuzz.interp_membership(employability_range, employability['High'].mf, output),
            'Very High': fuzz.interp_membership(employability_range, employability['Very High'].mf, output)
        }

        # Display membership values for the crisp output
        for label, value in employability_memberships.items():
            if value > membership_value:
                membership = label
                membership_value = value

        output = round(output, 2)

        if output < 75:
            result = f"""Employability Rating: :red[{membership}] (:red[{output}])"""
        elif output < 85:
            result = f"""Employability Rating: :orange[{membership}] (:orange[{output}])"""
        else:
            result = f"""Employability Rating: :green[{membership}] (:green[{output}])"""

        st.subheader(result)