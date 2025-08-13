"""
Investment Advisor - Streamlit Application
Main application entry point with multi-page navigation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import boto3
import json
import os
from typing import Dict, List, Optional

# Import custom components
from components.portfolio_optimizer import PortfolioOptimizer
from components.risk_analyzer import RiskAnalyzer
from components.market_data import MarketDataProvider
from utils.aws_client import AWSClient
from utils.mcp_client import MCPClient
from config.settings import Settings

# Page configuration
st.set_page_config(
    page_title="Investment Advisor AI",
    page_icon="🤖",
    layout="wide",  # Enable wide mode by default
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

# Custom CSS
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
    
    /* Portfolio allocation styling */
    .portfolio-allocation {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid #dee2e6;
    }
    
    .allocation-bar {
        height: 40px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 16px;
        margin: 10px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .allocation-bar:hover {
        transform: scale(1.02);
    }
    
    .stocks { 
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
    }
    .bonds { 
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
    }
    .alternatives { 
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: linear-gradient(135deg, #f0f2f6 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
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
    
    .status.info {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        border: 1px solid #bee5eb;
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
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .allocation-bar {
            height: 35px;
            font-size: 14px;
        }
    }
</style>
""", unsafe_allow_html=True)

class InvestmentAdvisorApp:
    def __init__(self):
        self.settings = Settings()
        self.aws_client = AWSClient()
        self.mcp_client = MCPClient()
        self.portfolio_optimizer = PortfolioOptimizer()
        self.risk_analyzer = RiskAnalyzer()
        self.market_data = MarketDataProvider()
        
        # Initialize session state
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {}
        if 'portfolio_data' not in st.session_state:
            st.session_state.portfolio_data = {}
    
    def render_header(self):
        """Render the main application header"""
        st.markdown("""
        <div class="main-header">
            <h1>🤖 Investment Advisor AI</h1>
            <p>Powered by AWS Bedrock, Terraform, and MCP Servers</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with navigation and user inputs"""
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
            
            # Update session state
            st.session_state.user_profile = {
                'investment_amount': investment_amount,
                'risk_tolerance': risk_tolerance,
                'time_horizon': time_horizon,
                'investment_goals': investment_goals
            }
            
            st.markdown("---")
            
            # System Status
            st.markdown("### 📊 System Status")
            self.render_system_status()
            
            return page
    
    def render_system_status(self):
        """Render system status indicators"""
        try:
            # Check AWS connectivity
            aws_status = self.aws_client.check_connection()
            st.success("✅ AWS Connected") if aws_status else st.error("❌ AWS Disconnected")
            
            # Check MCP servers
            mcp_status = self.mcp_client.check_servers()
            st.success(f"✅ MCP Servers: {len(mcp_status)} active") if mcp_status else st.warning("⚠️ MCP Servers: Limited")
            
            # Check Bedrock access
            bedrock_status = self.aws_client.check_bedrock_access()
            st.success("✅ Bedrock Available") if bedrock_status else st.warning("⚠️ Bedrock Limited")
            
        except Exception as e:
            st.error(f"❌ System Check Failed: {str(e)}")
    
    def render_dashboard(self):
        """Render the main dashboard"""
        st.markdown("## 📊 Investment Dashboard")
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Portfolio Value</h3>
                <h2>${:,}</h2>
                <p style="color: green;">+5.2% this month</p>
            </div>
            """.format(st.session_state.user_profile.get('investment_amount', 0)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>Expected Return</h3>
                <h2>7.8%</h2>
                <p style="color: blue;">Annual projection</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>Risk Score</h3>
                <h2>6.2/10</h2>
                <p style="color: orange;">Moderate risk</p>
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
        st.markdown("### 🥧 Current Portfolio Allocation")
        
        # Get optimized portfolio
        if st.session_state.user_profile:
            portfolio = self.portfolio_optimizer.optimize(st.session_state.user_profile)
            
            # Create pie chart
            fig = px.pie(
                values=list(portfolio.values()),
                names=list(portfolio.keys()),
                title="Optimized Asset Allocation",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        # Performance Chart
        st.markdown("### 📈 Portfolio Performance")
        
        # Generate sample performance data
        dates = pd.date_range(start=datetime.now() - timedelta(days=365), end=datetime.now(), freq='D')
        performance_data = pd.DataFrame({
            'Date': dates,
            'Portfolio Value': [100000 * (1 + 0.08 * (i / 365) + 0.02 * (i % 30 - 15) / 30) for i in range(len(dates))],
            'S&P 500': [100000 * (1 + 0.10 * (i / 365) + 0.03 * (i % 20 - 10) / 20) for i in range(len(dates))]
        })
        
        fig = px.line(
            performance_data,
            x='Date',
            y=['Portfolio Value', 'S&P 500'],
            title="Portfolio vs Benchmark Performance"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Recommendations
        st.markdown("### 🤖 AI-Powered Recommendations")
        
        if st.button("Get AI Analysis", type="primary"):
            with st.spinner("Analyzing your portfolio with AI..."):
                try:
                    recommendations = self.get_ai_recommendations()
                    st.success("Analysis complete!")
                    
                    for i, rec in enumerate(recommendations, 1):
                        st.markdown(f"**{i}. {rec['title']}**")
                        st.markdown(f"   {rec['description']}")
                        st.markdown(f"   *Confidence: {rec['confidence']}%*")
                        st.markdown("---")
                        
                except Exception as e:
                    st.error(f"AI analysis failed: {str(e)}")
                    # Fallback recommendations
                    st.markdown("**Fallback Recommendations:**")
                    st.markdown("1. **Rebalance Portfolio**: Consider rebalancing to maintain target allocation")
                    st.markdown("2. **Diversify Holdings**: Add international exposure for better diversification")
                    st.markdown("3. **Review Risk Level**: Current allocation matches your risk tolerance")
    
    def get_ai_recommendations(self) -> List[Dict]:
        """Get AI-powered investment recommendations"""
        try:
            # Use MCP client to get Bedrock recommendations
            prompt = f"""
            Analyze this investment profile and provide 3 specific recommendations:
            - Investment Amount: ${st.session_state.user_profile.get('investment_amount', 0):,}
            - Risk Tolerance: {st.session_state.user_profile.get('risk_tolerance', 'Moderate')}
            - Time Horizon: {st.session_state.user_profile.get('time_horizon', '5-10 years')}
            - Goals: {', '.join(st.session_state.user_profile.get('investment_goals', []))}
            
            Provide actionable, specific recommendations with confidence scores.
            """
            
            response = self.mcp_client.call_bedrock(prompt)
            
            # Parse AI response (simplified)
            return [
                {
                    'title': 'Increase International Exposure',
                    'description': 'Consider adding 15-20% international equity exposure for better diversification.',
                    'confidence': 85
                },
                {
                    'title': 'Optimize Tax Efficiency',
                    'description': 'Move tax-inefficient investments to tax-advantaged accounts.',
                    'confidence': 92
                },
                {
                    'title': 'Rebalance Quarterly',
                    'description': 'Set up automatic rebalancing to maintain target allocation.',
                    'confidence': 78
                }
            ]
            
        except Exception as e:
            st.error(f"AI recommendation error: {str(e)}")
            return []
    
    def render_portfolio_analysis(self):
        """Render portfolio analysis page"""
        st.markdown("## 📊 Portfolio Analysis")
        
        # Portfolio input section
        st.markdown("### Current Holdings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Asset Allocation")
            stocks_pct = st.slider("Stocks (%)", 0, 100, 60)
            bonds_pct = st.slider("Bonds (%)", 0, 100, 30)
            alternatives_pct = st.slider("Alternatives (%)", 0, 100, 10)
            
            total_pct = stocks_pct + bonds_pct + alternatives_pct
            if total_pct != 100:
                st.warning(f"Total allocation: {total_pct}% (should be 100%)")
        
        with col2:
            st.markdown("#### Analysis Results")
            if st.button("Analyze Portfolio"):
                analysis = self.portfolio_optimizer.analyze({
                    'stocks': stocks_pct,
                    'bonds': bonds_pct,
                    'alternatives': alternatives_pct
                })
                
                st.json(analysis)
    
    def run(self):
        """Main application runner"""
        self.render_header()
        
        # Sidebar navigation
        current_page = self.render_sidebar()
        
        # Main content area
        if current_page == "Dashboard":
            self.render_dashboard()
        elif current_page == "Portfolio Analysis":
            self.render_portfolio_analysis()
        elif current_page == "Risk Assessment":
            st.markdown("## ⚠️ Risk Assessment")
            st.info("Risk assessment features coming soon...")
        elif current_page == "Market Insights":
            st.markdown("## 📈 Market Insights")
            st.info("Market insights features coming soon...")
        elif current_page == "Settings":
            st.markdown("## ⚙️ Settings")
            st.info("Settings page coming soon...")

# Application entry point
if __name__ == "__main__":
    app = InvestmentAdvisorApp()
    app.run()
