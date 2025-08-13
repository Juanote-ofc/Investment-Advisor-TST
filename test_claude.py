#!/usr/bin/env python3
"""
Simple Claude API test script
"""
import anthropic
import os

def test_claude():
    # Check if API key is set
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        print("Please set your API key:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")
        return
    
    try:
        # Initialize the client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Test API call
        print("🔄 Testing Claude API connection...")
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            temperature=0,
            messages=[
                {"role": "user", "content": "Hello! Please respond with just 'API connection successful!'"}
            ]
        )
        
        print("✅ Success!")
        print(f"Response: {message.content[0].text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_claude()
