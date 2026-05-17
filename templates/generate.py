import os, json
from string import Template

BASE = "/Users/garethlee/harlo-unkle"

# Read template
with open(os.path.join(BASE, "templates/service-page.html")) as f:
    TPL = f.read()

def render(template_str, **kwargs):
    """Simple string replace for {{VAR}} placeholders."""
    result = template_str
    for key, value in kwargs.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result

AREAS = {
    # North
    "woodlands": "Woodlands",
    "yishun": "Yishun",
    "sembawang": "Sembawang",
    # North-East
    "ang-mo-kio": "Ang Mo Kio",
    "hougang": "Hougang",
    "sengkang": "Sengkang",
    "punggol": "Punggol",
    "serangoon": "Serangoon",
    # East
    "bedok": "Bedok",
    "pasir-ris": "Pasir Ris",
    "tampines": "Tampines",
    "changi": "Changi",
    "pay-lebar": "Paya Lebar",
    # West
    "jurong-west": "Jurong West",
    "jurong-east": "Jurong East",
    "clementi": "Clementi",
    "bukit-batok": "Bukit Batok",
    "bukit-panjang": "Bukit Panjang",
    "choa-chu-kang": "Choa Chu Kang",
    "pioneer": "Pioneer",
    # Central
    "bishan": "Bishan",
    "toa-payoh": "Toa Payoh",
    "geylang": "Geylang",
    "kallang": "Kallang",
    "queenstown": "Queenstown",
    "buki-timah": "Bukit Timah",
    "novena": "Novena",
    "orchard": "Orchard",
    "marine-parade": "Marine Parade",
}

def build_region_links(svc_slug):
    links = []
    for a_slug, a_label in AREAS.items():
        links.append('<a href="/services/' + svc_slug + '-' + a_slug + '.html">' + a_label + '</a>')
    return '\n\n    <div class="section-header" style="padding-top:2rem">\n      <span class="section-label">Serving All of Singapore</span>\n      <p style="margin-bottom:1rem;color:var(--text-secondary)">We cover every HDB town and neighbourhood — HDB, condo, and landed properties islandwide.</p>\n      <div class="region-areas"><div class="region-grid">\n        ' + '\n        '.join(links) + '\n      </div></div>'

