import os, json
from pathlib import Path
from string import Template

BASE = Path('/Users/garethlee/harlo-unkle')
AREAS = {
    "woodlands":"Woodlands","yishun":"Yishun","sembawang":"Sembawang","ang-mo-kio":"Ang Mo Kio",
    "hougang":"Hougang","sengkang":"Sengkang","punggol":"Punggol","serangoon":"Serangoon",
    "bedok":"Bedok","pasir-ris":"Pasir Ris","tampines":"Tampines","changi":"Changi",
    "pay-lebar":"Paya Lebar","jurong-west":"Jurong West","jurong-east":"Jurong East",
    "clementi":"Clementi","bukit-batok":"Bukit Batok","bukit-panjang":"Bukit Panjang",
    "choa-chu-kang":"Choa Chu Kang","pioneer":"Pioneer","bishan":"Bishan",
    "toa-payoh":"Toa Payoh","geylang":"Geylang","kallang":"Kallang",
    "queenstown":"Queenstown","buki-timah":"Bukit Timah","novena":"Novena",
    "orchard":"Orchard","marine-parade":"Marine Parade",
}
REGIONS = {
    "North":["woodlands","yishun","sembawang"],
    "North-East":["ang-mo-kio","hougang","sengkang","punggol","serangoon"],
    "East":["bedok","pasir-ris","tampines","changi","pay-lebar"],
    "West":["jurong-west","jurong-east","clementi","bukit-batok","bukit-panjang","choa-chu-kang","pioneer"],
    "Central":["bishan","toa-payoh","geylang","kallang","queenstown","buki-timah","novena","orchard","marine-parade"],
}
SVCS = [
    {"slug":"plumbing","badge":"Plumbing","lead":"We connect you with trusted plumbers across Singapore. Fast response, fair prices.","price":"Simple fixes $50-$80. Emergency: $100-$300+.","price_range":"$50-$300","svc_types":["Plumbing Singapore","Leak Repair Singapore","Toilet Unblock Singapore","Water Heater Singapore","HDB Plumbing Singapore"],"subs":[("Leak and Pipe Repair","Burst pipes, dripping taps, faucet replacements. We stop leaks quickly."),("Toilet Unblock","Choked toilet bowl, slow drains. Cleared professionally."),("Water Heater","Electric or gas install and repair. Ariston, Panasonic, Rheem."),("HDB Plumbing","Concealed/exposed pipe work, bowl replacement. HDB-compliant."),("Pipe Replacement","Copper, PVC, or PEX reroutes and replacement."),("Bathroom Fitting","Shower mixer, basin, sanitary ware install.")]},
    {"slug":"handyman","badge":"Handyman","lead":"We connect you with reliable handymen. Small jobs welcome!","price":"Small tasks $40-$80. Larger projects: $80-$200.","price_range":"$40-$200","svc_types":["Handyman Singapore","Furniture Assembly Singapore","Painting Singapore","Light Installation Singapore","General Repair Singapore"],"subs":[("Furniture Assembly","IKEA, Courts, Harvey Norman. Assembled correctly."),("Painting and Touch-ups","Room repainting, patching holes, peeling fixes."),("Light Fixtures","Ceiling fans, pendant lights, LED downlights."),("Curtains and Blinds","Rods, tracks, blinds. Level install."),("General Repairs","Loose tiles, squeaky doors, handles."),("Moving Help","Disassemble, heavy lifting, reassembly.")]},
    {"slug":"aircon","badge":"Aircon Servicing","lead":"We connect you with experienced aircon technicians. Same-day from $40/unit.","price":"General wash $40-$55/unit. Chemical $80-$120/unit. Gas refill $60-$150.","price_range":"$40-$150","svc_types":["Aircon Servicing Singapore","Chemical Wash Singapore","Gas Top-Up Singapore","Aircon Repair Singapore","Aircon Installation Singapore"],"subs":[("General Wash","Filter clean, coil clean, drain flush for efficiency."),("Chemical Wash","Deep clean for stubborn buildup. Improves airflow."),("Gas Top-Up","R22, R32, R410A refill when unit is warm-running."),("Repair and Diagnose","Not turning on, noisy, leaking — root-cause fixed."),("New Installation","HDB / Condo installs. Daikin, Mitsubishi, Panasonic, Midea."),("Service Contract","Planned maintenance to keep warranty valid.")]},
    {"slug":"electrical","badge":"Electrical","lead":"We connect you with EMA licensed electricians. Emergency service available.","price":"Socket replacement from $50-$80. Power trip repair $80-$200.","price_range":"$50-$200","svc_types":["Electrical Services Singapore","Power Trip Fix Singapore","Lighting Installation Singapore","Socket Repair Singapore","New Wiring Singapore"],"subs":[("Power Trip Fix","Burnt MCBs, faulty RCBOs. Root-cause repaired."),("Lighting","Downlights, pendants, LED strips, ceiling fans."),("Socket Repair","Loose sockets, sparking switches, dead power points."),("New Wiring","Renovation / BTO. Surface or concealed wiring."),("DB Box and Breaker","Board upgrade, surge protection, earth leakage."),("EMA Licensed Work","EMA-certified work. Safe, insured, compliant.")]},
    {"slug":"door-repair","badge":"Door Repair","lead":"Door repair experts available same-day. HDB main doors, bedroom doors, digital locks.","price":"Adjustment from $50-$80. Lock replacement $80-$200.","price_range":"$50-$250","svc_types":["Door Repair Singapore","Hinge Repair Singapore","Lock Replacement Singapore","Door Alignment Singapore","Wooden Door Fix Singapore"],"subs":[("Hinge Repair","Squeaky or loose hinges. Tightened or replaced."),("Lock Replacement","Lost keys, broken latches, digital locks."),("Door Alignment","Dragging or latch failure? Smoothened."),("Wooden Door Fixes","Swollen, cracked, splintered refurbishment.")]},
    {"slug":"wall-mounting","badge":"Wall Mounting","lead":"Wall mounting professionals available now. From $40. Safe and secure.","price":"TV mounting $40-$60. Heavy items $60-$120.","price_range":"$40-$120","svc_types":["TV Wall Mounting Singapore","Shelf Installation Singapore","Picture Hanging Singapore","Cable Management Singapore"],"subs":[("TV Mounting","LED, OLED, QLED. Fixed, tilt, full-motion brackets."),("Shelf Installation","Floating, bookshelves, kitchen racks anchored well."),("Picture and Art","Museum-quality hanging for art and mirrors."),("Cable Management","Clean wire hiding behind TVs.")]},
    {"slug":"toilet-waterproofing","badge":"Toilet Waterproofing","lead":"We connect you with waterproofing specialists. HDB leak repair, PU injection.","price":"PU injection from $300. Full hack waterproofing $800-$1,800.","price_range":"$300-$1,800","svc_types":["Toilet Waterproofing Singapore","PU Injection Singapore","HDB Waterproofing Singapore","Leak Repair Singapore","Waterproofing Contractor Singapore"],"subs":[("PU Injection","Targeted leak sealing for HDB toilets."),("Full Hack Waterproofing","Strip-and-recoat where PU isn't enough."),("HDB Leak Repair","Ceiling stains, grout fouling, floor tiles lifted."),("Condo Waterproofing","Common-area dispute leaks and unit-side fixes."),("Outside Inspections","Roof/balcony seal repairs before interior damage.")]},
    {"slug":"epoxy-grouting","badge":"Epoxy Grouting","lead":"Mould-proof tile regrouting specialists for HDB and condo.","price":"Cement grout $180-$300. Epoxy grout $300-$600 for typical HDB bathroom.","price_range":"$180-$600","svc_types":["Epoxy Grouting Singapore","Tile Regrouting Singapore","HDB Bathroom Grouting Singapore","Mould Proof Grouting Singapore"],"subs":[("Epoxy Grouting","Mould-proof, waterproof finish for wet areas."),("Cement Grout Regrouting","Traditional regrout with anti-mould treatment."),("Tile Preparation","Cleaning out old cement and debris."),("Sealing Advice","How to protect your grout after regrouting.")]},
    {"slug":"appliance-repair","badge":"Appliance Repair","lead":"We connect you with appliance repair specialists. Fridge, washer, oven.","price":"General diagnostics $50-$90. Repair quote given before work.","price_range":"$50-$200","svc_types":["Appliance Repair Singapore","Fridge Repair Singapore","Washer Repair Singapore","Oven Repair Singapore"],"subs":[("Fridge Repair","Not cooling, leaking, noisy compressor diagnostics."),("Washer Repair","Spin failure, drum noise, leak or error codes."),("Oven Repair","Heating element, thermostat, door seal issues."),("Dryer Repair","Vent block, sensor failure, no heat.")]},
    {"slug":"locksmith","badge":"Locksmith","lead":"24hr emergency lockout help. Digital locks, HDB main doors, gates.","price":"Lockout callout $80-$180. Digital lock install $120-$300.","price_range":"$80-$300","svc_types":["Locksmith Singapore","Emergency Locksmith Singapore","Digital Lock Singapore","Lock Change Singapore","Gate Lock Repair Singapore"],"subs":[("Emergency Unlock","Locked out. Non-destructive opening when possible."),("Digital Lock Install","Schlage, Yale, Danalock Types supported."),("Lock Replacement","Cylinder change, knob sets, deadbolts."),("Gate Lock Repair","Gate latch, auto-gate motor basics.")]},
]
curated = [
    ("How to Vet a Home Services Provider in Singapore: 7 Questions","/blog/how-to-vet-home-services-provider-singapore.html","Guides"),
    ("HDB Home Repairs: What You Can and Can't Do Yourself","/blog/hdb-home-repairs-diy-guide.html","HDB"),
    ("HDB vs Condo Home Services: Do You Actually Pay More?","/blog/hdb-vs-condo-home-services-costs.html","Guides"),
    ("Emergency Plumber Singapore: What to Do Before They Arrive","/blog/emergency-plumber-singapore-2026.html","Plumbing"),
    ("HDB Pipe Leak Singapore: Complete Guide — Causes, Fixes, and When to Call a Pro","/blog/hdb-pipe-leak-singapore-guide.html","Plumbing"),
    ("Aircon Servicing vs Chemical Overhaul: Which Does Your HDB Need?","/blog/aircon-servicing-singapore-chemical-wash-vs-general.html","Aircon"),
    ("Why Your Aircon Smells Like Mould in Singapore (And How to Fix It)","/blog/aircon-smell-mould-singapore-fix.html","Aircon"),
    ("Emergency Electrician Singapore: What’s Actually an Emergency?","/blog/emergency-electrician-singapore-what-to-know.html","Electrical"),
    ("HDB Toilet Waterproofing: PU vs Full Hack — Cost Comparison","/blog/hdb-toilet-waterproofing-pu-vs-hack.html","Waterproofing"),
    ("Epoxy Grouting in Singapore: Is It Worth It for HDB Bathrooms?","/blog/epoxy-grouting-singapore-pros-cons.html","Grouting"),
    ("Appliance Repair Singapore: 5 Fridge & Washer Warning Signs","/blog/appliance-repair-signs-you-need-a-pro.html","Appliance Repair"),
]

