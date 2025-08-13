#!/bin/bash

# Investment Advisor - Local Development Server
# Runs the Streamlit app locally for development and testing

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Investment Advisor AI - Local Development${NC}"
echo -e "${BLUE}=================================================${NC}"

# Navigate to the streamlit app directory
cd /Users/juancarlosmunguiassaldana/AD\ INVEST_TST/Investment-Advisor-TST/streamlit-app

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Install/update requirements
echo -e "${BLUE}📚 Installing requirements...${NC}"
pip install -r requirements.txt

# Set environment variables for local development
export AWS_REGION=us-east-1
export AWS_PROFILE=Juanelo
export S3_BUCKET=investment-advisor-dev-data-accce88f
export KNOWLEDGE_BASE_BUCKET=investment-advisor-dev-kb-accce88f
export BEDROCK_REGION=us-east-1

echo -e "${GREEN}✅ Environment configured${NC}"
echo -e "${BLUE}🌐 Starting Streamlit server...${NC}"
echo ""
echo -e "${GREEN}📱 Your app will be available at: http://localhost:8501${NC}"
echo -e "${GREEN}🔄 The app will auto-reload when you make changes${NC}"
echo ""

# Start Streamlit with development settings
streamlit run app.py \
    --server.port 8501 \
    --server.address localhost \
    --server.runOnSave true \
    --browser.gatherUsageStats false \
    --theme.primaryColor "#667eea" \
    --theme.backgroundColor "#ffffff" \
    --theme.secondaryBackgroundColor "#f0f2f6" \
    --theme.textColor "#262730"