def build_subs(svc_name, extra_text=""):
    icons = {
        "plumbing": ["💧","🚽","🔥","🏠","🔧","🚿"],
        "handyman": ["🪑","🎨","💡","🪟","🚪","📦"],
        "aircon": ["🧹","🧪","💨","🔧","🏗️","📋"],
        "electrical": ["⚡","💡","🔌","🏠","🔋","📜"],
        "door-repair": ["🔧","🔒","📐","🪵"],
        "wall-mounting": ["📺","📚","🖼️","🔌"],
    }
    data = {
        "plumbing": [
            ["Leak and Pipe Repair","Burst pipes, dripping taps, faucet replacements. We stop the leak fast."],
            ["Toilet Unblock and Fix","Choked toilet bowl, slow-flushing drain. Cleared professionally."],
            ["Water Heater","Electric or gas install and repair. Ariston, Panasonic, Rheem."],
            ["HDB Plumbing","Concealed pipes, exposed pipe work, toilet bowl replacement. HDB-compliant."],
            ["Pipe Replacement","Old copper, PVC, or PEX pipes rerouted or replaced."],
            ["Bathroom Fitting","Shower mixer, basin installation, sanitary ware. Professional finish."],
        ],
        "handyman": [
            ["Furniture Assembly","IKEA, Courts, Harvey Norman. Assemble flat-pack right."],
            ["Painting and Touch-ups","Room repainting, patching holes, peeling paint fix."],
            ["Light Fixtures","Ceiling fans, pendant lights, LED downlights. Safe install."],
            ["Curtains and Blinds","Curtain rod, track, and blind install. Precise leveling."],
            ["General Repairs","Loose tiles, squeaky doors, broken handles. Every small repair."],
            ["Moving Help","Disassemble, heavy lifting, reassemble."],
        ],
        "aircon": [
            ["General Wash","Filter clean, coil clean, drain flush for efficiency."],
            ["Chemical Wash","Deep clean for stubborn buildup. Better airflow."],
            ["Gas Top-Up","R22, R32, R410A refill for warm-running units."],
            ["Repair and Diagnose","Not turning on? Noise? Leaking? We fix it."],
            ["New Installation","HDB and Condo. Mitsubishi, Daikin, Panasonic."],
            ["Service Contract","Annual maintenance. Keep warranty valid."],
        ],
        "electrical": [
            ["Power Trip Fix","Burnt MCBs, faulty RCBOs. Root cause fixed."],
            ["Lighting","Downlights, pendant lights, LED strips, ceiling fans."],
            ["Socket Repair","Loose sockets, sparking switches, dead power points."],
            ["New Wiring","Renovation, BTO. Surface or concealed wiring."],
            ["DB Box and Breaker","Upgrade board, surge protection, earth leakage."],
            ["EMA Licensed Work","All work EMA certified. Safe, insured."],
        ],
        "door-repair": [
            ["Hinge Repair","Squeaky or loose hinges. Tightened or replaced."],
            ["Lock Replacement","Lost keys, broken latches, digital locks."],
            ["Door Alignment","Dragging or won't latch? Fixed smooth."],
            ["Wooden Door Fixes","Swollen, cracked, splintered. Refurbished."],
        ],
        "wall-mounting": [
            ["TV Mounting","LED, OLED, QLED. Fixed, tilt, full-motion."],
            ["Shelf Installation","Floating, bookshelves, kitchen racks. Anchored."],
            ["Picture and Art","Museum-quality hanging for art and mirrors."],
            ["Cable Management","Clean wire hiding behind TVs."],
        ],
    }
    items = data[svc_name]
    lines = []
    for i, (name, desc) in enumerate(items):
        ic = icons[svc_name][i]
        txt = desc
        if extra_text:
            txt = txt.rstrip(".") + extra_text
        lines.append('      <div class="sub-item"><div class="sub-icon" style="background:$TINT;">' + ic + '</div><div><h3>' + name + '</h3><p>' + txt + '</p></div></div>')
    return "\n".join(lines)

