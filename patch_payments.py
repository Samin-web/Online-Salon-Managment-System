"""
Directly patch payments.html to fix the broken QR code JavaScript.
"""
import re

filepath = r"C:\Users\A S U S\OneDrive\문서\OnlineStylehub\templates\customers\payments.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Broken option tag (date filter split across lines)
old_option = (
    '<option value="{{ apt.id }}">\n'
    '                            {{ apt.salon.name }} &mdash; Rs.{{ apt.total_price }} ({{ apt.appointment_date|date:"d M Y"\n'
    '                            }})\n'
    '                        </option>'
)
new_option = '<option value="{{ apt.id }}">{{ apt.salon.name }} &mdash; Rs.{{ apt.total_price }} ({{ apt.appointment_date|date:"d M Y" }})</option>'

if old_option in content:
    content = content.replace(old_option, new_option)
    print("Fix 1 applied: option tag fixed")
else:
    print("Fix 1: old_option not found (may already be fixed)")

# Fix 2: Replace the entire broken salonQRData block with a clean one
# Use regex to match any variant of the broken block
bad_block_pattern = re.compile(
    r'/\*\s*[\u2500\u2014-]+\s*QR CODE DYNAMIC LOGIC\s*[\u2500\u2014-]+\s*\*/.*?(?=const selectElement)',
    re.DOTALL
)

good_block = """/* ── QR CODE DYNAMIC LOGIC ── */
        const salonQRData = {};
        {% for apt in pending_appointments %}
        salonQRData[{{ apt.id }}] = {
            qr: '{% if apt.salon.qr_code %}{{ apt.salon.qr_code.url }}{% endif %}',
            enabled: {% if apt.salon.is_qr_payment_enabled %}true{% else %}false{% endif %},
            name: '{{ apt.salon.name|escapejs }}'
        };
        {% endfor %}

        """

match = bad_block_pattern.search(content)
if match:
    content = content[:match.start()] + good_block + content[match.end():]
    print("Fix 2 applied: salonQRData block rewritten")
else:
    print("Fix 2: pattern not found")

# Fix 3: Ensure apptId is parsed as int  
content = content.replace(
    "const apptId = this.value;\n        if (apptId && salonQRData[apptId]) {\n            const data = salonQRData[apptId];",
    "const apptId = parseInt(this.value);\n        const data = salonQRData[apptId];\n        if (apptId && data) {"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! File patched successfully.")

# Verify
with open(filepath, 'r', encoding='utf-8') as f:
    verify = f.read()

if 'enabled: {% if apt.salon.is_qr_payment_enabled %}true{% else %}false{% endif %}' in verify:
    print("VERIFIED: Clean salonQRData block is present")
else:
    print("WARNING: Could not verify fix")

if '{{ apt.appointment_date|date:"d M Y" }})' in verify:
    print("VERIFIED: Option date tag is clean")
