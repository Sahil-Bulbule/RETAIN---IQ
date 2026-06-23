"""
IBM HR Employee Attrition Prediction - Streamlit Application
A professional HR dashboard with clean premium UI
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import warnings
import os
import joblib
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Retain IQ",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Clean Premium UI
def load_css():
    st.markdown("""
    <style>
        /* Hide sidebar toggle button */
        .css-1lsmgbg, .css-1lsmgbg:hover, .css-1lsmgbg:focus {
            display: none !important;
        }
        
        /* Hide the sidebar completely */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Clean Premium Background */
        .stApp {
            background: linear-gradient(135deg, #0c0c1d 0%, #1a1a2e 50%, #16213e 100%);
        }
        
        /* Premium Header */
        .header {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            padding: 35px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.8em;
            font-weight: 300;
            margin: 0;
            color: #ffffff;
            letter-spacing: 2px;
        }
        
        .header h1 span {
            color: #ffd700;
            font-weight: 600;
        }
        
        .header p {
            color: rgba(255, 255, 255, 0.6);
            font-size: 1.1em;
            margin-top: 8px;
            letter-spacing: 1px;
            font-weight: 300;
        }
        
        /* Premium Glass Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            padding: 24px;
            margin: 12px 0;
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 215, 0, 0.15);
        }
        
        /* Premium Labels */
        .metric-label {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.75em;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: 300;
            color: #ffffff;
            margin-top: 5px;
        }
        
        .metric-value.gold {
            color: #ffd700;
        }
        .metric-value.green {
            color: #00d4aa;
        }
        .metric-value.red {
            color: #ff6b6b;
        }
        
        /* Premium Button */
        .stButton > button {
            background: linear-gradient(135deg, #ffd700, #f0a500);
            color: #0c0c1d;
            font-size: 1.2em;
            font-weight: 600;
            padding: 18px 40px;
            border: none;
            border-radius: 12px;
            transition: all 0.3s ease;
            width: 100%;
            height: 65px;
            letter-spacing: 1px;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(255, 215, 0, 0.2);
        }
        
        /* Premium Input Fields */
        .stSelectbox, .stNumberInput, .stSlider {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            margin-bottom: 8px !important;
            padding: 6px 10px !important;
        }
        
        .stSelectbox > div, .stNumberInput > div, .stSlider > div {
            padding: 2px 0 !important;
        }
        
        .stSelectbox label, .stNumberInput label, .stSlider label {
            padding: 0 0 8px 0 !important;
            color: rgba(255, 255, 255, 0.7) !important;
            font-weight: 400 !important;
            display: block !important;
            margin: 0 !important;
            line-height: 1.2 !important;
        }
        
        .stNumberInput input {
            padding: 8px 12px !important;
            min-height: 38px !important;
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
        }
        
        .stNumberInput input:focus {
            border-color: #ffd700 !important;
            box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.1) !important;
        }
        
        .stSelectbox select {
            padding: 8px 12px !important;
            min-height: 38px !important;
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
        }
        
        .stSelectbox select:focus {
            border-color: #ffd700 !important;
        }
        
        .stSelectbox:hover, .stNumberInput:hover, .stSlider:hover {
            border-color: rgba(255, 215, 0, 0.2);
        }
        
        .stSlider > div > div {
            padding: 8px 0 !important;
        }
        
        .stSlider input {
            padding: 8px 0 !important;
        }
        
        /* Premium Section Headers */
        .section-header {
            color: #ffffff;
            font-size: 1.4em;
            font-weight: 300;
            margin: 25px 0 15px 0;
            letter-spacing: 1px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .section-header span {
            color: #ffd700;
            margin-right: 10px;
        }
        
        /* Premium Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 215, 0, 0.3);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 215, 0, 0.5);
        }
        
        /* Risk Colors */
        .risk-low { 
            color: #00d4aa; 
            font-weight: 500;
        }
        .risk-medium { 
            color: #ffd700; 
            font-weight: 500;
        }
        .risk-high { 
            color: #ff6b6b; 
            font-weight: 500;
        }
        
        /* Premium Divider */
        .premium-divider {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.15), transparent);
            margin: 30px 0;
        }
        
        /* Prediction Cards - Fixed for perfect alignment */
        .prediction-card-wrapper {
            display: flex;
            gap: 15px;
            width: 100%;
            margin: 10px 0;
        }
        
        .prediction-card-item {
            flex: 1;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 20px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        
        .prediction-card-item:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 215, 0, 0.15);
        }
        
        .prediction-card-item .label {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.75em;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .prediction-card-item .value {
            font-size: 2.5em;
            font-weight: 300;
            margin-top: 5px;
        }
        
        .prediction-card-item .value.green {
            color: #00d4aa;
        }
        
        .prediction-card-item .value.red {
            color: #ff6b6b;
        }
        
        .prediction-card-item .value.gold {
            color: #ffd700;
        }
        
        .prediction-card-item .value.white {
            color: #ffffff;
        }
        
        .prediction-stay {
            border-color: rgba(0, 212, 170, 0.3) !important;
            background: rgba(0, 212, 170, 0.08) !important;
        }
        
        .prediction-leave {
            border-color: rgba(255, 107, 107, 0.3) !important;
            background: rgba(255, 107, 107, 0.08) !important;
        }
        
        /* Premium Form Container */
        .form-container {
            background: rgba(255, 255, 255, 0.02);
            padding: 20px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.04);
        }
        
        /* Premium List Items */
        .list-item {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: rgba(255, 255, 255, 0.8);
            list-style: none !important;
        }
        
        .list-item:last-child {
            border-bottom: none;
        }
        
        .list-item.danger {
            color: #ff6b6b;
        }
        
        .list-item.success {
            color: #00d4aa;
        }
        
        .list-item.warning {
            color: #ffd700;
        }
        
        ul {
            list-style-type: none !important;
            padding-left: 0 !important;
        }
        
        .main-content {
            padding: 0 10px;
        }
        
        .row-widget.stColumns {
            gap: 15px !important;
        }
        
        .stSelectbox > div > div {
            min-height: 38px !important;
        }
        
        .stNumberInput > div > div {
            min-height: 38px !important;
        }
        
        .stSlider > div {
            padding: 8px 0 !important;
        }
        
        .stSelectbox > div, .stNumberInput > div {
            padding: 0 !important;
        }
        
        .stSelectbox, .stNumberInput, .stSlider {
            padding: 8px 12px 10px 12px !important;
            margin-bottom: 10px !important;
        }
        
        .css-1offfwp {
            padding: 0 5px !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Load file with multiple methods
def load_pickle_file(file_path):
    """Load a pickle file with multiple methods"""
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except:
        try:
            return joblib.load(file_path)
        except:
            for protocol in [4, 3, 2, 1, 0]:
                try:
                    with open(file_path, 'rb') as f:
                        return pickle.load(f)
                except:
                    continue
            raise Exception(f"Could not load {file_path}")

# Load model and preprocessors
@st.cache_resource
def load_model_artifacts():
    """Load the ANN model, scaler, and feature columns"""
    try:
        required_files = ['ann_model.pkl', 'an_scaler.pkl', 'ann_columns.pkl']
        missing_files = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            st.error("❌ Missing required files!")
            st.info("Please make sure the following files are in the same directory:")
            for file in missing_files:
                st.write(f"- {file}")
            st.stop()
        
        model = load_pickle_file('ann_model.pkl')
        scaler = load_pickle_file('an_scaler.pkl')
        columns = load_pickle_file('ann_columns.pkl')
        
        return model, scaler, columns
        
    except Exception as e:
        st.error(f"❌ Error loading model artifacts: {e}")
        st.stop()

# Create input form
def create_input_form():
    """Create the employee input form with all required features"""
    
    st.markdown("""
    <div style='background: rgba(255,255,255,0.02); padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.04); margin-bottom: 25px;'>
        <h2 style='color: #ffffff; margin: 0; font-weight: 300; letter-spacing: 1px;'>📝 Employee Information</h2>
        <p style='color: rgba(255,255,255,0.4); margin: 8px 0 0 0; font-size: 0.9em;'>Enter employee details for attrition risk prediction</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Information Section
    st.markdown('<div class="section-header"><span>👤</span> Personal Information</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=65, value=30, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
    
    with col2:
        education = st.selectbox("Education Level", 
                                [1, 2, 3, 4, 5],
                                format_func=lambda x: {1: "Below College", 2: "College", 3: "Bachelor", 
                                                      4: "Master", 5: "Doctor"}.get(x, str(x)))
        education_field = st.selectbox("Education Field", 
                                      ["Life Sciences", "Medical", "Marketing", "Technical Degree", 
                                       "Human Resources", "Other"])
        total_working_years = st.number_input("Total Working Years", min_value=0, max_value=40, value=10, step=1)
    
    with col3:
        years_at_company = st.number_input("Years at Company", min_value=0, max_value=40, value=5, step=1)
        years_in_current_role = st.number_input("Years in Current Role", min_value=0, max_value=20, value=3, step=1)
        years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0, max_value=15, value=2, step=1)
    
    # Job Information Section
    st.markdown('<div class="section-header"><span>💼</span> Job Information</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        department = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
        job_role = st.selectbox("Job Role", 
                               ["Sales Executive", "Research Scientist", "Laboratory Technician", 
                                "Manufacturing Director", "Healthcare Representative", "Manager", 
                                "Sales Representative", "Research Director", "Human Resources"])
        job_level = st.number_input("Job Level", min_value=1, max_value=5, value=2, step=1)
    
    with col2:
        job_involvement = st.selectbox("Job Involvement", [1, 2, 3, 4],
                                      format_func=lambda x: {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}.get(x, str(x)))
        job_satisfaction = st.selectbox("Job Satisfaction", [1, 2, 3, 4],
                                       format_func=lambda x: {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}.get(x, str(x)))
        environment_satisfaction = st.selectbox("Environment Satisfaction", [1, 2, 3, 4],
                                               format_func=lambda x: {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}.get(x, str(x)))
    
    with col3:
        relationship_satisfaction = st.selectbox("Relationship Satisfaction", [1, 2, 3, 4],
                                                format_func=lambda x: {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}.get(x, str(x)))
        work_life_balance = st.selectbox("Work Life Balance", [1, 2, 3, 4],
                                        format_func=lambda x: {1: "Poor", 2: "Good", 3: "Better", 4: "Best"}.get(x, str(x)))
        overtime = st.selectbox("Overtime", ["No", "Yes"])
    
    # Compensation Section
    st.markdown('<div class="section-header"><span>💰</span> Compensation & Performance</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=500)
        monthly_rate = st.number_input("Monthly Rate", min_value=1000, max_value=25000, value=10000, step=500)
        daily_rate = st.number_input("Daily Rate", min_value=100, max_value=1500, value=800, step=50)
    
    with col2:
        hourly_rate = st.number_input("Hourly Rate", min_value=30, max_value=200, value=65, step=5)
        percent_salary_hike = st.slider("Percent Salary Hike", min_value=10, max_value=25, value=15, step=1)
        performance_rating = st.selectbox("Performance Rating", [1, 2, 3, 4],
                                         format_func=lambda x: {1: "Low", 2: "Good", 3: "Excellent", 4: "Outstanding"}.get(x, str(x)))
    
    with col3:
        stock_option_level = st.number_input("Stock Option Level", min_value=0, max_value=3, value=1, step=1)
        num_companies_worked = st.number_input("Number of Companies Worked", min_value=0, max_value=10, value=2, step=1)
        training_times_last_year = st.number_input("Training Times Last Year", min_value=0, max_value=10, value=2, step=1)
    
    # Work Details Section
    st.markdown('<div class="section-header"><span>📊</span> Work Details</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        years_with_curr_manager = st.number_input("Years With Current Manager", min_value=0, max_value=20, value=4, step=1)
        distance_from_home = st.number_input("Distance From Home (km)", min_value=1, max_value=50, value=10, step=1)
        business_travel = st.selectbox("Business Travel", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
    
    # Collect all inputs in a dictionary
    input_data = {
        'Age': age,
        'DailyRate': daily_rate,
        'DistanceFromHome': distance_from_home,
        'Education': education,
        'EnvironmentSatisfaction': environment_satisfaction,
        'HourlyRate': hourly_rate,
        'JobInvolvement': job_involvement,
        'JobLevel': job_level,
        'JobSatisfaction': job_satisfaction,
        'MonthlyIncome': monthly_income,
        'MonthlyRate': monthly_rate,
        'NumCompaniesWorked': num_companies_worked,
        'PercentSalaryHike': percent_salary_hike,
        'PerformanceRating': performance_rating,
        'RelationshipSatisfaction': relationship_satisfaction,
        'StockOptionLevel': stock_option_level,
        'TotalWorkingYears': total_working_years,
        'TrainingTimesLastYear': training_times_last_year,
        'WorkLifeBalance': work_life_balance,
        'YearsAtCompany': years_at_company,
        'YearsInCurrentRole': years_in_current_role,
        'YearsSinceLastPromotion': years_since_last_promotion,
        'YearsWithCurrManager': years_with_curr_manager,
        'Gender': gender,
        'OverTime': overtime,
        'BusinessTravel': business_travel,
        'Department': department,
        'EducationField': education_field,
        'JobRole': job_role,
        'MaritalStatus': marital_status
    }
    
    return input_data

# Preprocess input data
def preprocess_input(input_data, columns, scaler):
    """Convert input to one-hot encoded format and scale"""
    try:
        df = pd.DataFrame([input_data])
        categorical_cols = ['Gender', 'OverTime', 'BusinessTravel', 'Department', 
                           'EducationField', 'JobRole', 'MaritalStatus']
        
        df_encoded = pd.get_dummies(df, columns=categorical_cols)
        
        for col in columns:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        df_encoded = df_encoded.reindex(columns=columns, fill_value=0)
        df_scaled = scaler.transform(df_encoded)
        
        return df_scaled, df_encoded
    
    except Exception as e:
        st.error(f"❌ Error preprocessing data: {e}")
        return None, None

# Make prediction
def predict_attrition(model, scaled_data):
    """Make attrition prediction using Keras model"""
    try:
        prediction_prob = model.predict(scaled_data, verbose=0)
        
        if len(prediction_prob.shape) == 2:
            if prediction_prob.shape[1] == 2:
                probability = float(prediction_prob[0][1])
                prediction = 1 if probability > 0.5 else 0
            else:
                probability = float(prediction_prob[0][0])
                prediction = 1 if probability > 0.5 else 0
        else:
            probability = float(prediction_prob[0])
            prediction = 1 if probability > 0.5 else 0
        
        probability = max(0, min(1, probability))
        return prediction, probability
    except Exception as e:
        st.error(f"❌ Error making prediction: {e}")
        return None, None

# Generate insights
def generate_insights(input_data, prediction, probability):
    """Generate insights and recommendations based on employee data"""
    
    insights = {
        'risk_factors': [],
        'recommendations': [],
        'score': 0
    }
    
    # Risk factor analysis
    if input_data['OverTime'] == 'Yes':
        insights['risk_factors'].append("Frequent Overtime")
        insights['score'] += 20
    
    if input_data['JobSatisfaction'] <= 2:
        insights['risk_factors'].append("Low Job Satisfaction")
        insights['score'] += 15
    
    if input_data['WorkLifeBalance'] <= 2:
        insights['risk_factors'].append("Poor Work Life Balance")
        insights['score'] += 15
    
    if input_data['DistanceFromHome'] > 20:
        insights['risk_factors'].append("Long Distance From Home")
        insights['score'] += 10
    
    if input_data['EnvironmentSatisfaction'] <= 2:
        insights['risk_factors'].append("Low Environment Satisfaction")
        insights['score'] += 10
    
    if input_data['PercentSalaryHike'] < 15:
        insights['risk_factors'].append("Low Salary Growth")
        insights['score'] += 10
    
    if input_data['YearsAtCompany'] > 10 and input_data['NumCompaniesWorked'] < 2:
        insights['risk_factors'].append("Few Promotion Opportunities")
        insights['score'] += 10
    
    if input_data['YearsSinceLastPromotion'] > 5:
        insights['risk_factors'].append("Long Time Since Last Promotion")
        insights['score'] += 10
    
    if input_data['JobInvolvement'] <= 2:
        insights['risk_factors'].append("Low Job Involvement")
        insights['score'] += 5
    
    # Risk category based on score and probability
    risk_score = min(100, insights['score'] + int(probability * 50))
    risk_category = "Low Risk" if risk_score < 40 else "Medium Risk" if risk_score < 70 else "High Risk"
    
    # Generate recommendations
    if input_data['PercentSalaryHike'] < 15:
        insights['recommendations'].append("Salary Review")
    if input_data['JobSatisfaction'] <= 2:
        insights['recommendations'].append("Career Development Plan")
    if input_data['YearsAtCompany'] > 5 and input_data['NumCompaniesWorked'] < 2:
        insights['recommendations'].append("Promotion Discussion")
    if input_data['WorkLifeBalance'] <= 2:
        insights['recommendations'].append("Employee Wellness Program")
    if input_data['DistanceFromHome'] > 20:
        insights['recommendations'].append("Flexible Work Arrangement")
    if input_data['TrainingTimesLastYear'] < 2:
        insights['recommendations'].append("Skill Development Training")
    if input_data['YearsSinceLastPromotion'] > 5:
        insights['recommendations'].append("Career Growth Planning")
    if input_data['JobInvolvement'] <= 2:
        insights['recommendations'].append("Engagement Activities")
    
    insights['risk_score'] = risk_score
    insights['risk_category'] = risk_category
    
    return insights

# Create Risk Meter
def create_risk_meter(probability):
    """Create a clean risk meter gauge"""
    try:
        risk_score = int(probability * 100)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Meter", 'font': {'size': 20, 'color': '#ffffff'}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': 'rgba(255,255,255,0.3)',
                        'tickfont': {'color': 'rgba(255,255,255,0.5)'}},
                'bar': {'color': "#ffd700"},
                'bgcolor': "rgba(0,0,0,0.3)",
                'borderwidth': 1,
                'bordercolor': "rgba(255,255,255,0.1)",
                'steps': [
                    {'range': [0, 33], 'color': 'rgba(0, 212, 170, 0.15)'},
                    {'range': [33, 66], 'color': 'rgba(255, 215, 0, 0.15)'},
                    {'range': [66, 100], 'color': 'rgba(255, 107, 107, 0.15)'}
                ],
                'threshold': {
                    'line': {'color': "#ff6b6b", 'width': 3},
                    'thickness': 0.7,
                    'value': risk_score
                }
            }
        ))
        
        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#ffffff'}
        )
        
        return fig
    except Exception as e:
        return None

# Display prediction results
def display_results(prediction, probability, input_data, insights):
    """Display all prediction results and insights"""
    
    risk_score = insights['risk_score']
    risk_category = insights['risk_category']
    
    # Determine risk color
    risk_color = {'Low Risk': '#00d4aa', 'Medium Risk': '#ffd700', 'High Risk': '#ff6b6b'}[risk_category]
    risk_class = {'Low Risk': 'risk-low', 'Medium Risk': 'risk-medium', 'High Risk': 'risk-high'}[risk_category]
    
    # Main results - Using HTML for perfect alignment
    st.markdown('<div class="section-header"><span>📊</span> Prediction Results</div>', unsafe_allow_html=True)
    
    # Create three cards in a row using HTML
    if prediction == 0:
        pred_class = "prediction-stay"
        pred_value = "✓ Stay"
        pred_color = "green"
    else:
        pred_class = "prediction-leave"
        pred_value = "⚠ Leave"
        pred_color = "red"
    
    confidence = max(probability, 1-probability)
    
    st.markdown(f"""
    <div class="prediction-card-wrapper">
        <div class="prediction-card-item {pred_class}">
            <div class="label">PREDICTION</div>
            <div class="value {pred_color}">{pred_value}</div>
        </div>
        <div class="prediction-card-item">
            <div class="label">ATTRITION PROBABILITY</div>
            <div class="value gold">{probability:.1%}</div>
        </div>
        <div class="prediction-card-item">
            <div class="label">CONFIDENCE SCORE</div>
            <div class="value white">{confidence:.1%}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Risk Meter
    st.markdown('<div class="section-header"><span>🎯</span> Risk Meter</div>', unsafe_allow_html=True)
    fig = create_risk_meter(probability)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.metric("Risk Score", f"{int(probability * 100)}%")
    
    # Attrition Risk Diagnostic
    st.markdown('<div class="section-header"><span>🔍</span> Attrition Risk Diagnostic</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='glass-card'>
            <div style='color: rgba(255,255,255,0.6); font-size: 0.9em; margin-bottom: 15px;'>RISK FACTORS</div>
            <ul style='list-style-type: none !important; padding-left: 0 !important; margin: 0;'>
        """, unsafe_allow_html=True)
        
        if insights['risk_factors']:
            for factor in insights['risk_factors']:
                st.markdown(f"<li class='list-item danger'>⚠ {factor}</li>", unsafe_allow_html=True)
        else:
            st.markdown("<li class='list-item success'>✓ No significant risk factors identified</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='glass-card'>
            <div style='color: rgba(255,255,255,0.6); font-size: 0.9em; margin-bottom: 15px;'>RECOMMENDATIONS</div>
            <ul style='list-style-type: none !important; padding-left: 0 !important; margin: 0;'>
        """, unsafe_allow_html=True)
        
        if insights['recommendations']:
            for rec in insights['recommendations']:
                st.markdown(f"<li class='list-item warning'>💡 {rec}</li>", unsafe_allow_html=True)
        else:
            st.markdown("<li class='list-item success'>✓ No immediate recommendations needed</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    # Key Employee Insights
    st.markdown('<div class="section-header"><span>📊</span> Key Employee Insights</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='glass-card'>
            <div class='metric-label'>Age Group</div>
            <div class='metric-value' style='font-size: 1.4em;'>{input_data['Age']} years</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        income_category = "Low" if input_data['MonthlyIncome'] < 3000 else "Medium" if input_data['MonthlyIncome'] < 7000 else "High"
        st.markdown(f"""
        <div class='glass-card'>
            <div class='metric-label'>Income Category</div>
            <div class='metric-value' style='font-size: 1.4em;'>{income_category}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        experience_level = "Entry" if input_data['TotalWorkingYears'] < 5 else "Mid" if input_data['TotalWorkingYears'] < 15 else "Senior"
        st.markdown(f"""
        <div class='glass-card'>
            <div class='metric-label'>Experience Level</div>
            <div class='metric-value' style='font-size: 1.4em;'>{experience_level}</div>
        </div>
        """, unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        promotion_status = "Eligible" if input_data['YearsAtCompany'] > 3 else "Not Eligible"
        color = "#00d4aa" if promotion_status == "Eligible" else "#ff6b6b"
        st.markdown(f"""
        <div class='glass-card'>
            <div class='metric-label'>Promotion Status</div>
            <div class='metric-value' style='font-size: 1.4em; color: {color};'>{promotion_status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        wl_score = min(100, input_data['WorkLifeBalance'] * 25)
        wl_color = "#00d4aa" if wl_score >= 75 else "#ffd700" if wl_score >= 50 else "#ff6b6b"
        st.markdown(f"""
        <div class='glass-card'>
            <div class='metric-label'>Work-Life Health Score</div>
            <div class='metric-value' style='font-size: 1.4em; color: {wl_color};'>{wl_score}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        engagement_score = min(100, (input_data['JobSatisfaction'] * 20 + input_data['EnvironmentSatisfaction'] * 20) // 2)
        eng_color = "#00d4aa" if engagement_score >= 75 else "#ffd700" if engagement_score >= 50 else "#ff6b6b"
        st.markdown(f"""
        <div class='glass-card'>
            <div class='metric-label'>Engagement Score</div>
            <div class='metric-value' style='font-size: 1.4em; color: {eng_color};'>{engagement_score}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Employee Summary Card
    st.markdown('<div class="section-header"><span>📋</span> Employee Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class='glass-card'>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 5px 0;'>
            <div>
                <div style='color: rgba(255,255,255,0.4); font-size: 0.7em; text-transform: uppercase; letter-spacing: 1px;'>Risk Category</div>
                <div style='font-size: 1.3em; font-weight: 500; margin-top: 5px;' class='{risk_class}'>{risk_category}</div>
            </div>
            <div>
                <div style='color: rgba(255,255,255,0.4); font-size: 0.7em; text-transform: uppercase; letter-spacing: 1px;'>Risk Score</div>
                <div style='font-size: 1.3em; font-weight: 500; margin-top: 5px; color: #ffd700;'>{risk_score}%</div>
            </div>
            <div>
                <div style='color: rgba(255,255,255,0.4); font-size: 0.7em; text-transform: uppercase; letter-spacing: 1px;'>Top Risk Factors</div>
                <div style='font-size: 0.95em; margin-top: 5px; color: rgba(255,255,255,0.8);'>
                    {', '.join(insights['risk_factors'][:2]) if insights['risk_factors'] else 'None identified'}
                </div>
            </div>
            <div>
                <div style='color: rgba(255,255,255,0.4); font-size: 0.7em; text-transform: uppercase; letter-spacing: 1px;'>HR Action Required</div>
                <div style='font-size: 1em; font-weight: 500; margin-top: 5px; color: {"#ff6b6b" if risk_category == "High Risk" else "#ffd700" if risk_category == "Medium Risk" else "#00d4aa"};'>
                    {"🚨 Immediate Attention" if risk_category == "High Risk" else "📊 Monitor Closely" if risk_category == "Medium Risk" else "✅ Routine Review"}
                </div>
            </div>
            <div>
                <div style='color: rgba(255,255,255,0.4); font-size: 0.7em; text-transform: uppercase; letter-spacing: 1px;'>Employee Snapshot</div>
                <div style='font-size: 0.95em; margin-top: 5px; color: rgba(255,255,255,0.8);'>
                    Age: {input_data['Age']} | Tenure: {input_data['YearsAtCompany']} yrs
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main application
def main():
    """Main application entry point"""
    
    # Load CSS
    load_css()
    
    # Header
    st.markdown("""
    <div class='header'>
        <h1>💼 Retain <span>I</span>Q 💼</h1>
        <p>Employee Attrition & Retention Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model artifacts (silently)
    model, scaler, columns = load_model_artifacts()
    
    # Main content area
    st.markdown("""
    <div style='background: rgba(0,0,0,0.15); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.03);'>
    """, unsafe_allow_html=True)
    
    # Create input form
    input_data = create_input_form()
    
    # Prediction button
    st.markdown("<br>", unsafe_allow_html=True)
    predict_button = st.button("🔍 Analyze Employee", use_container_width=True)
    
    if predict_button:
        with st.spinner("Analyzing employee data..."):
            scaled_data, encoded_df = preprocess_input(input_data, columns, scaler)
            
            if scaled_data is not None:
                prediction, probability = predict_attrition(model, scaled_data)
                
                if prediction is not None:
                    insights = generate_insights(input_data, prediction, probability)
                    st.markdown("<hr class='premium-divider'>", unsafe_allow_html=True)
                    display_results(prediction, probability, input_data, insights)
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()