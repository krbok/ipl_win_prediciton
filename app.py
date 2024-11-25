import streamlit as st
import pandas as pd
import pickle

# Page configuration
st.set_page_config(
    page_title="IPL Win Predictor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with modern dark theme inspired by Profit Pulse
st.markdown("""
    <style>
    /* Global theme */
    .stApp {
        background: linear-gradient(135deg, #1a1b2e, #2d2e47);
        color: #e0e0ff;
    }
    
    /* Header styling */
    .title-container {
        background: rgba(92, 99, 237, 0.1);
        padding: 2.5rem;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        margin: 1rem 0 2rem 0;
        text-align: center;
        border: 1px solid rgba(92, 99, 237, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Section styling */
    .section-container {
        background: rgba(92, 99, 237, 0.05);
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(92, 99, 237, 0.1);
        box-shadow: 0 4px 16px 0 rgba(31, 38, 135, 0.15);
        transition: transform 0.3s ease;
    }
    
    .section-container:hover {
        transform: translateY(-2px);
    }
    
    /* Input styling */
    .stSelectbox > div > div {
        background: rgba(92, 99, 237, 0.1) !important;
        border: 1px solid rgba(92, 99, 237, 0.2) !important;
        border-radius: 12px !important;
        color: #e0e0ff !important;
        padding: 0.5rem !important;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(92, 99, 237, 0.1) !important;
        border: 1px solid rgba(92, 99, 237, 0.2) !important;
        border-radius: 12px !important;
        color: #e0e0ff !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #5c63ed, #7c83ff) !important;
        color: white !important;
        padding: 1rem 2rem !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 15px rgba(92, 99, 237, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(92, 99, 237, 0.4) !important;
        background: linear-gradient(45deg, #7c83ff, #5c63ed) !important;
    }
    
    /* Results styling */
    .team-card {
        background: rgba(92, 99, 237, 0.1);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(92, 99, 237, 0.2);
        margin: 1rem 0;
        box-shadow: 0 4px 16px 0 rgba(31, 38, 135, 0.15);
        transition: transform 0.3s ease;
    }
    
    .team-card:hover {
        transform: translateY(-2px);
    }
    
    .stat-card {
        background: rgba(92, 99, 237, 0.1);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(92, 99, 237, 0.2);
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
    }
    
    /* Text styling */
    h1 {
        color: #e0e0ff !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2, h3, h4 {
        color: #e0e0ff !important;
        font-weight: 600 !important;
    }
    
    label {
        color: rgba(224, 224, 255, 0.8) !important;
        font-weight: 500 !important;
    }
    
    /* Progress bars */
    .prediction-progress {
        height: 24px;
        background: rgba(92, 99, 237, 0.1);
        border-radius: 12px;
        overflow: hidden;
        margin: 15px 0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .prediction-bar {
        height: 100%;
        transition: width 0.8s ease-in-out;
    }
    
    /* Error messages */
    .stAlert {
        background: rgba(255, 87, 87, 0.1) !important;
        border: 1px solid rgba(255, 87, 87, 0.2) !important;
        border-radius: 12px !important;
        color: #ffe0e0 !important;
        padding: 1rem !important;
    }
    
    /* Data display */
    .dataframe {
        background: rgba(92, 99, 237, 0.05) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(92, 99, 237, 0.1) !important;
    }
    
    .dataframe th {
        background: rgba(92, 99, 237, 0.1) !important;
        color: #e0e0ff !important;
        padding: 12px !important;
    }
    
    .dataframe td {
        color: #e0e0ff !important;
        padding: 12px !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(92, 99, 237, 0.1);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(92, 99, 237, 0.3);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(92, 99, 237, 0.4);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #5c63ed !important;
    }
    
    /* Toggle switch */
    .stCheckbox > div > label > div {
        background-color: rgba(92, 99, 237, 0.3) !important;
    }
    
    .stCheckbox > div > label > div[data-checked="true"] {
        background-color: #5c63ed !important;
    }
    </style>
    """, unsafe_allow_html=True)



# Title with emojis
st.markdown("""
    <div class="title-container">
        <h1>🏏 IPL Win Predictor 🏆</h1>
        <p style='font-size: 1.2rem; opacity: 0.8;'>Predict match outcomes with machine learning</p>
    </div>
""", unsafe_allow_html=True)

# Load the model
try:
    pipe = pickle.load(open('pipe.pkl', 'rb'))
except:
    st.error("⚠️ Model file not found. Please ensure 'pipe.pkl' is in the same directory.")
    st.stop()

# Teams
teams = sorted([
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'
])

# Team Selection Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🏏 Batting Team")
    batting_team = st.selectbox('Select batting team', teams, key='batting')
with col2:
    st.markdown("### ⚾ Bowling Team")
    bowling_team = st.selectbox('Select bowling team', teams, key='bowling')

if batting_team == bowling_team:
    st.warning("⚠️ Please select different teams for batting and bowling!")
st.markdown('</div>', unsafe_allow_html=True)

# Match Details Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown("### 🏟️ Match Details")
cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

col1, col2 = st.columns(2)
with col1:
    selected_city = st.selectbox('🌍 Venue', sorted(cities))
with col2:
    target = st.number_input('🎯 Target Score', min_value=0, value=0)
st.markdown('</div>', unsafe_allow_html=True)

# Current Status Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown("### 📊 Current Match Status")
col1, col2, col3 = st.columns(3)
with col1:
    score = st.number_input('Current Score 🏃', min_value=0, value=0)
with col2:
    wickets = st.number_input('Wickets Lost 🎯', min_value=0, max_value=9, value=0)
with col3:
    overs = st.number_input('Overs Completed 🕒', min_value=0.0, max_value=20.0, value=0.0, step=0.1)
st.markdown('</div>', unsafe_allow_html=True)

# Prediction Button
if st.button('🎮 Predict Win Probability'):
    if batting_team == bowling_team:
        st.error("🚫 Batting and Bowling teams cannot be the same!")
    elif target == 0:
        st.error("🎯 Please enter a valid target!")
    elif score > target:
        st.error("❌ Current score cannot be greater than target!")
    elif overs == 0:
        st.error("⏰ Overs cannot be 0!")
    else:
        # Calculations
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets = 10 - wickets
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        # Create DataFrame for prediction
        df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        # Make prediction
        result = pipe.predict_proba(df)
        batting_prob = round(result[0][1] * 100)
        bowling_prob = round(result[0][0] * 100)

        # Display results
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown("### 🎯 Match Prediction")
        
        # Team probabilities with progress bars
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="team-card">
                    <h4>{batting_team}</h4>
                    <div class="prediction-progress">
                        <div class="prediction-bar" style="width: {batting_prob}%; background: linear-gradient(45deg, #4CAF50, #8BC34A);">
                        </div>
                    </div>
                    <h2>{batting_prob}%</h2>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="team-card">
                    <h4>{bowling_team}</h4>
                    <div class="prediction-progress">
                        <div class="prediction-bar" style="width: {bowling_prob}%; background: linear-gradient(45deg, #2196F3, #03A9F4);">
                        </div>
                    </div>
                    <h2>{bowling_prob}%</h2>
                </div>
            """, unsafe_allow_html=True)
        
        # Match statistics
        st.markdown("### 📈 Match Statistics")
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        with stats_col1:
            st.markdown(f"""
                <div class="stat-card">
                    <h4>Required Run Rate</h4>
                    <h2>{rrr:.2f}</h2>
                    <p style='opacity: 0.8;'>runs per over</p>
                </div>
            """, unsafe_allow_html=True)
        with stats_col2:
            st.markdown(f"""
                <div class="stat-card">
                    <h4>Current Run Rate</h4>
                    <h2>{crr:.2f}</h2>
                    <p style='opacity: 0.8;'>runs per over</p>
                </div>
            """, unsafe_allow_html=True)
        with stats_col3:
            st.markdown(f"""
                <div class="stat-card">
                    <h4>Runs Needed</h4>
                    <h2>{runs_left}</h2>
                    <p style='opacity: 0.8;'>to win</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Additional match insights
        if batting_prob > bowling_prob:
            st.markdown(f"""
                <div style='text-align: center; margin-top: 2rem; padding: 1rem; background: rgba(76, 175, 80, 0.1); border-radius: 10px;'>
                    <h3>🎯 Match Insight</h3>
                    <p>{batting_team} is in a strong position to win with a {batting_prob}% chance!</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='text-align: center; margin-top: 2rem; padding: 1rem; background: rgba(33, 150, 243, 0.1); border-radius: 10px;'>
                    <h3>🎯 Match Insight</h3>
                    <p>{bowling_team} is in a strong position to win with a {bowling_prob}% chance!</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 2rem; opacity: 0.7;'>
        <p>🏏  </p>
    </div>
""", unsafe_allow_html=True)