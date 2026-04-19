import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os
from datetime import datetime, timedelta
from src.agents import AnalystAgent, SentimentAgent, PredictionAgent, StrategyAgent, ScenarioAgent
from data_generator import generate_voxintel_data, generate_single_record

# --- PAGE CONFIG ---
st.set_page_config(page_title="VoxIntel V3 | Autonomous Opinion AI", page_icon="🌌", layout="wide")

# --- PREMIUM THEME & GLASSMORPHISM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Outfit:wght@500;800&display=swap');
    
    .main {
        background-color: #05070A;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at top right, #0F172A, #05070A);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        text-align: center;
        transition: 0.4s;
    }
    .metric-card:hover {
        border-color: #00F2FF;
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 242, 255, 0.1);
    }
    .agent-log {
        background: rgba(0, 242, 255, 0.02);
        border-left: 4px solid #00F2FF;
        padding: 12px;
        margin: 8px 0;
        border-radius: 4px;
        font-size: 0.9rem;
        color: #A0AEC0;
    }
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.02em;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00F2FF, #7000FF);
        color: white;
        border: none;
        padding: 12px;
        font-weight: 800;
        border-radius: 12px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'data_buffer' not in st.session_state:
    if os.path.exists('data/raw_poll_data.csv'):
        st.session_state.data_buffer = pd.read_csv('data/raw_poll_data.csv')
    else:
        st.session_state.data_buffer = generate_voxintel_data(500)
    st.session_state.data_buffer['Timestamp'] = pd.to_datetime(st.session_state.data_buffer['Timestamp'])

if 'sim_running' not in st.session_state:
    st.session_state.sim_running = False

if 'logs' not in st.session_state:
    st.session_state.logs = ["System: VoxIntel Core initialized. Waiting for agent handshake..."]

# --- SIDEBAR: SIMULATION CONTROL ---
st.sidebar.image("https://img.icons8.com/color/144/artificial-intelligence.png", width=80)
st.sidebar.title("🎛️ Control Center")

col_a, col_b = st.sidebar.columns(2)
if col_a.button("🚀 LIVE FEED"):
    st.session_state.sim_running = True
if col_b.button("🛑 STOP"):
    st.session_state.sim_running = False

if st.sidebar.button("♻️ RESET ECOSYSTEM"):
    st.session_state.data_buffer = generate_voxintel_data(500)
    st.session_state.logs = ["System: Buffer flushed. New baseline established."]
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Scenario Analysis")
scenario_area = st.sidebar.selectbox("Hypothetical Investment", ['Quality', 'Price Drop', 'Support', 'R&D'])
scenario_mag = st.sidebar.slider("Investment Magnitude", 1, 5, 3)

# --- LIVE SIMULATION LOGIC ---
if st.session_state.sim_running:
    new_record = generate_single_record(len(st.session_state.data_buffer))
    new_df = pd.DataFrame([new_record])
    new_df['Timestamp'] = pd.to_datetime(new_df['Timestamp'])
    st.session_state.data_buffer = pd.concat([st.session_state.data_buffer, new_df], ignore_index=True)
    if len(st.session_state.data_buffer) > 2000: # Cap for performance
        st.session_state.data_buffer = st.session_state.data_buffer.iloc[1:]
    time.sleep(1)
    # Rerun to update dashboard
    st.rerun()

# --- HEADER ---
st.title("🌌 VOXINTEL V3 : Autonomous Opinion AI")
st.markdown("<p style='font-size: 1.2rem; color: #718096;'>Multi-Agent Cognitive Engine & Real-time Drift Analytics</p>", unsafe_allow_html=True)

# --- DATA ORCHESTRATION ---
df = st.session_state.data_buffer
analyst = AnalystAgent(df)
sentiment = SentimentAgent(df)
predictor = PredictionAgent(df)
scenario = ScenarioAgent(df)

# RUN AGENT CALCULATIONS
stats = analyst.get_summary_stats()
preds, trend = predictor.forecast_satisfaction()
sim_res = scenario.simulate_shift({'area': scenario_area, 'magnitude': scenario_mag})
strat_agent = StrategyAgent(stats, sentiment.get_sentiment_distribution().to_dict(), trend)

# GATHER AGENT THOUGHTS
if len(st.session_state.logs) > 8:
    st.session_state.logs = st.session_state.logs[-8:] # Keep last 8