# Sanitize services: remove duplicate leftover pages containing old template fragments
for p in list((BASE/'services').glob('*.html')):
    if p.read_text().count('<!-- rebuild marker -->') > 1:
        p.unlink()

CARD_TMPL = '<a href="$url" style="text-decoration:none;color:inherit;"><div style="background:#fff;border-radius:16px;padding:1.25rem;box-shadow:0 2px 10px rgba(0,0,0,0.06);border:1px solid var(--border);"><div style="font-size:0.7rem;font-weight:700;color:#E91E63;background:#FCE4EC;display:inline-block;padding:3px 10px;border-radius:999px;margin-bottom:0.5rem;">$svc_label</div><h3 style="font-size:1.05rem;margin:0 0 0.6rem;line-height:1.35;">$title</h3><p style="color:#6B7280;font-size:0.9rem;margin:0;">Quick guide from Harlo Unkle. <span style="color:#E91E63;font-weight:700;">Read more →</span></p></div></a>'
proof = '''<div class="service-cta" style="margin-top:1.25rem"><h3>Trusted local help with clear pricing</h3><a href="tel:[INSERT NUMBER]" class="btn btn-primary btn-lg">CALL UNKLE NOW</a><div class="phone-sm">Usually responds within the hour.</div></div><div class="price-box" style="margin-top:1rem;">Rated 4.9 out of 5 by homeowners. No hidden fees, pay the provider direct.</div>

'''
marker = '<div style="background:var(--bg-subtle);border-top:1px solid var(--border);border-bottom:1px solid var(--border);" class="section">\n      <div class="container">\n        <div class="section-header">\n          <span class="section-label">Related Guides</span>\n          <h2>Recommended Reading</h2>\n        </div>\n        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1rem;">$related</div>\n      </div>\n    </div>\n\n    <section class="cta-section">'
last_updated = '<time datetime="2026-07-21" style="font-size:0.8rem;color:#9CA3AF;display:block;margin-top:0.75rem;">Last updated: 21 Jul 2026</time>'
script_footer = '''<script>
document.addEventListener('click', function(e) {
  var target = e.target.closest('a');
  if (!target || !target.hasAttribute('href')) return;
  var href = target.getAttribute('href');
  var payload = {'page_location': window.location.href, 'page_title': document.title};
  if (href.indexOf('tel:') === 0) {
    try {
      navigator.sendBeacon('https://www.google-analytics.com/g/collect?'
        + 'v=2&tid=G-Q82QGJL0E4&cid=' + (window.ga_cid || Math.random().toString(36).slice(2))
        + '&en=call_click&dl=' + encodeURIComponent(window.location.href)
        + '&dt=' + encodeURIComponent(document.title));
    } catch(e) {}
    if (typeof gtag === 'function') gtag('event', 'call_click', payload);
  }
  if (href.indexOf('wa.me') !== -1) {
    if (typeof gtag === 'function') gtag('event', 'whatsapp_click', payload);
  }
});
</script>
</body>
</html>
<!-- rebuild marker -->'''

