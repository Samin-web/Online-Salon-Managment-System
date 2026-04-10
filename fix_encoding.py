import os

def fix_file(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    
    with open(path, 'rb') as f:
        data = f.read()
    
    # Try to decode as utf-8, if fails try latin-1
    try:
        content = data.decode('utf-8')
    except UnicodeDecodeError:
        content = data.decode('latin-1')
    
    # Clean up any weird characters and ensure flattened tags
    import re
    def clean_tag(match):
        return re.sub(r'\s+', ' ', match.group(0))
    
    content = re.sub(r'\{\{.*?\}\}', clean_tag, content, flags=re.DOTALL)
    content = re.sub(r'\{%.*?%\}', clean_tag, content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    print(f"Fixed {path}")

# Fix both files
fix_file(r"c:\Users\A S U S\OneDrive\문서\OnlineStylehub\templates\owner\pending_only.html")
fix_file(r"c:\Users\A S U S\OneDrive\문서\OnlineStylehub\templates\shared_status_popup.html")
