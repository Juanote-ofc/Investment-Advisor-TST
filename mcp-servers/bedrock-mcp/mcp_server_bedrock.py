#!/usr/bin/env python3
"""
Custom MCP Server for Amazon Bedrock Integration
Provides investment-specific AI capabilities
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
import boto3
from botocore.exceptions import ClientError

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BedrockMCPServer:
    def __init__(self):
        self.server = Server("bedrock-investment-advisor")
        self.bedrock_client = None
        self.available_models = [
            "amazon.titan-text-express-v1",
            "amazon.nova-pro-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0"
        ]
        
        # Register handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup MCP server handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available Bedrock tools"""
            return [
                Tool(
                    name="analyze_investment",
                    description="Analyze investment scenarios using AI",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "investment_amount": {"type": "number"},
                            "risk_tolerance": {"type": "string", "enum": ["conservative", "moderate", "aggressive"]},
                            "time_horizon": {"type": "string"},
                            "goals": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["investment_amount", "risk_tolerance", "time_horizon"]
                    }
                ),
                Tool(
                    name="optimize_portfolio",
                    description="Optimize portfolio allocation using AI",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "current_allocation": {"type": "object"},
                            "constraints": {"type": "object"},
                            "objectives": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["current_allocation"]
                    }
                ),
                Tool(
                    name="assess_risk",
                    description="Assess investment risk using AI models",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "portfolio": {"type": "object"},
                            "market_conditions": {"type": "object"},
                            "time_horizon": {"type": "string"}
                        },
                        "required": ["portfolio"]
                    }
                ),
                Tool(
                    name="generate_report",
                    description="Generate comprehensive investment report",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_profile": {"type": "object"},
                            "portfolio_data": {"type": "object"},
                            "report_type": {"type": "string", "enum": ["summary", "detailed", "risk_analysis"]}
                        },
                        "required": ["user_profile", "portfolio_data"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls"""
            try:
                if name == "analyze_investment":
                    return await self.analyze_investment(arguments)
                elif name == "optimize_portfolio":
                    return await self.optimize_portfolio(arguments)
                elif name == "assess_risk":
                    return await self.assess_risk(arguments)
                elif name == "generate_report":
                    return await self.generate_report(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
            
            except Exception as e:
                logger.error(f"Tool call error: {str(e)}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def analyze_investment(self, args: Dict[str, Any]) -> List[TextContent]:
        """Analyze investment scenario using Bedrock"""
        try:
            prompt = self.create_investment_analysis_prompt(args)
            response = await self.call_bedrock_model(prompt, "amazon.titan-text-express-v1")
            
            return [TextContent(
                type="text",
                text=f"Investment Analysis:\n\n{response}"
            )]
        
        except Exception as e:
            return [TextContent(type="text", text=f"Analysis failed: {str(e)}")]
    
    async def optimize_portfolio(self, args: Dict[str, Any]) -> List[TextContent]:
        """Optimize portfolio using AI"""
        try:
            prompt = self.create_portfolio_optimization_prompt(args)
            response = await self.call_bedrock_model(prompt, "amazon.nova-pro-v1:0")
            
            return [TextContent(
                type="text",
                text=f"Portfolio Optimization:\n\n{response}"
            )]
        
        except Exception as e:
            return [TextContent(type="text", text=f"Optimization failed: {str(e)}")]
    
    async def assess_risk(self, args: Dict[str, Any]) -> List[TextContent]:
        """Assess investment risk"""
        try:
            prompt = self.create_risk_assessment_prompt(args)
            response = await self.call_bedrock_model(prompt, "anthropic.claude-3-haiku-20240307-v1:0")
            
            return [TextContent(
                type="text",
                text=f"Risk Assessment:\n\n{response}"
            )]
        
        except Exception as e:
            return [TextContent(type="text", text=f"Risk assessment failed: {str(e)}")]
    
    async def generate_report(self, args: Dict[str, Any]) -> List[TextContent]:
        """Generate comprehensive investment report"""
        try:
            prompt = self.create_report_prompt(args)
            response = await self.call_bedrock_model(prompt, "amazon.titan-text-express-v1")
            
            return [TextContent(
                type="text",
                text=f"Investment Report:\n\n{response}"
            )]
        
        except Exception as e:
            return [TextContent(type="text", text=f"Report generation failed: {str(e)}")]
    
    def create_investment_analysis_prompt(self, args: Dict[str, Any]) -> str:
        """Create prompt for investment analysis"""
        return f"""
        As an expert investment advisor, analyze the following investment scenario:
        
        Investment Amount: ${args['investment_amount']:,}
        Risk Tolerance: {args['risk_tolerance']}
        Time Horizon: {args['time_horizon']}
        Goals: {', '.join(args.get('goals', []))}
        
        Provide a comprehensive analysis including:
        1. Recommended asset allocation
        2. Specific investment vehicles
        3. Expected returns and risks
        4. Tax considerations
        5. Rebalancing strategy
        
        Format the response as structured recommendations.
        """
    
    def create_portfolio_optimization_prompt(self, args: Dict[str, Any]) -> str:
        """Create prompt for portfolio optimization"""
        current = args['current_allocation']
        return f"""
        Optimize the following portfolio allocation:
        
        Current Allocation: {json.dumps(current, indent=2)}
        Constraints: {json.dumps(args.get('constraints', {}), indent=2)}
        Objectives: {', '.join(args.get('objectives', ['maximize_return', 'minimize_risk']))}
        
        Provide:
        1. Optimized allocation percentages
        2. Rationale for changes
        3. Expected improvement metrics
        4. Implementation timeline
        5. Monitoring recommendations
        """
    
    def create_risk_assessment_prompt(self, args: Dict[str, Any]) -> str:
        """Create prompt for risk assessment"""
        return f"""
        Assess the risk profile of this investment portfolio:
        
        Portfolio: {json.dumps(args['portfolio'], indent=2)}
        Market Conditions: {json.dumps(args.get('market_conditions', {}), indent=2)}
        Time Horizon: {args.get('time_horizon', 'Not specified')}
        
        Provide:
        1. Overall risk score (1-10)
        2. Key risk factors
        3. Diversification analysis
        4. Stress test scenarios
        5. Risk mitigation recommendations
        """
    
    def create_report_prompt(self, args: Dict[str, Any]) -> str:
        """Create prompt for report generation"""
        report_type = args.get('report_type', 'summary')
        return f"""
        Generate a {report_type} investment report for:
        
        User Profile: {json.dumps(args['user_profile'], indent=2)}
        Portfolio Data: {json.dumps(args['portfolio_data'], indent=2)}
        
        Include:
        1. Executive summary
        2. Current portfolio analysis
        3. Performance metrics
        4. Recommendations
        5. Next steps
        
        Format as a professional investment report.
        """
    
    async def call_bedrock_model(self, prompt: str, model_id: str) -> str:
        """Call Bedrock model with prompt"""
        try:
            if not self.bedrock_client:
                self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
            
            if model_id.startswith('amazon.titan'):
                body = json.dumps({
                    'inputText': prompt,
                    'textGenerationConfig': {
                        'maxTokenCount': 2000,
                        'temperature': 0.7,
                        'topP': 0.9
                    }
                })
            elif model_id.startswith('amazon.nova'):
                body = json.dumps({
                    'messages': [{'role': 'user', 'content': [{'text': prompt}]}],
                    'max_tokens': 2000,
                    'temperature': 0.7
                })
            elif model_id.startswith('anthropic.claude'):
                body = json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 2000,
                    'messages': [{'role': 'user', 'content': prompt}]
                })
            else:
                raise ValueError(f"Unsupported model: {model_id}")
            
            response = self.bedrock_client.invoke_model(
                modelId=model_id,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            
            # Parse response based on model type
            if model_id.startswith('amazon.titan'):
                return response_body['results'][0]['outputText']
            elif model_id.startswith('amazon.nova'):
                return response_body['output']['message']['content'][0]['text']
            elif model_id.startswith('anthropic.claude'):
                return response_body['content'][0]['text']
            
        except ClientError as e:
            logger.error(f"Bedrock API error: {str(e)}")
            return f"AI service temporarily unavailable. Error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return f"Analysis failed due to technical error: {str(e)}"
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="bedrock-investment-advisor",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )

async def main():
    """Main entry point"""
    server = BedrockMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