result = '''<!DOCTYPE html>
<html lang="en-SG">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>$title</title>
  <meta name="description" content="$desc">
  <meta name="keywords" content="$keywords">
  <meta name="robots" content="index, follow">
  <meta property="og:title" content="$og_title">
  <meta property="og:description" content="$og_desc">
  <meta property="og:type" content="website">
  <meta property="og:url" content="$url">
  <meta property="og:locale" content="en_SG">
  <link rel="canonical" href="$url">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2216%22 fill=%22%23E91E63%22/><text x=%2250%22 y=%2268%22 text-anchor=%22middle%22 font-size=%2256%22 font-weight=%22900%22 fill=%22white%22 font-family=%22sans-serif%22>H</text></svg>">
  <link rel="stylesheet" href="/style.css">
  <meta name="article:author" content="Harlo Unkle Editorial Team">
  <meta name="article:published_time" content="2026-06-01">
  $last_updated
  <script type="application/ld+json">$biz</script>
  <script type="application/ld+json">$faq</script>
  <script type="application/ld+json">$breadcrumb</script>
  <script type="application/ld+json">$article</script>
</head>
<body class="sticky-cta-active">
  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="logo"><div class="logo-mark">H</div><span>HARLO UNKLE</span></a>
      <a href="tel:[INSERT NUMBER]" class="header-cta">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6A19.79 19.79 0 012.12 4.11 2 2 0 014.11 2h3a2 2 0 012 1.72c.13.95.36 1.88.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.92.34 1.86.57 2.81.7A2 2 0 0122 16.92z"/></svg>
        Call Unkle
      </a>
    </div>
  </header>
  <section class="service-hero">
    <div class="service-badge" style="color:$badge_text;background:$badge_bg;">$badge in $area_label</div>
    <h1>$headline</h1>
    <p>$lead</p>
  </section>
  <div class="container">
    <div class="service-cta">
      <h3>$cta_help</h3>
      <a href="tel:[INSERT NUMBER]" class="btn btn-primary btn-lg">CALL UNKLE NOW</a>
      <div class="phone-sm">$cta_hint</div>
    </div>
    <div class="price-box">$price</div>
    <div class="section-header">
      <span class="section-label">What We Do</span>
      <h2>$subs_heading</h2>
    </div>
    <div class="sub-list">$subs</div>
    $proof
    <div class="section-header" style="padding-top:2rem">
      <span class="section-label">FAQ</span>
      <h2>$faq_heading</h2>
    </div>
    <div class="faq-list">$faq_html</div>
    ${region_links}
  </div>
  ${related_block}
  <section class="cta-section">
    <h2>${bottom_title}</h2>
    <p>${bottom_body}</p>
    <a href="tel:[INSERT NUMBER]" class="btn btn-primary btn-lg">CALL UNKLE NOW</a>
    <div class="phone"><a href="tel:[INSERT NUMBER]">[INSERT NUMBER]</a></div>
  </section>
  <footer class="site-footer">
    <div class="footer-brand">HARLO UNKLE</div>
    <div class="footer-links">
      <a href="/">Home</a>
      <a href="/plumbing.html">Plumbing</a>
      <a href="/handyman.html">Handyman</a>
      <a href="/aircon.html">Aircon</a>
      <a href="/electrical.html">Electrical</a>
      <a href="/door-repair.html">Door Repair</a>
      <a href="/wall-mounting.html">Wall Mounting</a>
      <a href="/toilet-waterproofing.html">Toilet Waterproofing</a>
      <a href="/epoxy-grouting.html">Epoxy Grouting</a>
      <a href="/appliance-repair.html">Appliance Repair</a>
      <a href="/locksmith.html">Locksmith</a>
    </div>
    <div class="footer-legal">
      <a href="/blog.html">Blog</a>
      <a href="/privacy-policy.html">Privacy Policy</a>
      <a href="/terms.html">Terms &amp; Conditions</a>
    </div>
    <div class="footer-copy">© 2026 HARLO UNKLE. All rights reserved.</div>
  </footer>
  <div class="sticky-cta">
    <a href="tel:[INSERT NUMBER]" class="btn btn-call">📞 Call</a>
    <a href="https://wa.me/[INSERT NUMBER]?text=$wa_text" target="_blank" class="btn btn-wa">WhatsApp</a>
  </div>
'''