# Service configs
SVCS = [
    {
        "slug": "plumbing",
        "badge": "Plumbing",
        "hl": "Plumber in Singapore",
        "lead": "We connect you with trusted plumbers across Singapore. Fast response, fair prices.",
        "price": "\u002450-\u002480 for simple fixes. Emergency: \u0024100-\u0024300+.",
        "faq_q": ["How much does a plumber cost?","Same-day plumber available?","Do you cover all areas?","How long does it take?"],
        "faq_a": ["Simple fixes \u002450-\u002480. Emergency: \u0024100-\u0024300+.","Yes, most plumbers offer same-day or 24-hour emergency.","Yes! All HDB estates, condos, and landed properties.","Most fixes done within 30-60 minutes."],
        "price_range": "\u002450-\u0024300",
        "svc_types": ["Plumbing Singapore","Leak Repair Singapore","Toilet Unblock Singapore","Water Heater Singapore","HDB Plumbing Singapore"],
        "tint": "#E3F2FD", "tint_txt": "#1565C0",
    },
    {
        "slug": "handyman",
        "badge": "Handyman",
        "hl": "Handyman in Singapore",
        "lead": "We connect you with reliable handymen. Small jobs welcome!",
        "price": "Small tasks \u002440-\u002480. Larger projects: \u002480-\u0024200.",
        "faq_q": ["Cost of a handyman?","Same-day handyman?","What can a handyman do?"],
        "faq_a": ["Small jobs \u002440-\u002480. Larger projects \u002480-\u0024200.","Most arrive within 24 hours, many same-day.","Assembly, painting, light fixtures, curtains, general house repairs."],
        "price_range": "\u002440-\u0024200",
        "svc_types": ["Handyman Singapore","Furniture Assembly Singapore","Painting Singapore","Light Installation Singapore","General Repair Singapore"],
        "tint": "#FFF3E0", "tint_txt": "#E65100",
    },
    {
        "slug": "aircon",
        "badge": "Aircon Servicing",
        "hl": "Aircon Servicing in Singapore",
        "lead": "We connect you with experienced aircon technicians. Same-day from \u002440/unit.",
        "price": "General wash \u002440-\u002455/unit. Chemical \u002480-\u0024120/unit. Gas \u002460-\u0024150.",
        "faq_q": ["How often to service?","Cost of aircon service?","All aircon brands?"],
        "faq_a": ["Every 3-4 months for general wash. Chemical every 12-18 months.","General \u002440-\u002455/unit. Chemical \u002480-\u0024120. Gas \u002460-\u0024150.","Yes - Mitsubishi, Daikin, Panasonic, York, LG, Carrier, Midea."],
        "price_range": "\u002440-\u0024150",
        "svc_types": ["Aircon Servicing Singapore","Chemical Wash Singapore","Gas Top-Up Singapore","Aircon Repair Singapore","Aircon Installation Singapore"],
        "tint": "#E0F7FA", "tint_txt": "#00695C",
    },
    {
        "slug": "electrical",
        "badge": "Electrical",
        "hl": "Electrician in Singapore",
        "lead": "We connect you with EMA licensed electricians. Emergency service available.",
        "price": "Socket replacement from \u002450-\u002480. Power trip repair \u002480-\u0024200.",
        "faq_q": ["Cost of electrician?","Can I fix power trip myself?","Emergency electrician?","What is EMA licensed?"],
        "faq_a": ["\u002450-\u002480 for simple fixes. Power trip \u002480-\u0024200.","No. Dangerous and illegal. Call EMA licensed pros.","Yes! Many offer same-day or 2-hour response.","Energy Market Authority licensing required for all electrical work in Singapore."],
        "price_range": "\u002450-\u0024200",
        "svc_types": ["Electrical Services Singapore","Power Trip Fix Singapore","Lighting Installation Singapore","Socket Repair Singapore","New Wiring Singapore"],
        "tint": "#FFEBEE", "tint_txt": "#C62828",
    },
    {
        "slug": "door-repair",
        "badge": "Door Repair",
        "hl": "Door Repair in Singapore",
        "lead": "Door repair experts available same-day. HDB main doors, bedroom doors.",
        "price": "Adjustment from \u002450-\u002480. Lock replacement \u002480-\u0024200.",
        "faq_q": ["Door repair cost?","How fast?","Repair or replace?"],
        "faq_a": ["\u002450-\u002480 adjustments. Lock replacement \u002480-\u0024200.","Same-day. Emergency lockouts: 1-2 hours.","If frame solid, repair cheaper. Water-damaged may need replacement."],
        "price_range": "\u002450-\u0024250",
        "svc_types": ["Door Repair Singapore","Hinge Repair Singapore","Lock Replacement Singapore","Door Alignment Singapore","Wooden Door Fix Singapore"],
        "tint": "#F3E5F5", "tint_txt": "#6A1B9A",
    },
    {
        "slug": "wall-mounting",
        "badge": "Wall Mounting",
        "hl": "TV and Wall Mounting Singapore",
        "lead": "Wall mounting professionals available now. From \u002440. Safe and secure.",
        "price": "TV mounting from \u002440-\u002460. Heavy items \u002460-\u0024120.",
        "faq_q": ["TV mounting cost?","Can you mount on HDB walls?","Do you provide the bracket?"],
        "faq_a": ["\u002440-\u002460 for TV. Heavy items \u002460-\u0024120.","Yes. Concrete, partition, or drywall.","You can provide yours or we source one."],
        "price_range": "\u002440-\u0024120",
        "svc_types": ["TV Wall Mounting Singapore","Shelf Installation Singapore","Picture Hanging Singapore","Cable Management Singapore"],
        "tint": "#ECEFF1", "tint_txt": "#37474F",
    },
]

count = 0

