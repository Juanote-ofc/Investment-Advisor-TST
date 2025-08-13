"""
Investment Advisor - Simple Local Version
A simplified version for local testing
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Investment Advisor AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-username/investment-advisor',
        'Report a bug': 'https://github.com/your-username/investment-advisor/issues',
        'About': """
        # Investment Advisor AI
        
        An AI-powered investment advisory platform built with:
        - **Streamlit** for the frontend
        - **AWS Bedrock** for AI capabilities  
        - **Terraform** for infrastructure
        - **ECS Fargate** for deployment
        
        Version: 1.0.0
        """
    }
)

# Enhanced CSS styling
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card h3 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .metric-card h2 {
        color: #667eea;
        margin: 0.5rem 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Status indicators */
    .status {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 15px;
        padding: 15px;
        border-radius: 10px;
        font-weight: 500;
    }
    
    .status.success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status.warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

def render_header():
    """Render the main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Investment Advisor AI</h1>
        <p>Powered by AWS Bedrock, Terraform, and MCP Servers</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with user inputs"""
    with st.sidebar:
        st.markdown("### 🎯 Navigation")
        
        page = st.selectbox(
            "Choose a page:",
            ["Dashboard", "Portfolio Analysis", "Risk Assessment", "Market Insights", "Settings"]
        )
        
        st.markdown("---")
        
        # User Profile Section
        st.markdown("### 👤 User Profile")
        with st.expander("Investment Profile", expanded=True):
            investment_amount = st.number_input(
                "Investment Amount ($)",
                min_value=1000,
                max_value=10000000,
                value=100000,
                step=5000
            )
            
            risk_tolerance = st.select_slider(
                "Risk Tolerance",
                options=["Conservative", "Moderate", "Aggressive"],
                value="Moderate"
            )
            
            time_horizon = st.selectbox(
                "Investment Time Horizon",
                ["1-3 years", "3-5 years", "5-10 years", "10+ years"]
            )
            
            investment_goals = st.multiselect(
                "Investment Goals",
                ["Retirement", "Education", "Home Purchase", "Wealth Building", "Income Generation"]
            )
        
        # System Status
        st.markdown("---")
        st.markdown("### 📊 System Status")
        st.markdown("""
        <div class="status success">
            <span>✅</span>
            <div>
                <strong>Local Development Mode</strong><br>
                <small>Running on localhost:8501</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return {
            'page': page,
            'investment_amount': investment_amount,
            'risk_tolerance': risk_tolerance,
            'time_horizon': time_horizon,
            'investment_goals': investment_goals
        }

def get_portfolio_allocation(risk_tolerance):
    """Get portfolio allocation based on risk tolerance"""
    allocations = {
        'Conservative': {'Stocks': 30, 'Bonds': 60, 'Alternatives': 10},
        'Moderate': {'Stocks': 60, 'Bonds': 30, 'Alternatives': 10},
        'Aggressive': {'Stocks': 80, 'Bonds': 15, 'Alternatives': 5}
    }
    return allocations.get(risk_tolerance, allocations['Moderate'])