for svc in SVCS:
    for a_slug, a_label in AREAS.items():
        faqs = [
            ("How much does "+svc['badge'].lower()+" cost in "+a_label+"?"),
            "Simple fixes usually start from $80. Exact quote by photo/phone.",
            ("Same-day "+svc['badge'].lower()+" available in "+a_label+"?"),
            "Yes — many local providers serve "+a_label+" same-day for urgent jobs.",
            ("Do you cover HDB and condo in "+a_label+"?"),
            "Yes. Service covers HDB, condos, and landed along "+a_label+" estates.",
        ]
        faq_html = "\n".join(['      <details class="faq-item"><summary class="faq-summary">'+q+'</summary><div class="faq-answer"><p>'+a+'</p></div></details>' for q,a in zip(faqs[0::2], faqs[1::2])])
        faq_schema_items = ", ".join([json.dumps({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}) for q,a in zip(faqs[0::2], faqs[1::2])])
        faq_json = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['+faq_schema_items+']}'
        breadcrumb = json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://harlounkle.com/"},{"@type":"ListItem","position":2,"name":svc['badge'],"item":"https://harlounkle.com/"+svc['slug']+".html"},{"@type":"ListItem","position":3,"name":a_label,"item":"https://harlounkle.com/services/"+svc['slug']+"-"+a_slug+".html"}]})
        article = json.dumps({"@context":"https://schema.org","@type":"Article","headline":svc['badge']+' '+a_label+' | HARLO UNKLE',"description":svc['badge']+' services in '+a_label+', Singapore. Quick online request, local provider routing.',"author":{"@type":"Organization","name":"Harlo Unkle Editorial Team"},"publisher":{"@type":"Organization","name":"Harlo Unkle"},"datePublished":"2026-06-01","dateModified":"2026-07-21","mainEntityOfPage":{"@type":"WebPage","@id":"https://harlounkle.com/services/"+svc['slug']+"-"+a_slug+".html"}})
        biz = json.dumps({"@context":"https://schema.org","@type":"LocalBusiness","name":"HARLO UNKLE "+svc['badge']+" "+a_label,"description":svc['badge']+" services in "+a_label+", Singapore.","telephone":"[INSERT NUMBER]","priceRange":svc['price_range'],"areaServed":[{"@type":"Country","name":"Singapore"},{"@type":"Place","name":a_label+", Singapore"}],"serviceType":svc['svc_types']})

        cur_region = None
        for reg, sl in REGIONS.items():
            if a_slug in sl:
                cur_region = reg
                break
        near = []
        if cur_region:
            near = [(sl,AREAS[sl]) for sl in REGIONS[cur_region] if sl != a_slug]
        region_links_html = '<div class="region-areas"><h3>We also serve nearby areas</h3><div class="region-grid">\n    '+"\n    ".join(['<a href="/services/'+svc['slug']+'-'+sl+'.html">'+l+'</a>' for sl,l in near])+'\n</div></div>' if near else ''

        seen = set()
        related = []
        for title, url, label in curated:
            if url in seen:
                continue
            seen.add(url)
            related.append((title, url, label))
            if len(related) == 4:
                break
        related_html = "\n".join([Template(CARD_TMPL).substitute(url=u, svc_label=l, title=title.replace('"',"'")) for title,u,l in related])
        wa_text = 'Hi%20Unkle%2C%20I%20need%20'+svc['slug']+'%20near%20'+a_label.replace(' ','%20')

        html = Template(result).substitute(
            title=svc['badge']+' '+a_label+' | HARLO UNKLE',
            desc=svc['badge']+' services in '+a_label+', Singapore. Book now.',
            keywords=svc['slug']+' '+a_slug.replace('-',' ')+', '+", ".join(svc['svc_types']),
            og_title=svc['badge']+' '+a_label+' | HARLO UNKLE',
            og_desc=svc['badge']+' services in '+a_label+' Singapore.',
            url='https://harlounkle.com/services/'+svc['slug']+'-'+a_slug+'.html',
            headline=svc['badge']+' '+a_label,
            badge=svc['badge'],
            badge_text='#1565C0' if svc['slug']=='plumbing' else '#00695C' if svc['slug']=='aircon' else '#C62828' if svc['slug']=='electrical' else '#37474F',
            badge_bg='#E3F2FD' if svc['slug']=='plumbing' else '#E0F7FA' if svc['slug']=='aircon' else '#FFEBEE' if svc['slug']=='electrical' else '#ECEFF1',
            area_label=a_label,
            lead='Trusted '+svc['slug']+' services available in '+a_label+'. Request a free quote today.',
            cta_help='📞 Get a Free Quote in '+a_label,
            cta_hint='Or <a href="https://wa.me/[INSERT NUMBER]?text='+wa_text+'">WhatsApp</a>',
            price=svc['price'],
            subs_heading=svc['badge']+' in '+a_label,
            subs="\n".join(['      <div class="sub-item"><div class="sub-icon" style="background:#E0F7FA;">💧</div><div><h3>'+n+'</h3><p>'+d+'</p></div></div>' for n,d in svc['subs']]),
            proof=proof,
            faq_heading='Common Questions in '+a_label,
            faq_html=faq_html,
            region_links=region_links_html,
            bottom_title='Need Help in '+a_label+'?',
            bottom_body='We route you to the nearest provider in '+a_label+'.',
            wa_text=wa_text,
            last_updated=last_updated,
            biz=biz,
            faq=faq_json,
            breadcrumb=breadcrumb,
            article=article,
            related_block=Template(marker).substitute(related=related_html),
        )
        path = BASE / 'services' / (svc['slug']+'-'+a_slug+'.html')
        path.write_text(html)

print('wrote service pages')
