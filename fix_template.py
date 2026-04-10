# Fix the salon_detail.html template syntax error
file_path = r'c:\Users\A S U S\OneDrive\문서\OnlineStylehub\templates\public\salon_detail.html'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the problematic section (split across multiple lines)
old_text = '''{% if forloop.counter <= review.rating %}★{% else %}<span style="opacity: 0.2;">★</span>{% endif
                            %}
                            {% endfor %}'''

# Define the corrected section
new_text = '''{% if forloop.counter <= review.rating %}★{% else %}<span style="opacity: 0.2;">★</span>{% endif %}
                        {% endfor %}'''

# Replace the old text with the new text
if old_text in content:
    content = content.replace(old_text, new_text)
    print("✓ Found and fixed the template syntax error!")
else:
    print("✗ Could not find the exact pattern to replace")
    print("Trying alternative approach...")
    
    # Try line-by-line approach
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '{% endif' in line and not line.strip().endswith('%}'):
            print(f"Found broken tag at line {i+1}: {line[:50]}...")
            # Fix this line and the next
            if i+1 < len(lines) and lines[i+1].strip() == '%}':
                lines[i] = line.rstrip() + ' %}'
                lines[i+1] = ''  # Remove the orphaned %}
                print("Applied fix!")
                
    content = '\n'.join(lines)

# Write the fixed content back
with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("Template file has been updated successfully!")
