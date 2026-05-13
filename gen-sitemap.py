import os

BASE = "/tmp/harlo-unkle-work"

pages = [
    "",
    "plumbing", "handyman", "aircon", "electrical", "door-repair", "wall-mounting",
    "toilet-waterproofing", "epoxy-grouting", "appliance-repair", "locksmith",
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

svcs = ["plumbing", "handyman", "aircon", "electrical", "door-repair", "wall-mounting",
        "waterproofing", "grouting", "appliance", "locksmith"]

xml = '<?xml version="1.0" encoding="UTF-8"?>'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

# Priority: homepage = 1.0, service pages = 0.9, regional = 0.8
for p in pages:
    if p:
        xml += '<url><loc>https://harlounkle.com/' + p + '.html</loc></url>'
    else:
        xml += '<url><loc>https://harlounkle.com/</loc></url>'

for s in svcs:
    for a in areas:
        xml += '<url><loc>https://harlounkle.com/services/' + s + '-' + a + '.html</loc></url>'

xml += '</urlset>'

with open(os.path.join(BASE, "sitemap.xml"), "w") as f:
    f.write(xml)

print("OK: sitemap.xml written with " + str(len(xml.split('<url>')) - 1) + " URLs")