current_thoughts = [
    analyst.get_agent_thought(),
    sentiment.get_agent_thought(),
    predictor.get_agent_thought(),
    strat_agent.get_agent_thought(),
    scenario.get_agent_thought(sim_res)
]
for t in current_thoughts:
    if t not in st.session_state.logs:
        st.session_state.logs.append(t)

# --- MAIN DASHBOARD: KPIS ---
row0_1, row0_2, row0_3, row0_4 = st.columns(4)

def render_metric(label, value, delta=None, color="#00F2FF"):
    delta_html = f"<span style='color:#48BB78; font-size:0.8rem;'>{delta}</span>" if delta else ""
    st.markdown(f"""
        <div class="metric-card">
            <p style='color:#718096; text-transform:uppercase; font-size:0.7rem; font-weight:bold;'>{label}</p>
            <h2 style='color:{color}; margin:0;'>{value}</h2>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

with row0_1:
    render_metric("Total Voices", stats['total_responses'], "+Live")
with row0_2:
    render_metric("Avg Satisfaction", f"{stats['avg_satisfaction']} / 5.0", "-0.02 Drift" if st.session_state.sim_running else None)
with row0_3:
    render_metric("Top Product", stats['top_product'], "Stable", "#7000FF")
with row0_4:
    render_metric("Predicted Gain", f"+{sim_res['net_gain']}", "Scenario Alpha", "#FF00E5")

st.markdown("<br>", unsafe_allow_html=True)

# --- MIDDLE SECTION: LOGS & WHAT-IF ---
col_log, col_scenario = st.columns([1, 1])

with col_log:
    st.subheader("🤖 Collaborative Intelligence Logs")
    for log in reversed(st.session_state.logs):
        st.markdown(f"<div class='agent-log'>{log}</div>", unsafe_allow_html=True)

with col_scenario:
    st.subheader("🔮 Scenario Inference")
    fig_scenario = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = sim_res['simulated_avg'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Projected Satisfaction ({scenario_area})", 'font': {'size': 16}},
        delta = {'reference': sim_res['original_avg'], 'relative': False},
        gauge = {
            'axis': {'range': [1, 5]},
            'bar': {'color': "#00F2FF"},
            'steps' : [
                {'range': [1, 3], 'color': "rgba(255,0,0,0.1)"},
                {'range': [3, 4], 'color': "rgba(255,255,0,0.1)"},
                {'range': [4, 5], 'color': "rgba(0,255,0,0.1)"}
            ],
        }
    ))
    fig_scenario.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#E0E0E0", 'family': "Inter"})
    st.plotly_chart(fig_scenario, use_container_width=True)

# --- VISUALS SECTION ---
st.markdown("---")
row2_1, row2_2 = st.columns([2, 1])

with row2_1:
    st.subheader("📈 Market Share vs Time")
    # Group by date and product
    history = df.copy()
    history['Date'] = history['Timestamp'].dt.date
    share_over_time = history.groupby(['Date', 'Product_Interests']).size().reset_index(name='Count')
    fig_hist = px.line(share_over_time, x='Date', y='Count', color='Product_Interests',
                       template='plotly_dark', color_discrete_sequence=['#00F2FF', '#7000FF', '#FF00E5'])
    fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_hist, use_container_width=True)

with row2_2:
    st.subheader("🌓 Thematic Sentiment")
    theme_dist = sentiment.get_theme_distribution().reset_index()
    theme_dist.columns = ['Theme', 'Volume']
    fig_theme = px.bar_polar(theme_dist, r='Volume', theta='Theme', 
                             template='plotly_dark', color='Volume', color_continuous_scale='Blues')
    fig_theme.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_theme, use_container_width=True)

# --- STRATEGY ENGINE ---
st.markdown("---")
st.subheader("💡 VoxIntel Strategy Agent : Prescriptive Insights")
recs = strat_agent.generate_recommendations()

cols = st.columns(len(recs))
for i, rec in enumerate(recs):
    with cols[i]:
        if "🚨" in rec or "URGENT" in rec:
            st.error(rec)
        elif "📉" in rec or "ALERT" in rec:
            st.warning(rec)
        else:
            st.success(rec)

# --- FOOTER ---
st.markdown("<br><hr><p style='text-align: center; color: #4F4F4F; font-size: 0.8rem;'>VoxIntel v3.0 | Industry-Grade Autonomous BI | Neural Orchestration</p>", unsafe_allow_html=True)
