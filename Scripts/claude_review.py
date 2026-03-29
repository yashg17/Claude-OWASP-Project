import os
import sys
import json
import anthropic
from dotenv import load_dotenv

# Load from .env if it exists (for local testing)
load_dotenv()

def analyze_code(file_path):
    # Get API Key from Environment Variable (Jenkins will provide this)
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        print("ERROR: CLAUDE_API_KEY not found.")
        sys.exit(1)

    if not os.path.exists(file_path):
        print(f"ERROR: File {file_path} not found.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    
    with open(file_path, "r") as f:
        code_content = f.read()

    # Professional System Prompt
    system_prompt = (
        "You are a senior security engineer. Analyze the provided Python code for OWASP Top 10 vulnerabilities. "
        "Output ONLY a raw JSON array of objects. Each object must have: "
        "vulnerability_type, severity, line_number, and recommendation. "
        "Do not include markdown blocks like ```json."
    )

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": f"Analyze this code:\n\n{code_content}"}]
        )
        
        # Clean the response in case Claude adds markdown backticks
        raw_json = response.content[0].text.replace('```json', '').replace('```', '').strip()
        print(raw_json)
        
    except Exception as e:
        print(f"API Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Allows Jenkins to pass the filename: python3 scripts/claude_review.py app.py
    target_file = sys.argv[1] if len(sys.argv) > 1 else "app.py"
    analyze_code(target_file)
