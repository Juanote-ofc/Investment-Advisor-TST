#!/usr/bin/env python3
"""
Simple Claude chat example
"""
import anthropic
import os

def chat_with_claude(prompt):
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0.7,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def main():
    print("Claude API Example")
    print("-" * 20)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
            
        try:
            response = chat_with_claude(user_input)
            print(f"\nClaude: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
