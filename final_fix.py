import re
import os

def join_tags(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find split tags: {{ or {% followed by newline and optional spaces, then content, then closure
    # This is tricky because we want to join anything between {{ and }} or {% and %} if it's split by a newline
    
    # Simple strategy: Find all occurrences of {{ ... }} and {% ... %} that span multiple lines and join them
    
    def replacer(match):
        return match.group(0).replace('\n', ' ').replace('\r', '').replace('  ', ' ')

    # Regex for {{ ... }} and {% ... %} spanning multiple lines
    new_content = re.sub(r'\{\{.*?\}\}', replacer, content, flags=re.DOTALL)
    new_content = re.sub(r'\{%.*?%\}', replacer, new_content, flags=re.DOTALL)

    # Specific fix for the badge in manage_staff if needed
    # (The regex above should handle it, but being explicit is fine)

    if content != new_content:
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)
        print(f"Fixed tags in {file_path}")
    else:
        print(f"No changes needed for {file_path}")

# Target files
files = [
    r"c:\Users\A S U S\OneDrive\문서\OnlineStylehub\apps\dashboard\templates\dashboard\manage_staff.html",
    r"c:\Users\A S U S\OneDrive\문서\OnlineStylehub\apps\dashboard\templates\dashboard\staff_application_detail.html"
]

for f_path in files:
    join_tags(f_path)
