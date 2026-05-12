import os

BASE = "/Users/garethlee/harlo-unkle"

pages = [
    "",
    "plumbing", "handyman", "aircon", "electrical", "door-repair", "wall-mounting",
    "about", "contact", "terms", "privacy",
]

areas = {
    "jurong-west": "Jurong West",
    "jurong-east": "Jurong East",
    "clementi": "Clementi",
    "tampines": "Tampines",
    "bedok": "Bedok",
    "woodlands": "Woodlands",
    "yishun": "Yishun",
    "ang-mo-kio": "Ang Mo Kio",
    "bishan": "Bishan",
    "pasir-ris": "Pasir Ris",
}

svcs = ["plumbing", "handyman", "aircon", "electrical", "door-repair", "wall-mounting"]

xml = ['<?xml version="1.0" encoding="UTF-8"?>']
xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

# Priority: homepage = 1.0, service pages = 0.9, regional = 0.8, other = 0.7
for p in pages:
    xml.append('  <url><loc>https://harlounkle.com/' + (p + ".html" if p else "") + '</loc></url>')

for s in svcs:
    for a in areas:
        xml.append('  <url><loc>https://harlounkle.com/services/' + s + '-' + a + '.html</loc></url>')

xml.append('</urlset>')

with open(os.path.join(BASE, "sitemap.xml"), "w") as f:
    f.write("\n".join(xml))

print("OK: sitemap.xml written with " + str(len(xml) - 2) + " URLs")
