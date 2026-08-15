import base64

with open('anki-addon/theme/logo.png', 'rb') as f:
    data = f.read()

b64 = base64.b64encode(data).decode('ascii')
content = f'"""Embedded Logo Base64 Data URI for Anki Wykiati."""\n\nLOGO_PNG_BASE64 = "data:image/png;base64,{b64}"\n'

with open('anki-addon/theme/logo_data.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Generated anki-addon/theme/logo_data.py successfully!")
