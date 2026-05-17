import os

BASE = "/Users/garethlee/harlo-unkle"

pages = [
    "",
    "plumbing", "handyman", "aircon", "electrical", "door-repair", "wall-mounting",
]

areas = [
    # North
    "woodlands", "yishun", "sembawang",
    # North-East
    "ang-mo-kio", "hougang", "sengkang", "punggol", "serangoon",
    # East
    "bedok", "pasir-ris", "tampines", "changi", "pay-lebar",
    # West
    "jurong-west", "jurong-east", "clementi", "bukit-batok", "bukit-panjang", "choa-chu-kang", "pioneer",
    # Central
    "bishan", "toa-payoh", "geylang", "kallang", "queenstown", "buki-timah", "novena", "orchard", "marine-parade",
]

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
