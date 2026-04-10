import re
import os

file_path = r"c:\Users\A S U S\OneDrive\문서\OnlineStylehub\apps\dashboard\templates\dashboard\staff_application_detail.html"

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit()

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

stack = []
for i, line in enumerate(lines):
    line_num = i + 1
    # Find all {% ... %}
    tags = re.findall(r'\{%\s*(.*?)\s*%\}', line)
    for content in tags:
        parts = content.split()
        if not parts: continue
        tag = parts[0]
        
        if tag in ['block', 'if', 'for', 'with', 'autoescape']:
            stack.append((tag, line_num))
        elif tag == 'else' or tag == 'elif':
            if not stack or stack[-1][0] != 'if':
                print(f"Error: {tag} at line {line_num} not inside if")
        elif tag == 'empty':
             if not stack or stack[-1][0] != 'for':
                print(f"Error: empty at line {line_num} not inside for")
        elif tag.startswith('end'):
            if not stack:
                print(f"Error: {tag} at line {line_num} has no opening tag")
                continue
            
            opening_tag = stack[-1][0]
            if tag == 'end' + opening_tag:
                stack.pop()
            else:
                print(f"Mismatch: {tag} at line {line_num} inside {opening_tag} (line {stack[-1][1]})")

if stack:
    for tag, line in stack:
        print(f"Unclosed: {tag} at line {line}")
else:
    print("No imbalances found in blocks.")