for svc in SVCS:
    subs = build_subs(svc["slug"])
    
    # FAQ HTML
    fhtml = ""
    for i in range(len(svc["faq_q"])):
        fhtml += '      <details class="faq-item"><summary class="faq-summary">' + svc["faq_q"][i] + '</summary><div class="faq-answer"><p>' + svc["faq_a"][i] + '</p></div></details>\n'
    
    # FAQ schema
    fs = []
    for i in range(len(svc["faq_q"])):
        fs.append(json.dumps({"@type":"Question","name":svc["faq_q"][i],"acceptedAnswer":{"@type":"Answer","text":svc["faq_a"][i].replace("<strong>","").replace("</strong>","")}}))
    
    biz = json.dumps({"@context":"https://schema.org","@type":"LocalBusiness","name":"HARLO UNKLE - " + svc["hl"],"description":"HARLO UNKLE " + svc["hl"],"telephone":"[INSERT NUMBER]","priceRange":svc["price_range"],"areaServed":[{"@type":"Country","name":"Singapore"}],"serviceType":svc["svc_types"]})
    
    p = render(TPL,
        TITLE=svc["hl"] + " | HARLO UNKLE",
        DESC=svc["lead"],
        KEYWORDS=", ".join(svc["svc_types"]),
        OG_TITLE=svc["hl"] + " | HARLO UNKLE",
        OG_DESC=svc["lead"],
        CANONICAL="https://harlounkle.com/" + svc["slug"] + ".html",
        OG_URL="https://harlounkle.com/" + svc["slug"] + ".html",
        CSS_PATH="/style.css",
        BADGE=svc["badge"],
        HEADLINE=svc["hl"],
        LEAD=svc["lead"],
        QUOTE_EXTRA="",
        PRICE=svc["price"],
        SUBS_HEADING="Services we provide",
        SUBS=subs,
        CTA_HELP_LABEL="Need help?",
        CTA_PHONE_HINT="We'll find you a local provider.",
        FAQ_HEADING="Common Questions",
        FAQS=fhtml,
        REGION_LINKS=build_region_links(svc["slug"]),
        BOTTOM_CTA_TITLE="Need Help Now?",
        BOTTOM_CTA_BODY="One call. We route you to the nearest provider.",
        WA_TEXT="Hi%20Unkle%2C%20I%20need%20help",
        TINT_TEXT=svc["tint_txt"],
        TINT_BG=svc["tint"],
        BUSINESS_SCHEMA=biz,
        FAQ_SCHEMA="{\"@context\":\"https://schema.org\",\"@type\":\"FAQPage\",\"mainEntity\":[" + ", ".join(fs) + "]}",
    )
    
    with open(os.path.join(BASE, svc["slug"] + ".html"), "w") as f:
        f.write(p)
    count += 1
    print("OK: " + svc["slug"] + ".html")
    
    # Regional pages
    for a_slug, a_label in AREAS.items():
        a_subs = build_subs(svc["slug"], " Trusted service in " + a_label + ".")
        a_f = ""
        for i in range(len(svc["faq_q"])):
            q = svc["faq_q"][i].rstrip("?") + " in " + a_label + "?"
            a_f += '      <details class="faq-item"><summary class="faq-summary">' + q + '</summary><div class="faq-answer"><p>' + svc["faq_a"][i] + '</p></div></details>\n'
        
        a_fs = []
        for i in range(len(svc["faq_q"])):
            q = svc["faq_q"][i].rstrip("?") + " in " + a_label + "?"
            a_fs.append(json.dumps({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":svc["faq_a"][i].replace("<strong>","").replace("</strong>","")}}))
        
        a_biz = json.dumps({"@context":"https://schema.org","@type":"LocalBusiness","name":"HARLO UNKLE " + svc["badge"] + " " + a_label,"description":svc["badge"] + " services in " + a_label + ", Singapore.","telephone":"[INSERT NUMBER]","priceRange":svc["price_range"],"areaServed":[{"@type":"Country","name":"Singapore"},{"@type":"Place","name":a_label + ", Singapore"}],"serviceType":[s.replace(" Singapore"," in " + a_label) for s in svc["svc_types"]]})

        # Group areas by URA region for smarter cross-linking
        REGIONS = {
            "North": ["woodlands","yishun","sembawang"],
            "North-East": ["ang-mo-kio","hougang","sengkang","punggol","serangoon"],
            "East": ["bedok","pasir-ris","tampines","changi","pay-lebar"],
            "West": ["jurong-west","jurong-east","clementi","bukit-batok","bukit-panjang","choa-chu-kang","pioneer"],
            "Central": ["bishan","toa-payoh","geylang","kallang","queenstown","buki-timah","novena","orchard","marine-parade"],
        }
        # Find which region this area belongs to
        current_region = None
        for reg, reg_areas in REGIONS.items():
            if a_slug in reg_areas:
                current_region = reg
                break
        # Show same-region areas (excluding current area)
        nearby_areas = []
        if current_region:
            nearby_areas = [(slug, AREAS[slug]) for slug in REGIONS[current_region] if slug != a_slug and slug in AREAS]
        alinks = []
        for os2, ol2 in nearby_areas:
            alinks.append('<a href="/services/' + svc["slug"] + '-' + os2 + '.html">' + ol2 + '</a>')
        rhtml = '\n  <div class="region-areas"><h3>We also serve nearby areas</h3><div class="region-grid">' + "\n      ".join(alinks) + "\n    </div></div>"
        
        wa = "Hi%20Unkle%2C%20I%20need%20" + svc["slug"] + "%20near%20" + a_label.replace(" ","%20")
        
        p2 = render(TPL,
            TITLE=svc["badge"] + " " + a_label + " | HARLO UNKLE",
            DESC=svc["badge"] + " services in " + a_label + ", Singapore. Book now.",
            KEYWORDS=svc["slug"] + " " + a_slug.replace("-"," ") + ", " + ", ".join(svc["svc_types"]),
            OG_TITLE=svc["badge"] + " " + a_label + " | HARLO UNKLE",
            OG_DESC=svc["badge"] + " available in " + a_label + ", Singapore.",
            CANONICAL="https://harlounkle.com/services/" + svc["slug"] + "-" + a_slug + ".html",
            OG_URL="https://harlounkle.com/services/" + svc["slug"] + "-" + a_slug + ".html",
            CSS_PATH="/style.css",
            BADGE=svc["badge"] + " in " + a_label,
            HEADLINE=svc["badge"] + " " + a_label,
            LEAD="Trusted " + svc["badge"].lower() + " services available in " + a_label + ". Get a free quote today.",
            QUOTE_EXTRA=" in " + a_label,
            PRICE=svc["price"],
            SUBS_HEADING=svc["badge"] + " in " + a_label,
            SUBS=a_subs,
            CTA_HELP_LABEL="Need " + svc["badge"].lower() + " in " + a_label + "?",
            CTA_PHONE_HINT="Provider near " + a_label + ".",
            FAQ_HEADING="Common Questions in " + a_label,
            FAQS=a_f,
            REGION_LINKS=rhtml,
            BOTTOM_CTA_TITLE="Need Help in " + a_label + "?",
            BOTTOM_CTA_BODY="We route you to the nearest provider in " + a_label + ".",
            WA_TEXT=wa,
            TINT_TEXT=svc["tint_txt"],
            TINT_BG=svc["tint"],
            BUSINESS_SCHEMA=a_biz,
            FAQ_SCHEMA="{\"@context\":\"https://schema.org\",\"@type\":\"FAQPage\",\"mainEntity\":[" + ", ".join(a_fs) + "]}",
        )
        
        rpath = os.path.join(BASE, "services", svc["slug"] + "-" + a_slug + ".html")
        os.makedirs(os.path.dirname(rpath), exist_ok=True)
        with open(rpath, "w") as f:
            f.write(p2)
        count += 1

print("Total: " + str(count) + " pages (6 main + 60 regional)")
