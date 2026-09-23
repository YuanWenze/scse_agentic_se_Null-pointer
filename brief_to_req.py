import json
from pathlib import Path
from ollama import chat

brief_path = Path("brief.txt")
brief_text = brief_path.read_text(encoding="utf-8")

system_prompt = """
You are a software requirements analyst.
Read the robot navigation brief.
Write the software requirements in plain text.
"""

response = chat(
    model="qwen3:8b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": brief_text}
    ]
)

output_text = response.message.content
print(output_text)

output_path = Path("robot_requirements.txt")
output_path.write_text(output_text, encoding="utf-8")

print("Saved to robot_requirements.txt")
