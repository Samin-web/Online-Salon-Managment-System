import re
import os

def find_split_tags(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex for tags split across lines
    split_vars = re.findall(r'\{\{[^}]*\n[^}]*\}\}', content)
    split_blocks = re.findall(r'\{%[^%]*\n[^%]*%\}', content)
    
    if split_vars or split_blocks:
        print(f"File: {file_path}")
        for v in split_vars:
            print(f"Split var: {v!r}")
        for b in split_blocks:
            print(f"Split block: {b!r}")
        
        # Auto-fix: replace newlines with spaces
        fixed = content
        fixed = re.sub(r'(\{\{.*?\}\})', lambda m: m.group(1).replace('\n', ' ').replace('\r', ''), fixed, flags=re.DOTALL)
        fixed = re.sub(r'(\{%.*?%\})', lambda m: m.group(1).replace('\n', ' ').replace('\r', ''), fixed, flags=re.DOTALL)
        
        # Also collapse multiple spaces
        fixed = re.sub(r'\s+', ' ', fixed) # Caution: this might collapse too much CSS/HTML
        # Better: just fix the tags
        
        # New strategy:
        def clean_tag(match):
            return re.sub(r'\s+', ' ', match.group(0))
        
        fixed = re.sub(r'\{\{.*?\}\}', clean_tag, content, flags=re.DOTALL)
        fixed = re.sub(r'\{%.*?%\}', clean_tag, fixed, flags=re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(fixed)
        print("Fixed.")

files = [
    r"c:\Users\A S U S\OneDrive\문서\OnlineStylehub\apps\dashboard\templates\dashboard\manage_staff.html",
    r"c:\Users\A S U S\OneDrive\문서\OnlineStylehub\apps\dashboard\templates\dashboard\staff_application_detail.html"
]

for f in files:
    find_split_tags(f)