def render_dashboard(user_profile):
    """Render the main dashboard"""
    st.markdown("## 📊 Investment Dashboard")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Portfolio Value</h3>
            <h2>${user_profile['investment_amount']:,}</h2>
            <p style="color: green;">+5.2% this month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        expected_return = {"Conservative": 5.5, "Moderate": 7.8, "Aggressive": 9.2}
        st.markdown(f"""
        <div class="metric-card">
            <h3>Expected Return</h3>
            <h2>{expected_return[user_profile['risk_tolerance']]}%</h2>
            <p style="color: blue;">Annual projection</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        risk_scores = {"Conservative": 3.1, "Moderate": 6.2, "Aggressive": 8.7}
        st.markdown(f"""
        <div class="metric-card">
            <h3>Risk Score</h3>
            <h2>{risk_scores[user_profile['risk_tolerance']]}/10</h2>
            <p style="color: orange;">{user_profile['risk_tolerance']} risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Diversification</h3>
            <h2>85%</h2>
            <p style="color: green;">Well diversified</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Portfolio Allocation Chart
    st.markdown("### 🥧 Recommended Portfolio Allocation")
    
    portfolio = get_portfolio_allocation(user_profile['risk_tolerance'])
    
    # Create pie chart
    fig = px.pie(
        values=list(portfolio.values()),
        names=list(portfolio.keys()),
        title=f"Optimized Asset Allocation - {user_profile['risk_tolerance']} Risk",
        color_discrete_sequence=['#e74c3c', '#3498db', '#f39c12']
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        font=dict(size=14),
        title_font_size=18,
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance Chart
    st.markdown("### 📈 Portfolio Performance Simulation")
    
    # Generate sample performance data
    dates = pd.date_range(start=datetime.now() - timedelta(days=365), end=datetime.now(), freq='D')
    base_return = expected_return[user_profile['risk_tolerance']] / 100
    
    # Simulate portfolio performance
    np.random.seed(42)  # For consistent results
    daily_returns = np.random.normal(base_return/365, 0.01, len(dates))
    portfolio_values = [user_profile['investment_amount']]
    
    for daily_return in daily_returns[1:]:
        portfolio_values.append(portfolio_values[-1] * (1 + daily_return))
    
    # Create benchmark (S&P 500 simulation)
    benchmark_returns = np.random.normal(0.10/365, 0.012, len(dates))
    benchmark_values = [user_profile['investment_amount']]
    
    for daily_return in benchmark_returns[1:]:
        benchmark_values.append(benchmark_values[-1] * (1 + daily_return))
    
    performance_data = pd.DataFrame({
        'Date': dates,
        'Your Portfolio': portfolio_values,
        'S&P 500 Benchmark': benchmark_values
    })
    
    fig = px.line(
        performance_data,
        x='Date',
        y=['Your Portfolio', 'S&P 500 Benchmark'],
        title="Portfolio vs Benchmark Performance (Simulated)"
    )
    fig.update_layout(
        yaxis_title="Portfolio Value ($)",
        xaxis_title="Date",
        font=dict(size=12),
        title_font_size=16
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # AI Recommendations
    st.markdown("### 🤖 AI-Powered Recommendations")
    
    if st.button("Get AI Analysis", type="primary"):
        with st.spinner("Analyzing your portfolio with AI..."):
            # Simulate AI analysis
            import time
            time.sleep(2)
            
            st.success("Analysis complete!")
            
            recommendations = [
                {
                    'title': 'Optimize Asset Allocation',
                    'description': f'Based on your {user_profile["risk_tolerance"].lower()} risk tolerance, consider adjusting your allocation to maximize returns.',
                    'confidence': 92
                },
                {
                    'title': 'Diversify Internationally',
                    'description': 'Add 15-20% international exposure to reduce portfolio correlation risk.',
                    'confidence': 85
                },
                {
                    'title': 'Tax-Loss Harvesting',
                    'description': 'Implement tax-loss harvesting strategies to improve after-tax returns.',
                    'confidence': 78
                }
            ]
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"**{i}. {rec['title']}**")
                st.markdown(f"   {rec['description']}")
                st.markdown(f"   *Confidence: {rec['confidence']}%*")
                st.markdown("---")

def render_portfolio_analysis(user_profile):
    """Render portfolio analysis page"""
    st.markdown("## 📊 Portfolio Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Current Holdings Simulation")
        
        # Sample holdings
        holdings_data = {
            'Asset': ['VTSAX', 'VTIAX', 'VBTLX', 'VNQ', 'Cash'],
            'Allocation (%)': [40, 20, 25, 10, 5],
            'Value ($)': [
                user_profile['investment_amount'] * 0.40,
                user_profile['investment_amount'] * 0.20,
                user_profile['investment_amount'] * 0.25,
                user_profile['investment_amount'] * 0.10,
                user_profile['investment_amount'] * 0.05
            ]
        }
        
        holdings_df = pd.DataFrame(holdings_data)
        st.dataframe(holdings_df, use_container_width=True)
    
    with col2:
        st.markdown("#### Performance Metrics")
        
        metrics = {
            'Total Return (1Y)': '+12.4%',
            'Volatility': '14.2%',
            'Sharpe Ratio': '0.87',
            'Max Drawdown': '-8.3%',
            'Beta': '0.92'
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)

def main():
    """Main application"""
    render_header()
    
    # Sidebar navigation
    user_profile = render_sidebar()
    
    # Main content area
    if user_profile['page'] == "Dashboard":
        render_dashboard(user_profile)
    elif user_profile['page'] == "Portfolio Analysis":
        render_portfolio_analysis(user_profile)
    elif user_profile['page'] == "Risk Assessment":
        st.markdown("## ⚠️ Risk Assessment")
        st.info("Risk assessment features coming soon...")
    elif user_profile['page'] == "Market Insights":
        st.markdown("## 📈 Market Insights")
        st.info("Market insights features coming soon...")
    elif user_profile['page'] == "Settings":
        st.markdown("## ⚙️ Settings")
        st.info("Settings page coming soon...")

if __name__ == "__main__":
    main()
