#!/usr/bin/env python3
"""Builds the Brandon Hall Hotel and Spa static site into ./site
Shared header/footer are stamped into every page so the output is
plain HTML that GitHub Pages can serve as-is."""
import os, json

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
HOTEL = "Brandon Hall Hotel and Spa"
PHONE, PHONE_HREF = "024 7710 2555", "+442477102555"
EMAIL = "events@brandonhallhotelandspa.com"
BOOK = "https://booking.profitroom.com/en/brandonhallhotelspawarwickshire/home?no-cache=&amp;currency=GBP"
MAPS = "https://maps.app.goo.gl/FGjTuhDh8wG2QdVG7"
IG = "https://www.instagram.com/brandonhallhotelandspa/"
FB = "https://www.facebook.com/brandonhallhotelandspa"
# Where the site is published. Share previews (WhatsApp, Facebook, LinkedIn,
# iMessage) need full addresses, so change this ONE line when the site moves
# to the hotel domain, e.g. "https://www.brandonhallhotelandspa.com",
# then run: python3 tools/build.py
SITE_URL = "https://orngroup.github.io/brandon-website"

NAV_LEFT = [("stay", "rooms-suites/", "Stay"), ("dining", "dining/", "Dining"), ("spa", "spa-leisure/", "Leisure &amp; Wellness")]
NAV_RIGHT = [("weddings", "weddings/", "Weddings"), ("meetings", "meetings-events/", "Meetings &amp; Events"), ("christmas", "christmas/", "Christmas")]

IG_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1.1.4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.7.1-1.1.1-1.7.2-2.1.4-.5.2-.9.4-1.3.8-.4.4-.6.8-.8 1.3-.2.4-.3 1-.4 2.1C2.6 9.9 2.6 10.3 2.6 12s0 2.1.1 3.3c.1 1.1.2 1.7.4 2.1.2.5.4.9.8 1.3.4.4.8.6 1.3.8.4.2 1 .3 2.1.4 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1.1-.1 1.7-.2 2.1-.4.5-.2.9-.4 1.3-.8.4-.4.6-.8.8-1.3.2-.4.3-1 .4-2.1.1-1.2.1-1.6.1-3.3s0-2.1-.1-3.3c-.1-1.1-.2-1.7-.4-2.1-.2-.5-.4-.9-.8-1.3-.4-.4-.8-.6-1.3-.8-.4-.2-1-.3-2.1-.4C15.5 4 15.1 4 12 4zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8zm0 8.1a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4zm6.2-8.3a1.1 1.1 0 1 1-2.3 0 1.1 1.1 0 0 1 2.3 0z"/></svg>'
FB_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21.9v-8.2h2.8l.4-3.2h-3.2V8.4c0-.9.3-1.6 1.6-1.6h1.7V4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.4H7.3v3.2h2.8v8.2h3.4z"/></svg>'
MENU_SVG = '<svg viewBox="0 0 28 28" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 8h22M3 14h22M3 20h22"/></svg>'


def head(p, title, desc, extra=""):
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#2C3E50">
<link rel="canonical" href="__PAGEURL__">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{HOTEL}">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="__PAGEURL__">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE_URL}/assets/img/share.jpg">
<meta property="og:image:secure_url" content="{SITE_URL}/assets/img/share.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{HOTEL}, a white country house across a wide lawn">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE_URL}/assets/img/share.jpg">
<link rel="apple-touch-icon" href="{p}assets/brand/favicon.png">
<script>
/* Mobile splash: decide before the first paint so there's no flash. Once per visit. */
try {{ if (matchMedia("(max-width: 760px)").matches && !sessionStorage.getItem("bhSplash")) document.documentElement.classList.add("splash"); }} catch (e) {{}}
</script>
<link rel="icon" href="{p}assets/brand/favicon.png">
<link rel="preload" href="{p}assets/fonts/italiana-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/lato-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/site.css">
{extra}</head>
<body>
<div class="splash-screen" aria-hidden="true"><img src="{p}assets/brand/logo-gold.svg" alt=""></div>
<a class="skip" href="#main">Skip to main content</a>
'''


def header(p, active):
    def links(items):
        out = []
        for key, href, label in items:
            cur = ' aria-current="page"' if key == active else ""
            out.append(f'<a href="{p}{href}"{cur}>{label}</a>')
        return "\n      ".join(out)
    drawer_links = "".join(f'<a href="{p}{h}">{l}</a>' for _, h, l in NAV_LEFT + NAV_RIGHT + [("o", "offers/", "Offers"), ("x", "out-about/", "Out &amp; About"), ("c", "contact/", "Contact")])
    return f'''<div class="utility">
  <div class="wrap">
    <span class="u-hide">Main Street, Brandon, near Coventry</span>
    <div class="u-links">
      <a href="tel:{PHONE_HREF}">{PHONE}</a>
      <a class="u-hide" href="{p}offers/">Offers</a>
      <a class="u-hide" href="{p}out-about/">Out &amp; About</a>
      <a class="u-hide" href="{p}contact/">Contact</a>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Main">
      {links(NAV_LEFT)}
    </nav>
    <button class="menu-toggle" aria-expanded="false" aria-controls="drawer" aria-label="Open menu" style="justify-self:start">{MENU_SVG}</button>
    <a class="brand-logo" href="{p}index.html" aria-label="{HOTEL} home"><img src="{p}assets/brand/logo-navy.svg" alt="{HOTEL}" width="232" height="151"></a>
    <nav class="nav nav--right" aria-label="Main continued">
      {links(NAV_RIGHT)}
      <a class="btn btn--book" href="{BOOK}" target="_blank" rel="noopener" data-book>Book direct</a>
    </nav>
    <a class="btn btn--book mobile-book" href="{BOOK}" target="_blank" rel="noopener" data-book>Book</a>
  </div>
</header>
<div class="drawer" id="drawer" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="drawer-top"><img src="{p}assets/brand/logo-white.svg" alt=""><button class="close">Close</button></div>
  <nav aria-label="Mobile">{drawer_links}</nav>
  <div class="drawer-meta">
    <p><a href="tel:{PHONE_HREF}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <a class="btn btn--book mt-1" href="{BOOK}" target="_blank" rel="noopener" data-book>Book direct</a>
  </div>
</div>
<main id="main">
'''


def footer(p, scripts=()):
    s = "".join(f'<script src="{p}assets/js/{x}"></script>\n' for x in scripts)
    return f'''</main>
<div class="pattern-band" aria-hidden="true"></div>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img class="flogo" src="{p}assets/brand/logo-gold.svg" alt="{HOTEL}">
        <address>{HOTEL}<br>Main Street, Brandon, Wolston<br>Coventry CV8 3FW</address>
        <p class="mt-1"><a href="{MAPS}" target="_blank" rel="noopener">Find us on Google Maps</a></p>
      </div>
      <div>
        <h4>Stay and visit</h4>
        <ul>
          <li><a href="{p}rooms-suites/">Rooms and suites</a></li>
          <li><a href="{p}dining/">The Clarendon</a></li>
          <li><a href="{p}dining/#book-table">Book a table</a></li>
          <li><a href="{p}spa-leisure/">Leisure and wellness</a></li>
          <li><a href="{p}out-about/">Out and about</a></li>
          <li><a href="{p}offers/">Offers</a></li>
          <li><a href="{BOOK}" target="_blank" rel="noopener" data-book>Book direct</a></li>
        </ul>
      </div>
      <div>
        <h4>Celebrate and meet</h4>
        <ul>
          <li><a href="{p}weddings/">Weddings</a></li>
          <li><a href="{p}meetings-events/">Meetings and events</a></li>
          <li><a href="{p}meetings-events/spaces/">Our event spaces</a></li>
          <li><a href="{p}meetings-events/planner/">Event planner</a></li>
          <li><a href="{p}christmas/">Christmas and New Year</a></li>
        </ul>
      </div>
      <div>
        <h4>Talk to us</h4>
        <ul>
          <li><a href="tel:{PHONE_HREF}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{p}contact/">Contact and directions</a></li>
          <li><a href="{REVIEW_FORM}" target="_blank" rel="noopener">Leave us a review</a></li>
        </ul>
        <div class="social">
          <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{IG_SVG}</a>
          <a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{FB_SVG}</a>
        </div>
      </div>
    </div>
    <div class="foot-base">
      <span>&copy; <span data-year>2026</span> {HOTEL}. 7 Hospitality Management Ltd.</span>
      <span><a href="{p}privacy/">Privacy</a> &nbsp;&nbsp; <a href="{p}accessibility/">Accessibility</a></span>
    </div>
  </div>
</footer>
{s}<script src="{p}assets/js/site.js"></script>
</body>
</html>
'''


HOTEL_IMG = "https://www.brandonhallhotelandspa.com/wp-content/uploads/"

def rimg(p, local, remote, alt, cls="", extra=""):
    """Image stored in this repo once the photo-fetch Action has run;
    until then it loads from the current hotel website."""
    return (f'<img src="{p}assets/img/site/{local}" alt="{alt}" loading="lazy"{(" class=" + chr(34) + cls + chr(34)) if cls else ""} {extra}'
            f'data-fallback="{HOTEL_IMG}{remote}" onerror="if(this.dataset.fallback){{this.src=this.dataset.fallback;this.dataset.fallback=\'\'}}">')


GOOGLE_REVIEWS = "https://www.google.com/maps/search/?api=1&amp;query=Brandon+Hall+Hotel+and+Spa+Coventry"
TRIPADVISOR = "https://www.tripadvisor.co.uk/Hotel_Review-g186403-d34327546-Reviews-Brandon_Hall_Hotel_and_Spa-Coventry_West_Midlands_England.html"

# Guest reviews shown on the home page. Add real reviews only, copied from
# Google or Tripadvisor, with the guest's first name and surname initial.
# (quote, name, source, stars, type of stay). Keep each one short.
GOOGLE_RATING = ("4.0", "1,300")   # update from the Google Business Profile now and then
REVIEW_FORM = "https://g.page/r/CWDf8Eg6xklPEBM/review"
REVIEWS = [
    ("I can honestly say I was beyond surprised by the quality of the food in the restaurant. The service was friendly, not too formal or intrusive. It feels real and like they genuinely care about you and your stay.", "James L.", "Google", 5, "Business stay"),
    ("Great place to stay, helpful staff, large rooms, lovely location and plenty of parking.", "Dan F.", "Google", 4, "Family holiday"),
    ("Beautiful surroundings, calm, quiet, on top friendly staff.", "Shanmugam S.", "Google", 5, "Holiday with friends"),
    ("Large hotel with good facilities. Nice bar and good pool with sauna and steam rooms. Bedroom was large and in good condition.", "Chris W.", "Google", 4, "Couple's holiday"),
    ("Really pleasant work stay at Brandon Hall. Spoke to Alia who was lovely and engaging as a manager.", "Steven L.", "Google", 4, "Work stay"),
    ("Rooms were very clean, food was great and staff were very friendly.", "Guest review", "Tripadvisor", 5, "Family stay"),
]

def stars(n):
    return f'<span class="stars" aria-label="{n} out of 5 stars">' + "".join('<span class="on">★</span>' if i < n else '<span>★</span>' for i in range(5)) + '</span>'

def reviews_html():
    if not REVIEWS:
        return ""
    items = "".join(
        f'<figure class="review-card">{stars(s)}<blockquote>{q}</blockquote>'
        f'<figcaption>{who}<span>{ctx}, via {src}</span></figcaption></figure>'
        for q, who, src, s, ctx in REVIEWS)
    return f'<div class="reviews">{items}</div>'


def dl(p, file, title, sub):
    return f'<a class="download" href="{p}downloads/{file}" download><span class="doc" aria-hidden="true"></span><span><strong>{title}</strong><span>{sub}</span></span></a>'


def write(path, html):
    page = path[:-len("index.html")] if path.endswith("index.html") else path
    html = html.replace("__PAGEURL__", SITE_URL + "/" + page)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", full)


# ----------------------------------------------------------------
# HOME
# ----------------------------------------------------------------
def home():
    p = ""
    schema = {
        "@context": "https://schema.org", "@type": "Hotel", "name": HOTEL,
        "description": "A historic country house hotel and spa in 17 acres of Warwickshire gardens and woodland, near Coventry.",
        "url": SITE_URL + "/", "telephone": "+44 24 7710 2555", "email": EMAIL,
        "image": SITE_URL + "/assets/img/share.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": "Main Street, Brandon", "addressLocality": "Wolston, Coventry", "postalCode": "CV8 3FW", "addressCountry": "GB"},
        "geo": {"@type": "GeoCoordinates", "latitude": 52.383, "longitude": -1.4061},
        "sameAs": [IG, FB],
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in ["Free on-site parking", "Indoor swimming pool", "Restaurant", "Meeting rooms", "Pet-friendly rooms on request"]]
    }
    h = head(p, f"{HOTEL} | Country house hotel near Coventry, Warwickshire",
             "A historic country house hotel in 17 acres of Warwickshire gardens and woodland near Coventry. Rooms, dining, weddings, meetings and events.",
             f'<script type="application/ld+json">{json.dumps(schema)}</script>\n')
    body = f'''
<section class="hero">
  <img src="assets/img/exterior-summer.jpg" alt="The white Georgian frontage of {HOTEL} across a wide lawn under a blue sky" fetchpriority="high">
  <div class="wrap">
    <h1>Your countryside escape in Warwickshire</h1>
    <p>A historic country house in 17 acres of gardens and woodland, a short drive from Coventry, Warwick and Stratford-upon-Avon.</p>
    <div class="btn-row">
      <a class="btn btn--book" href="{BOOK}" target="_blank" rel="noopener" data-book>Book direct</a>
      <a class="btn btn--light" href="meetings-events/planner/">Plan an event</a>
    </div>
  </div>
  <span class="credit">Photograph: Tommy James Photography</span>
</section>

<section class="section">
  <div class="wrap split">
    <div class="a">
      <figure class="mount mount--tall"><img src="assets/img/lounge-fireplace.jpg" alt="The lounge at {HOTEL}, with sofas around an open fireplace beneath a portrait" loading="lazy"></figure>
    </div>
    <div class="b">
      <span class="kicker">Welcome to {HOTEL}</span>
      <h2>Where history feels like home</h2>
      <p class="lede">Step into the calm of a country house where comfort and genuine hospitality meet.</p>
      <p>Set within historic grounds in the heart of Warwickshire, we're a place to slow down, reconnect and enjoy life at a gentler pace. Comfortable rooms, friendly faces and the small, thoughtful touches that make a stay memorable.</p>
      <p>Whether you're exploring Warwick and Stratford-upon-Avon, celebrating with the people you love, or bringing your team together, we'll take care of the rest.</p>
      <div class="btn-row"><a class="textlink" href="rooms-suites/">Our rooms and suites</a></div>
    </div>
  </div>
</section>

<section class="section--tight">
  <div class="wrap">
    <div class="facts">
      <div><strong>17 acres</strong><span>of gardens and woodland to explore</span></div>
      <div><strong>14</strong><span>event spaces, from boardrooms to the Woodlands Suite</span></div>
      <div><strong>280</strong><span>guests at a standing reception</span></div>
      <div><strong>24-hour</strong><span>reception, always here to help</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="intro mb-3">
      <div class="t"><h2>Stay, dine, celebrate</h2></div>
      <div class="c"><p class="lede">However you come to us, for a night away, a wedding or a day of meetings, it's the same country house welcome.</p></div>
    </div>
    <div class="paths">
      <a class="path path--tall" href="rooms-suites/"><img src="assets/img/bedroom-suite.jpg" alt="A suite with a grey upholstered headboard and a wedding dress hanging by the window" loading="lazy"><div class="t"><h3>Stay</h3><span>Rooms and suites overlooking the grounds</span></div></a>
      <a class="path" href="weddings/"><img src="assets/img/wedding-walk.jpg" alt="A bride and groom walking hand in hand across the lawn towards the hotel" loading="lazy"><div class="t"><h3>Weddings</h3><span>Your day, in our 17 acres</span></div></a>
      <a class="path" href="meetings-events/"><img src="assets/img/suite-cabaret-white.jpg" alt="A function suite laid with round tables, white linen and flowers" loading="lazy"><div class="t"><h3>Meetings and events</h3><span>Fourteen spaces and an online planner</span></div></a>
      <a class="path" href="dining/"><img src="assets/img/table-setting.jpg" alt="A round table laid with white linen, gold chargers and flowers" loading="lazy"><div class="t"><h3>The Clarendon</h3><span>Seasonal menus, lunch and dinner</span></div></a>
      <a class="path" href="spa-leisure/"><img src="assets/img/pool.jpg" alt="The indoor swimming pool under a glazed roof" loading="lazy"><div class="t"><h3>Leisure and wellness</h3><span>Indoor pool, gym and fitness centre</span></div></a>
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="intro mb-2">
      <div class="t"><h2>Latest offers</h2></div>
      <div class="c"><p>Book direct with us for the best available rate. <a class="textlink" href="offers/">See all offers</a></p></div>
    </div>
    <div class="offers">
      <a class="offer" href="offers/#suite-dreams"><h3>Suite Dreams</h3><p>Two nights in a Junior Suite with a complimentary dinner for two.</p></a>
      <a class="offer" href="offers/#stay-longer-5th-night"><h3>Book 4 nights, get the 5th free</h3><p>An extra night on us to explore more of Warwickshire.</p></a>
      <a class="offer" href="offers/#stay-3-save-20"><h3>Stay 3 nights and save 20%</h3><p>20% off our Best Available Rate for three nights or more.</p></a>
      <a class="offer" href="offers/#stay-2-save-15"><h3>Stay 2 nights and save 15%</h3><p>15% off our Best Available Rate for two nights or more.</p></a>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="wrap split split--flip">
    <div class="a"><figure class="mount"><img src="assets/img/christmas-table.jpg" alt="A festive dinner table with candles, crackers and glasses of wine" loading="lazy"></figure></div>
    <div class="b">
      <span class="kicker">Christmas and New Year 2026</span>
      <h2>Celebrate the season with us</h2>
      <p>Christmas Party Nights from £45, Festive Afternoon Tea from £40, a four-course Christmas Day lunch and a New Year's Eve masquerade gala, all in the warmth of the country house.</p>
      <div class="btn-row">
        <a class="btn btn--book" href="christmas/">Christmas and New Year</a>
        <a class="btn btn--light" href="downloads/christmas-brochure-2026.pdf" download>Download the brochure</a>
      </div>
    </div>
  </div>
</section>


<section class="section section--white">
  <div class="wrap">
    <div class="intro mb-2">
      <div class="t"><h2>What our guests say</h2></div>
      <div class="c">
        <p class="rating-line"><strong>{GOOGLE_RATING[0]}</strong> {stars(4)} <span>from over {GOOGLE_RATING[1]} Google reviews</span></p>
        <p><a class="textlink" href="{GOOGLE_REVIEWS}" target="_blank" rel="noopener">Read our Google reviews</a> &nbsp; <a class="textlink" href="{TRIPADVISOR}" target="_blank" rel="noopener">See us on Tripadvisor</a></p>
      </div>
    </div>
    {reviews_html()}
    <div class="review-cta">
      <p>Stayed with us recently? We'd love to hear how it went.</p>
      <a class="btn btn--navy" href="{REVIEW_FORM}" target="_blank" rel="noopener">Leave us a Google review</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="a">
      <span class="kicker">Getting here</span>
      <h2>In the heart of Warwickshire</h2>
      <p>We're on Main Street in the village of Brandon, just outside Coventry. Warwick, Kenilworth and Stratford-upon-Avon are all within easy reach. Use CV8 3FW for sat nav.</p>
      <address class="mt-1" style="font-style:normal">{HOTEL}<br>Main Street, Brandon, Wolston<br>Coventry CV8 3FW</address>
      <div class="btn-row">
        <a class="btn btn--line" href="{MAPS}" target="_blank" rel="noopener">Get directions</a>
        <a class="btn btn--line" href="tel:{PHONE_HREF}">Call {PHONE}</a>
      </div>
    </div>
    <div class="b"><figure class="mount"><img src="assets/img/exterior-front.jpg" alt="The front of the hotel with its glazed porch and bay windows" loading="lazy"></figure></div>
  </div>
</section>
'''
    write("index.html", h + header(p, "home") + body + footer(p))


# ----------------------------------------------------------------
# MEETINGS & EVENTS HUB
# ----------------------------------------------------------------
def meetings():
    p = "../"
    h = head(p, f"Meetings and events | {HOTEL}",
             "Meeting rooms and event spaces near Coventry for up to 280 guests, with day delegate and 24-hour packages, bedrooms and an online event planner.")
    body = f'''
<section class="hero hero--page">
  <img src="../assets/img/suite-theatre-2.jpg" alt="A function suite with rows of chairs facing the windows" fetchpriority="high">
  <div class="wrap">
    <h1>Meetings and events</h1>
    <p>From a board meeting for six to a conference for 120 and a gala dinner for 200, in a calm country house setting.</p>
    <div class="btn-row">
      <a class="btn btn--book" href="planner/">Plan your event</a>
      <a class="btn btn--light" href="spaces/">Find a room</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap intro">
    <div class="t">
      <h2>Room to think, space to breathe</h2>
    </div>
    <div class="c">
      <p class="lede">{HOTEL} offers the balance of professionalism, comfort and memorable surroundings that makes a meeting work.</p>
      <p>Set within landscaped grounds, the hotel gives your team a calm, inspiring place to focus, with flexible spaces for everything from interviews to conferences, celebrations and corporate dinners.</p>
      <p>Bedrooms on site let multi-day events flow without anyone watching the clock, and the spa and leisure club are there for team-building, a swim before breakfast or simply a break from a busy schedule.</p>
    </div>
  </div>
  <div class="wrap mt-3">
    <div class="facts">
      <div><strong>14</strong><span>meeting and event spaces</span></div>
      <div><strong>280</strong><span>guests at a standing reception</span></div>
      <div><strong>On site</strong><span>bedrooms for residential events</span></div>
      <div><strong>Free</strong><span>parking and Wi-Fi for every delegate</span></div>
    </div>
  </div>
</section>

<section class="section section--white" id="packages">
  <div class="wrap">
    <div class="intro mb-3">
      <div class="t"><h2>Meeting packages</h2></div>
      <div class="c"><p>Simple per-person packages that cover the essentials, so you can focus on the agenda. Rates include VAT.</p></div>
    </div>
    <div class="rates">
      <div class="rate">
        <h3>Day Delegate</h3>
        <div class="price">£35</div><div class="per">per person, midweek. From £30 at weekends</div>
        <ul><li>Meeting room hire</li><li>Refreshments mid-morning and mid-afternoon</li><li>Hot and cold lunch options</li></ul>
      </div>
      <div class="rate">
        <h3>24-Hour</h3>
        <div class="price">£155</div><div class="per">per person, midweek and weekends</div>
        <ul><li>Everything in the Day Delegate package</li><li>One night's accommodation</li><li>Breakfast the next morning</li></ul>
      </div>
      <div class="rate">
        <h3>Room hire</h3>
        <div class="price" style="font-size:2rem;padding-top:.6rem">Tailored</div><div class="per">quoted for your event</div>
        <ul><li>Your room, set to your layout</li><li>Choose catering à la carte</li><li>Add bedrooms, dinner and extras</li></ul>
      </div>
    </div>
    <div class="split mt-3" style="align-items:start">
      <div class="a">
        <h3>Every package includes</h3>
        <ul class="ticks">
          <li>Meeting room hire</li>
          <li>Unlimited tea, coffee and water</li>
          <li>Two servings of sweet and savoury refreshments</li>
          <li>Hot and cold lunch options</li>
          <li>A screen and HDMI cable</li>
          <li>A flipchart with pads and pens</li>
          <li>Complimentary Wi-Fi</li>
          <li>Complimentary car parking</li>
        </ul>
      </div>
      <div class="b">
        {dl(p, "meetings-and-events.pdf", "Meetings at " + HOTEL, "Brochure and package rates, PDF, 0.7 MB")}
        <p class="small mt-1">Prices are a guide. Your quote is confirmed by our events team.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="intro mb-3">
      <div class="t"><h2>Our main event spaces</h2></div>
      <div class="c"><p>Three suites that open up or divide to suit your numbers, plus quieter rooms for smaller meetings. Every plan below is drawn to the room's measurements.</p><p><a class="textlink" href="spaces/">Compare all 14 rooms</a></p></div>
    </div>
    <div class="rooms" id="suite-cards"></div>
  </div>
</section>

<section class="section section--navy">
  <div class="wrap split">
    <div class="a">
      <span class="kicker">Event planner</span>
      <h2>Plan your event in a few minutes</h2>
      <p>Tell us your numbers and see which rooms fit, how each layout looks, and what your package would cost. Add catering, extras and bedrooms for your group, then send it all to our events team in one go.</p>
      <div class="btn-row"><a class="btn btn--book" href="planner/">Start planning</a></div>
    </div>
    <div class="b">
      <ol class="plan-steps" style="list-style:none;padding:0;margin:0">
        <li style="padding:14px 0;border-top:1px solid rgba(255,255,255,.18)"><span style="font-size:1.3rem;color:var(--gold);margin-right:14px">1</span>Your event, date and numbers</li>
        <li style="padding:14px 0;border-top:1px solid rgba(255,255,255,.18)"><span style="font-size:1.3rem;color:var(--gold);margin-right:14px">2</span>Choose a layout and room, drawn to scale</li>
        <li style="padding:14px 0;border-top:1px solid rgba(255,255,255,.18)"><span style="font-size:1.3rem;color:var(--gold);margin-right:14px">3</span>Pick a package, catering and extras</li>
        <li style="padding:14px 0;border-top:1px solid rgba(255,255,255,.18)"><span style="font-size:1.3rem;color:var(--gold);margin-right:14px">4</span>Add bedrooms for your group</li>
        <li style="padding:14px 0;border-top:1px solid rgba(255,255,255,.18);border-bottom:1px solid rgba(255,255,255,.18)"><span style="font-size:1.3rem;color:var(--gold);margin-right:14px">5</span>Request your quote</li>
      </ol>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--flip">
    <div class="a"><figure class="mount"><img src="../assets/img/bar-lounge.jpg" alt="The hotel bar with armchairs, a clock above the back bar and framed prints" loading="lazy"></figure></div>
    <div class="b">
      <h2>Technology that just works</h2>
      <p>Every room has a screen, HDMI connection, flipchart and fast, complimentary Wi-Fi.</p>
      <p>The Brandon and Wolston suites go further, with 4K smart screens up to 98 inches, ClickShare wireless screen sharing, HDMI and USB-C connections and set-ups ready for Teams and Zoom. The Woodlands Suite has a PA system and microphones for larger audiences.</p>
      <p><a class="textlink" href="spaces/">See what's in each room</a></p>
    </div>
  </div>
</section>

<section class="section section--beige">
  <div class="wrap split">
    <div class="a">
      <h2>Bringing a team to stay?</h2>
      <p>Residential conferences, retreats and training programmes run smoothly when everyone's under one roof. We'll hold a block of bedrooms for your group, on bed and breakfast or dinner, bed and breakfast, with private dining for the evenings.</p>
      <p>Add bedrooms in the event planner and we'll include them in your proposal.</p>
      <div class="btn-row"><a class="btn btn--navy" href="planner/#step-6">Add bedrooms to your event</a></div>
    </div>
    <div class="b"><figure class="mount"><img src="../assets/img/bedroom-teal.jpg" alt="A double bedroom with a teal feature wall and a desk by the window" loading="lazy"></figure></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="intro mb-2">
      <div class="t"><h2>Set for the occasion</h2></div>
      <div class="c"><p>Conferences, training days, dinners and celebrations in our event spaces.</p></div>
    </div>
    <div class="photo-grid" data-meeting-photos data-root="../"></div>
  </div>
</section>

<section class="section--tight section--white">
  <div class="wrap cta-band" style="padding-top:56px;padding-bottom:56px">
    <div>
      <h2>Talk to our events team</h2>
      <p>We'll check availability and tailor a package around you. Call <a class="textlink" href="tel:{PHONE_HREF}">{PHONE}</a> or email <a class="textlink" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
    <a class="btn btn--book" href="planner/">Request a quote</a>
  </div>
</section>
'''
    script = '''<script>
(function(){
  var ids=["woodlands","brandon-suite","wolston-suite"], el=document.getElementById("suite-cards");
  el.innerHTML = ids.map(function(id){
    var r=BH_ROOMS.find(function(x){return x.id===id});
    var lay = r.cap.cabaret ? "cabaret" : "theatre";
    return '<article class="room-card"><div class="plan">'+bhPlan(r,lay,r.cap[lay],{compact:true})+'</div><div class="body">'+
      '<h3>'+r.name+'</h3><div class="meta">'+r.m2+' m², shown with '+r.cap[lay]+' guests in '+lay+'</div>'+
      '<dl>'+BH_LAYOUTS.map(function(l){var v=r.cap[l.id];return '<div><dt>'+l.label+'</dt><dd class="'+(v?'':'na')+'">'+(v||'–')+'</dd></div>'}).join('')+'</dl>'+
      '<p class="small">'+r.summary+'</p>'+
      '<div class="actions"><a class="btn btn--line" href="spaces/?room='+r.id+'">Room details</a><a class="btn btn--navy" href="planner/?room='+r.id+'&layout='+lay+'">Plan in this room</a></div></div></article>';
  }).join("");
})();
</script>
'''
    write("meetings-events/index.html", h + header(p, "meetings") + body + footer(p, ["venue-data.js", "floorplan.js"]).replace("</body>", script + "</body>"))


# ----------------------------------------------------------------
# SPACES (venue finder)
# ----------------------------------------------------------------
def spaces():
    p = "../../"
    h = head(p, f"Our event spaces and capacities | {HOTEL}",
             "Compare our 14 meeting and event rooms: sizes, capacities for every layout, floor plans and the technology in each room.")
    body = f'''
<section class="section" style="padding-bottom:40px">
  <div class="wrap intro">
    <div class="t">
      <span class="kicker"><a href="../" style="text-decoration:none">Meetings and events</a></span>
      <h1 style="font-size:clamp(2.6rem,5.6vw,4.4rem)">Our event spaces</h1>
    </div>
    <div class="c">
      <p class="lede">Fourteen rooms, from an intimate boardroom for ten to the Woodlands Suite for 280.</p>
      <p>Enter your numbers and choose a layout to see which rooms fit. Select any room for its floor plan, measurements and the technology in the room.</p>
    </div>
  </div>
</section>

<section style="padding-bottom:var(--section)">
  <div class="wrap">
    <div class="finder" role="search" aria-label="Find a room">
      <label class="field" for="f-guests">How many guests?
        <input id="f-guests" type="number" min="1" max="300" inputmode="numeric" placeholder="e.g. 40" style="width:150px">
      </label>
      <div class="field"><span>Layout</span><div class="layout-pick" id="f-layout" role="group" aria-label="Layout"></div></div>
    </div>
    <p class="accent" id="f-count" aria-live="polite"></p>
    <div class="rooms mt-1" id="room-cards"></div>

    <h2 class="mt-3" style="padding-top:40px">Our spaces in use</h2>
    <div class="photo-grid mt-1" data-meeting-photos data-root="../../"></div>

    <h2 class="mt-3" style="padding-top:40px">Capacity chart</h2>
    <p>Maximum guests per layout. Select a room to see its plan.</p>
    <div class="table-scroll mt-1"><table class="cap" id="cap-table"></table></div>
    <p class="small mt-1">Capacities are the most each room holds comfortably. Some rooms combine: the Woodlands Suite is Woodlands 1 and 2, and the Brandon Suite is Brandon 1 and 2.</p>
    <div class="mt-3" style="max-width:560px">
      {dl(p, "meetings-and-events.pdf", "Meetings at " + HOTEL, "Brochure and package rates, PDF, 0.7 MB")}
    </div>
  </div>
</section>
<dialog class="room-dialog" id="room-dialog" aria-label="Room details"></dialog>
'''
    write("meetings-events/spaces/index.html", h + header(p, "meetings") + body + footer(p, ["venue-data.js", "floorplan.js", "venue.js"]))


# ----------------------------------------------------------------
# PLANNER
# ----------------------------------------------------------------
def planner():
    p = "../../"
    h = head(p, f"Event planner and quote request | {HOTEL}",
             "Plan your meeting, conference or celebration: choose a room and layout drawn to scale, add catering, extras and bedrooms, and request a quote.")
    body = f'''
<section class="section page-top" style="padding-bottom:36px">
  <div class="wrap intro">
    <div class="t">
      <span class="kicker"><a href="../" style="text-decoration:none">Meetings and events</a></span>
      <h1 style="font-size:clamp(2.6rem,5.6vw,4.4rem)">Plan your event</h1>
    </div>
    <div class="c">
      <p class="lede">Build your event step by step. The plan and summary update as you go.</p>
      <p>Choose your room, layout, package, food and drink, extras and bedrooms. When you're happy, send it to our events team and they'll come back with availability and a tailored proposal. There's no commitment at this stage.</p>
    </div>
  </div>
</section>

<section class="gate-wrap" id="gate" hidden>
  <div class="wrap">
    <div class="gate">
      <div class="gate-inner">
        <span class="kicker">Before you start</span>
        <h2>Tell us who's planning</h2>
        <p>We'll use these details to send your proposal, and our events team can help if you get stuck. You can come back to your plan at any time on this device.</p>
        <form id="gate-form" novalidate>
          <div class="grid-2">
            <label class="field" for="g-name">Name<input id="g-name" type="text" autocomplete="name" required><span class="err" id="g-name-err"></span></label>
            <label class="field" for="g-company">Company or organisation<input id="g-company" type="text" autocomplete="organization" placeholder="If booking for a business"><span class="err"></span></label>
            <label class="field" for="g-email">Email<input id="g-email" type="email" autocomplete="email" required><span class="err" id="g-email-err"></span></label>
            <label class="field" for="g-phone">Phone number<input id="g-phone" type="tel" autocomplete="tel" required><span class="err" id="g-phone-err"></span></label>
          </div>
          <label class="check mt-1" style="border:0"><input type="checkbox" id="g-consent"><span>I'm happy for {HOTEL} to contact me about my event. See our <a href="../../privacy/">privacy notice</a>.</span></label>
          <p class="err" id="g-consent-err"></p>
          <div class="visually-hidden" aria-hidden="true"><label for="g-website">Leave this empty</label><input id="g-website" type="text" tabindex="-1" autocomplete="off"></div>
          <div class="btn-row"><button class="btn btn--book" type="submit">Start planning</button></div>
        </form>
        <p class="small mt-2">Prefer to talk? Call <a class="textlink" href="tel:{PHONE_HREF}">{PHONE}</a> or email <a class="textlink" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      </div>
    </div>
  </div>
</section>

<section style="padding-bottom:var(--section)" id="planner-wrap" hidden>
  <div class="wrap">
    <p class="who-bar">Planning as <strong id="who"></strong>. <a href="#" id="not-you">Not you?</a></p>
  </div>
  <div class="wrap planner">
    <form id="p-form" novalidate>
      <fieldset class="step" id="step-1">
        <legend><span class="step-n">1</span><span class="step-t">Your event</span></legend>
        <div class="chips" id="p-type" role="group" aria-label="Type of event"></div>
        <div class="grid-3">
          <label class="field" for="p-date">Date<input id="p-date" type="date"></label>
          <label class="field" for="p-days">Days<select id="p-days"><option value="1">1 day</option><option value="2">2 days</option><option value="3">3 days</option><option value="4">4 days</option><option value="5">5 days</option></select></label>
          <label class="field" for="p-guests">Guests<input id="p-guests" type="number" min="1" max="300" inputmode="numeric"></label>
        </div>
      </fieldset>

      <fieldset class="step" id="step-2">
        <legend><span class="step-n">2</span><span class="step-t">Layout and room</span></legend>
        <div class="layout-pick" id="p-layout" role="group" aria-label="Layout"></div>
        <p class="small" id="p-layout-desc"></p>
        <div class="opts" id="p-rooms" role="radiogroup" aria-label="Room"></div>
      </fieldset>

      <fieldset class="step" id="step-3">
        <legend><span class="step-n">3</span><span class="step-t">Package</span></legend>
        <div class="opts" id="p-pkg" role="radiogroup" aria-label="Package"></div>
        <p class="small" id="p-pkg-note"></p>
      </fieldset>

      <fieldset class="step" id="step-4">
        <legend><span class="step-n">4</span><span class="step-t">Food and drink</span></legend>
        <p class="small mt-0" id="p-cat-note"></p>
        <div class="checks mt-1" id="p-cat"></div>
      </fieldset>

      <fieldset class="step" id="step-5">
        <legend><span class="step-n">5</span><span class="step-t">Extras and technology</span></legend>
        <div class="checks" id="p-extras"></div>
        <label class="field mt-1" id="p-breakout-wrap" for="p-breakout" hidden>Breakout room<select id="p-breakout"></select></label>
      </fieldset>

      <fieldset class="step" id="step-6">
        <legend><span class="step-n">6</span><span class="step-t">Bedrooms for your group</span></legend>
        <p class="notice mt-0" id="p-stay-24" hidden>The 24-hour package already includes one night's accommodation and breakfast for each delegate. Add more bedrooms or nights below if you need them.</p>
        <label class="toggle mt-1"><input type="checkbox" id="p-stay"> Hold a block of bedrooms for my group</label>
        <div id="p-stay-fields" hidden>
          <div class="grid-3">
            <label class="field" for="p-arrival">Arrival<input id="p-arrival" type="date"></label>
            <label class="field" for="p-nights">Nights<input id="p-nights" type="number" min="1" max="14" value="1" inputmode="numeric"></label>
            <label class="field" for="p-bedrooms">Bedrooms<input id="p-bedrooms" type="number" min="1" max="120" value="10" inputmode="numeric"></label>
          </div>
          <p class="small mt-1" style="margin-bottom:8px">Room mix</p>
          <div class="grid-4">
            <label class="field" for="p-singles">Single use<input id="p-singles" type="number" min="0" max="120" value="10" inputmode="numeric"></label>
            <label class="field" for="p-doubles">Double<input id="p-doubles" type="number" min="0" max="120" value="0" inputmode="numeric"></label>
            <label class="field" for="p-twins">Twin<input id="p-twins" type="number" min="0" max="120" value="0" inputmode="numeric"></label>
            <label class="field" for="p-board">Board<select id="p-board"><option value="bb">Bed and breakfast</option><option value="dbb">Dinner, bed and breakfast</option></select></label>
          </div>
          <p class="err mt-1" id="p-mix-note" aria-live="polite"></p>
        </div>
      </fieldset>

      <fieldset class="step" id="step-7">
        <legend><span class="step-n">7</span><span class="step-t">Check and send</span></legend>
        <div class="grid-2">
          <label class="field" for="p-name">Name<input id="p-name" type="text" autocomplete="name" required><span class="err" id="p-name-err"></span></label>
          <label class="field" for="p-company">Company or organisation <span class="hint">Optional</span><input id="p-company" type="text" autocomplete="organization"></label>
          <label class="field" for="p-email">Email<input id="p-email" type="email" autocomplete="email" required><span class="err" id="p-email-err"></span></label>
          <label class="field" for="p-phone">Phone number<input id="p-phone" type="tel" autocomplete="tel"></label>
        </div>
        <label class="field mt-1" for="p-notes">Anything else we should know? <span class="hint">Timings, dietary needs, accessibility, budget</span><textarea id="p-notes" rows="4"></textarea></label>
        <label class="field mt-1" for="p-source">How did you hear about us? <span class="hint">Optional</span><select id="p-source"><option value="">Choose one</option><option>Search engine</option><option>Recommendation</option><option>Been before</option><option>Social media</option><option>Event agency</option><option>Other</option></select></label>
        <div class="visually-hidden" aria-hidden="true"><label for="p-website">Leave this empty</label><input id="p-website" type="text" tabindex="-1" autocomplete="off"></div>
        <div class="btn-row"><button class="btn btn--book" type="submit" id="p-submit">Request my quote</button></div>
        <p class="err" id="p-send-err" aria-live="polite"></p>
      </fieldset>

      <div class="done" id="p-done" hidden tabindex="-1" aria-live="polite">
        <h3 id="p-done-title"></h3>
        <p id="p-done-text"></p>
        <pre id="p-done-copy"></pre>
        <div class="btn-row"><button type="button" class="btn btn--light" id="p-copy">Copy details</button><button type="button" class="btn btn--light" id="p-print">Print summary</button></div>
      </div>
    </form>

    <aside class="summary" aria-label="Your event summary">
      <div class="sheet"><div class="inner">
        <span class="kicker">Your event</span>
        <div class="plan-box" id="s-plan"></div>
        <p class="small mt-1" id="s-caption"></p>
        <dl id="s-list"></dl>
        <div class="est" id="s-estimate" hidden>
          <strong>Package estimate</strong><span class="v" id="s-est-total"></span>
          <p id="s-est-line"></p>
        </div>
        <div class="est" id="s-carbon" hidden>
          <strong>Estimated footprint</strong><span class="v co2" id="s-co2"></span>
          <p id="s-co2-line"></p>
          <p>An indicative estimate from room energy, catering and bedrooms, using UK hospitality benchmarks.</p>
        </div>
      </div></div>
      <p class="small mt-1">Plans are drawn to the room's measurements. Our events team confirms the final layout, availability and price.</p>
    </aside>
  </div>
</section>
'''
    write("meetings-events/planner/index.html", h + header(p, "meetings") + body + footer(p, ["venue-data.js", "floorplan.js", "planner.js"]))


# ----------------------------------------------------------------
# HOLDING PAGES (built in the next stage)
# ----------------------------------------------------------------
def holding(path, active, title, lede, img, alt, downloads=(), extra=""):
    depth = path.count("/") + 1
    p = "../" * depth
    h = head(p, f"{title} | {HOTEL}", lede)
    dls = "".join(dl(p, *d) for d in downloads)
    body = f'''
<section class="hero hero--page">
  <img src="{p}assets/img/{img}" alt="{alt}" fetchpriority="high">
  <div class="wrap"><h1>{title}</h1><p>{lede}</p></div>
</section>
<section class="section holding">
  <div class="wrap split" style="align-items:start">
    <div class="a">
      <p class="notice" style="margin-top:0">We're putting the finishing touches to this page. In the meantime, the downloads here have everything you need.</p>
      {extra}
      <p class="mt-2">For anything you need in the meantime, call <a class="textlink" href="tel:{PHONE_HREF}">{PHONE}</a> or email <a class="textlink" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
    <div class="b">{("<h3>Downloads</h3>" + dls) if dls else ""}</div>
  </div>
</section>
'''
    write(path + "/index.html", h + header(p, active) + body + footer(p))



# ----------------------------------------------------------------
# ROOMS & SUITES
# ----------------------------------------------------------------
def rooms():
    p = "../"
    h = head(p, f"Rooms and suites | {HOTEL}",
             "Classic, Executive and Junior Suite rooms in a country house hotel near Coventry, with free Wi-Fi, ensuite bathrooms and accessible rooms.")
    def room(title, kicker, img, alt, intro, items, flip=False, note=""):
        lis = "".join(f"<li>{i}</li>" for i in items)
        return f'''
<section class="section{' section--white' if flip else ''}">
  <div class="wrap split{' split--flip' if flip else ''}">
    <div class="a"><figure class="mount"><img src="../assets/img/{img}" alt="{alt}" loading="lazy"></figure></div>
    <div class="b">
      <span class="kicker">{kicker}</span>
      <h2>{title}</h2>
      <p>{intro}</p>
      <ul class="ticks ticks--one mt-1">{lis}</ul>
      {f'<p class="small mt-1">{note}</p>' if note else ''}
      <div class="btn-row"><a class="btn btn--book" href="{BOOK}" target="_blank" rel="noopener">Check availability</a></div>
    </div>
  </div>
</section>'''
    body = f'''
<section class="section page-open">
  <div class="wrap split">
    <div class="a">
      <h1 class="h1-page">Rooms and suites</h1>
      <p class="lede">Rest easy in country comfort.</p>
      <p>Each room at {HOTEL} is designed with comfort in mind: a quiet space to unwind after a busy day, with soft bedding, modern touches and views that remind you you're in the heart of the countryside.</p>
      <div class="btn-row">
        <a class="btn btn--book" href="{BOOK}" target="_blank" rel="noopener">Book direct</a>
        <a class="btn btn--line" href="../offers/">See our offers</a>
      </div>
    </div>
    <div class="b"><figure class="mount mount--tall"><img src="../assets/img/exterior-terrace.jpg" alt="The hotel's white bay-fronted wing with garden seating on the terrace" fetchpriority="high"></figure></div>
  </div>
</section>
{room("Classic Double and Twin", "Classic rooms", "bedroom-yellow.jpg", "A classic double bedroom", "Cosy and comfortable, with a double bed or two single beds.", ["Cosy, comfortable furnishings", "A double bed, or two twin beds", "Ensuite bathroom with bath or shower", "Accessible Classic rooms available"], True)}
{room("Executive Double", "Executive rooms", "bedroom-teal.jpg", "A double bedroom with a teal feature wall and a desk by the window", "Upgraded furnishings and a proper desk, ideal if you're staying for work.", ["Upgraded furnishings", "Double bed", "Desk and chair", "Ensuite bathroom with bath or shower", "Accessible Executive rooms available"])}
{room("Junior Suites", "Suites", "suite-bay.jpg", "A junior suite with a large bed and a bay window", "More space to spread out, with a sofa to relax on at the end of the day.", ["King-size bed", "More generous space and upgraded furnishings", "Seating area with sofa", "Ensuite bathroom with bath or shower"], True)}

<section class="section">
  <div class="wrap">
    <div class="intro mb-2">
      <div class="t"><h2>In every room</h2></div>
      <div class="c"><ul class="ticks"><li>TV</li><li>Free Wi-Fi</li><li>Tea and coffee making</li><li>Ironing set</li><li>Toiletries and hairdryer</li><li>Ensuite bathroom</li></ul></div>
    </div>
    <div class="intro mt-3">
      <div class="t"><h2>Around the hotel</h2></div>
      <div class="c">
        <p>From breakfast to a nightcap in the bar, everything is designed to make your stay easy, whether you're here to unwind, work or explore.</p>
        <ul class="ticks"><li>24-hour reception</li><li>Breakfast available</li><li>Bar and lounge</li><li>Laundry service</li><li>Accessible rooms</li><li>Pet-friendly rooms on request</li><li>Indoor pool, gym and fitness centre</li><li>17 acres of gardens and woodland</li></ul>
      </div>
    </div>
  </div>
</section>

<section class="section--tight section--navy">
  <div class="wrap cta-band" style="padding-top:56px;padding-bottom:56px">
    <div><h2>Book direct for the best rate</h2><p>Stay longer and save with our current offers.</p></div>
    <div class="btn-row" style="margin-top:0"><a class="btn btn--book" href="{BOOK}" target="_blank" rel="noopener">Book direct</a><a class="btn btn--light" href="../offers/">Offers</a></div>
  </div>
</section>
'''
    write("rooms-suites/index.html", h + header(p, "stay") + body + footer(p))


# ----------------------------------------------------------------
# LEISURE & WELLNESS
# ----------------------------------------------------------------
def leisure():
    p = "../"
    h = head(p, f"Leisure and wellness | {HOTEL}",
             "Indoor swimming pool, gym and fitness centre at Brandon Hall Hotel and Spa, near Coventry in Warwickshire.")
    body = f'''
<section class="hero hero--page">
  <img src="../assets/img/pool.jpg" alt="The indoor swimming pool under a glazed roof" fetchpriority="high">
  <div class="wrap"><h1>Leisure and wellness</h1><p>Swim, train or simply slow down, a few steps from your room.</p></div>
</section>

<section class="section">
  <div class="wrap intro">
    <div class="t"><h2>Time for yourself</h2></div>
    <div class="c">
      <p class="lede">Our leisure club gives you space to switch off, or to keep up your routine while you're away.</p>
      <p>Start the day with a swim under the glass roof, fit in a session in the gym between meetings, or unwind at the end of a day exploring Warwickshire. Our reception team can tell you everything you need to know before your visit.</p>
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="features">
      <article class="feature">
        <figure class="mount">{rimg(p, "leisure-pool.jpg", "2026/09/17685405-1000x665.jpg", "The swimming pool")}</figure>
        <h3>Swimming pool</h3>
        <p>An indoor pool beneath a glazed roof, bright in every season.</p>
      </article>
      <article class="feature">
        <figure class="mount">{rimg(p, "leisure-gym.jpg", "2026/09/96137361-1000x667.jpg", "The gym")}</figure>
        <h3>Gym</h3>
        <p>Cardio and resistance equipment to keep your routine going while you stay.</p>
      </article>
      <article class="feature">
        <figure class="mount">{rimg(p, "leisure-fitness.jpg", "2026/09/218517847-1000x750.jpg", "The fitness centre")}</figure>
        <h3>Fitness centre</h3>
        <p>Space to stretch, train and reset, whatever your pace.</p>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="a"><figure class="mount"><img src="../assets/img/grounds-lawn.jpg" alt="Wide striped lawns and mature trees in the hotel grounds" loading="lazy"></figure></div>
    <div class="b">
      <span class="kicker">In the grounds</span>
      <h2>Seventeen acres to explore</h2>
      <p>Beyond the leisure club, our gardens and woodland are made for a morning walk, a run before breakfast or a quiet moment with a book.</p>
      <div class="btn-row"><a class="btn btn--line" href="../out-about/">Out and about</a></div>
    </div>
  </div>
</section>

<section class="section--tight section--navy">
  <div class="wrap cta-band" style="padding-top:56px;padding-bottom:56px">
    <div><h2>Plan your stay</h2><p>For opening times and anything else about the leisure club, call reception on <a href="tel:{PHONE_HREF}" style="color:#fff">{PHONE}</a>.</p></div>
    <a class="btn btn--book" href="{BOOK}" target="_blank" rel="noopener">Book direct</a>
  </div>
</section>
'''
    write("spa-leisure/index.html", h + header(p, "spa") + body + footer(p))


# ----------------------------------------------------------------
# OUT & ABOUT
# ----------------------------------------------------------------
def out_about():
    p = "../"
    h = head(p, f"Things to do in Warwickshire | {HOTEL}",
             "Warwick Castle, Stratford-upon-Avon, Kenilworth Castle, Compton Verney and the Warwickshire countryside, all within easy reach of Brandon Hall Hotel and Spa.")
    places = [
        ("Warwick Castle", "Step into centuries of history and explore its towers, gardens and exhibitions.", "out-warwick-castle.webp", "2025/11/wars-of-the-roses-jousting.webp", "Knights jousting on horseback in front of a crowd at Warwick Castle", "https://www.warwick-castle.com"),
        ("Stratford-upon-Avon", "Discover Shakespeare's home town, with its theatres, river walks and charming streets.", "out-stratford.jpg", "2025/11/iStock-148521984-1000x669.jpg", "A thatched Tudor cottage in Stratford-upon-Avon", ""),
        ("Kenilworth Castle and Gardens", "Grand, romantic and full of stories.", "out-kenilworth.jpg", "2025/11/kenilworhero-1000x521.jpg", "The Elizabethan garden at Kenilworth Castle", "https://www.english-heritage.org.uk/visit/places/kenilworth-castle/"),
        ("Compton Verney Art Gallery and Park", "Art, nature and architecture in perfect balance.", "out-compton-verney.jpg", "2025/11/iStock-184639439-1000x756.jpg", "Compton Verney house across the lake", "https://www.comptonverney.org.uk"),
        ("The Warwickshire countryside", "Wander scenic walking routes, cycle through villages or simply enjoy the open air.", "out-countryside.jpg", "2025/11/iStock-1456041071-1000x750.jpg", "Green Warwickshire countryside and a river from above", ""),
    ]
    cards = "".join(
        f'''<article class="place">
          <figure class="place-img">{rimg(p, local, remote, alt)}</figure>
          <div class="place-t"><h3>{name}</h3><p>{text}</p>{f'<a class="textlink" href="{url}" target="_blank" rel="noopener">Find out more</a>' if url else ''}</div>
        </article>''' for name, text, local, remote, alt, url in places)
    body = f'''
<section class="section page-open">
  <div class="wrap split">
    <div class="a">
      <h1 class="h1-page">Out and about</h1>
      <p class="lede">Things to do in Warwickshire.</p>
      <p>When you stay at {HOTEL}, you're perfectly placed to explore some of Warwickshire's best-loved places, from historic towns to hidden countryside trails.</p>
    </div>
    <div class="b"><figure class="mount mount--tall"><img src="../assets/img/grounds-lake.jpg" alt="A still lake framed by pine trees" fetchpriority="high"></figure></div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <h2 class="mb-2">Explore, discover and enjoy</h2>
    <div class="places">{cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--flip">
    <div class="a"><figure class="mount"><img src="../assets/img/reception.jpg" alt="The hotel reception desk with fresh flowers" loading="lazy"></figure></div>
    <div class="b">
      <h2>Tap into our local knowledge</h2>
      <p>Our team is always happy to recommend places to visit, local restaurants and hidden gems to make your stay extra special. Just ask at reception, day or night.</p>
      <div class="btn-row"><a class="btn btn--book" href="{BOOK}" target="_blank" rel="noopener">Book your stay</a><a class="btn btn--line" href="{MAPS}" target="_blank" rel="noopener">Find us</a></div>
    </div>
  </div>
</section>
'''
    write("out-about/index.html", h + header(p, "") + body + footer(p))


def seo_files():
    pages = ["", "rooms-suites/", "dining/", "spa-leisure/", "out-about/", "weddings/", "meetings-events/", "meetings-events/spaces/", "meetings-events/planner/", "christmas/", "offers/", "contact/", "privacy/", "accessibility/"]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE_URL}/{u}</loc></url>\n" for u in pages) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(xml)
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")


# ----------------------------------------------------------------
# CHRISTMAS & NEW YEAR (content from the 2026 brochure and posters)
# ----------------------------------------------------------------
XMAS_ENQ = "mailto:" + EMAIL + "?subject=" + "Christmas%20and%20New%20Year%20enquiry"

def christmas():
    p = "../"
    h = head(p, f"Christmas and New Year 2026 | {HOTEL}",
             "Christmas party nights from £45, joiner nights, festive dining, afternoon tea, Christmas Day lunch and a New Year's Eve masquerade gala near Coventry.")
    def block(anchor, kicker, title, img, alt, paras, price_lines, flip=False, white=False, extra=""):
        ps = "".join(f"<p>{x}</p>" for x in paras)
        pr = "".join(f"<li><span>{a}</span><strong>{b_}</strong></li>" for a, b_ in price_lines)
        return f"""
<section class="section{' section--white' if white else ''}" id="{anchor}">
  <div class="wrap split{' split--flip' if flip else ''}">
    <div class="a"><figure class="mount mount--tall"><img src="../assets/img/{img}" alt="{alt}" loading="lazy"></figure></div>
    <div class="b">
      <span class="kicker">{kicker}</span>
      <h2>{title}</h2>
      {ps}
      <ul class="pricelist">{pr}</ul>
      {extra}
      <div class="btn-row"><a class="btn btn--book" href="{XMAS_ENQ}%3A%20{title.replace(' ', '%20').replace("'", '%27')}">Enquire now</a><a class="btn btn--line" href="tel:{PHONE_HREF}">Call {PHONE}</a></div>
    </div>
  </div>
</section>"""
    glance = [
        ("#party-nights", "Christmas Party Nights", "Private parties", "From £45"),
        ("#joiner-nights", "Joiner Party Nights", "4 and 18 December", "From £55"),
        ("#festive-dining", "Festive Dining", "Throughout December", "From £40"),
        ("#afternoon-tea", "Festive Afternoon Tea", "A seasonal treat", "From £40"),
        ("#christmas-day", "Christmas Day", "Friday 25 December", "£80"),
        ("#new-years-eve", "New Year's Eve", "Thursday 31 December", "From £85"),
    ]
    cards = "".join(f'<a class="glance" href="{h_}"><span class="g-date">{d}</span><strong>{t}</strong><span class="g-price">{pz} <small>per person</small></span></a>' for h_, t, d, pz in glance)
    body = f"""
<section class="hero hero--page">
  <img src="../assets/img/xmas-hero.jpg" alt="Glasses of champagne raised at a festive celebration" fetchpriority="high">
  <div class="wrap">
    <span class="kicker" style="color:var(--gold)">Christmas and New Year 2026</span>
    <h1>Christmas magic at the Hall</h1>
    <p>Party nights, festive dining, Christmas Day and a New Year's Eve masquerade in 17 acres of Warwickshire grounds.</p>
    <div class="btn-row"><a class="btn btn--book" href="#at-a-glance">See what's on</a><a class="btn btn--light" href="../downloads/christmas-brochure-2026.pdf" download>Download the brochure</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap intro">
    <div class="t"><h2>Celebrate the magic of the festive season</h2></div>
    <div class="c">
      <p class="lede">Timeless charm, warm hospitality and sparkling celebrations come together for an unforgettable Christmas at {HOTEL}.</p>
      <p>Set in 17 acres of Warwickshire grounds, the hotel becomes a winter wonderland throughout the festive season: the perfect setting to relax, celebrate and make cherished memories with family, friends and colleagues.</p>
      <p>Whether you're joining us for a joyful gathering, a festive afternoon tea or a peaceful winter escape, our dedicated team will take care of every detail.</p>
    </div>
  </div>
</section>

<section class="section section--navy pattern-section" id="at-a-glance">
  <div class="wrap">
    <h2 class="mb-2">At a glance</h2>
    <div class="glances">{cards}</div>
  </div>
</section>
{block("party-nights", "Private parties", "Christmas Party Nights", "xmas-party.jpg", "Friends dancing under festive lights",
  ["Gather your colleagues, friends or family for an evening of festive cheer, delicious dining and dancing in our beautifully decorated surroundings.",
   "Begin with a welcome drink before sitting down to a sumptuous three-course festive dinner prepared by our chefs. As the evening goes on, our resident DJ keeps the dance floor full with party classics and Christmas hits until late.",
   "Whether it's the office celebration or a festive night out with friends, we'll take care of every detail."],
  [("Welcome drink, three-course dinner, resident DJ and disco", "From £45 per person")], white=True,
  extra='<p class="small mt-1">Planning a party for your team? <a class="textlink" href="../meetings-events/planner/?type=christmas&amp;layout=cabaret">Use our event planner</a>.</p>')}
{block("joiner-nights", "Shared party nights", "Christmas Joiner Party Nights", "christmas-party.jpg", "Friends celebrating with sparklers",
  ["Perfect for smaller groups, friends, colleagues and couples. Enjoy a delicious festive meal, soak up the atmosphere and dance the night away with live entertainment and a fantastic party soundtrack.",
   "With sparkling decorations, great company and plenty of Christmas cheer, it's the perfect way to celebrate without organising a private event."],
  [("Friday 4 December 2026", ""), ("Friday 18 December 2026", ""), ("Festive meal and live entertainment", "From £55 per person")], flip=True)}
{block("festive-dining", "Our restaurant", "Festive Dining", "xmas-dining.jpg", "A festive main course with seasonal garnishes",
  ["Throughout the Christmas period, our restaurant is the perfect place to relax over seasonal dishes with family, friends or colleagues.",
   "Our chefs have created a festive menu of traditional Christmas favourites alongside contemporary dishes, from warming starters to indulgent desserts."],
  [("Festive lunch or evening meal", "From £40 per person")], white=True)}
{block("afternoon-tea", "A seasonal treat", "Festive Afternoon Tea", "xmas-tea.jpg", "Festive sandwiches, scones and cakes on a tiered stand",
  ["A much-loved seasonal tradition. Freshly prepared finger sandwiches, warm scones with clotted cream and preserves, and festive cakes and sweet treats, served with your choice of fine teas or freshly brewed coffee."],
  [("Festive Afternoon Tea", "From £40 per person"), ("Mulled Wine Afternoon Tea", "£45 per person")], flip=True)}
{block("christmas-day", "Friday 25 December 2026", "Christmas Day", "christmas-table.jpg", "A festive dinner table with candles and crackers",
  ["Celebrate Christmas Day with a traditional festive feast: a four-course Christmas menu, Buck's Fizz on arrival and Christmas novelties.",
   "Sit back and let our team take care of everything, so you can simply enjoy the day with the people who matter most."],
  [("Adults", "£80 per person"), ("Children aged 4 to 12", "£45 per person"), ("Children under 4", "Free")], white=True)}
{block("new-years-eve", "Thursday 31 December 2026", "New Year's Eve", "xmas-nye.jpg", "A guest celebrating at a party with lights behind",
  ["Welcome the New Year in style. Arrive and unwind, then celebrate at a spectacular masquerade gala evening with a sumptuous dinner, music, dancing and a midnight countdown.",
   "Stay the night and enjoy a leisurely brunch on New Year's Day before heading home. Masquerade theme, for guests aged 18 and over."],
  [("One-night package with dinner, entertainment, room and New Year's Day brunch", "£195 per person"), ("Single supplement", "£40"), ("Dinner and entertainment only", "£85 per person")], flip=True)}

<section class="section section--white">
  <div class="wrap split" style="align-items:start">
    <div class="a">
      <h2>Good to know</h2>
      <details class="terms">
        <summary>Key terms for Christmas Party Nights and Joiner Party Nights</summary>
        <ul class="ticks ticks--one">
          <li>A non-refundable deposit of £20 per person secures your party night.</li>
          <li>Full payment and final numbers are due four weeks before the event.</li>
          <li>Menu pre-orders and all dietary requirements are due two weeks before the event.</li>
          <li>Deposits and payments are non-refundable and non-transferable if you cancel or numbers go down.</li>
          <li>We may make minor changes to menus, entertainment or arrangements if necessary.</li>
          <li>Please drink responsibly. We may refuse service to intoxicated guests.</li>
          <li>Accommodation rates may be available for party guests, subject to availability.</li>
        </ul>
      </details>
      <p class="mt-2">To book or check availability, email <a class="textlink" href="mailto:{EMAIL}">{EMAIL}</a> or call <a class="textlink" href="tel:{PHONE_HREF}">{PHONE}</a>.</p>
    </div>
    <div class="b">
      <h3>Downloads</h3>
      {dl(p, "christmas-brochure-2026.pdf", "Christmas and New Year brochure 2026", "PDF, 9.6 MB")}
      {dl(p, "poster-christmas-new-year.pdf", "Christmas and New Year poster", "A4 PDF, 2.0 MB")}
      {dl(p, "poster-christmas-parties.pdf", "Christmas Parties poster", "A4 PDF, 1.6 MB")}
      {dl(p, "poster-festive-dining.pdf", "Festive Dining poster", "A4 PDF, 1.5 MB")}
      {dl(p, "poster-new-years-eve.pdf", "New Year's Eve poster", "A4 PDF, 1.6 MB")}
    </div>
  </div>
</section>
"""
    write("christmas/index.html", h + header(p, "christmas") + body + footer(p))


# ----------------------------------------------------------------
# OFFERS (content from the current website)
# ----------------------------------------------------------------
PR = "https://booking.profitroom.com/en/brandonhallhotelspawarwickshire/"
OFFERS = [
    ("suite-dreams", "Suite Dreams", "Two nights in a Junior Suite with dinner for two",
     "Treat yourself to an unforgettable stay. Book two nights in a Junior Suite and enjoy a complimentary dinner for two in our restaurant on one evening of your stay.",
     ["Two-night stay in a Junior Suite", "Complimentary dinner for two on one evening", "Extra space to relax in the countryside"],
     "Subject to availability. Dinner is included for two guests on one evening of the stay. Terms and conditions apply.",
     PR + "details/offer/1129398?no-cache=1&amp;currency=GBP", "suite-bay.jpg", "A junior suite with a large bed and a bay window"),
    ("stay-longer-5th-night", "Book 4 nights, get the 5th free", "An extra night on us",
     "Book a four-night stay and enjoy your fifth night completely free. More time for a relaxing retreat, a longer countryside break or a chance to explore more of Warwickshire.",
     ["Complimentary fifth night when you book four", "Comfortable country house accommodation", "More time to relax and explore"],
     "Subject to availability. Applies to consecutive-night stays. Terms and conditions apply.",
     PR + "pricelist/offers/?currency=GBP&amp;r1_adults=2&amp;codes=Stay_More", "grounds-lake.jpg", "A still lake framed by pine trees"),
    ("stay-3-save-20", "Stay 3 nights and save 20%", "20% off our Best Available Rate",
     "Book a minimum three-night stay and receive 20% off our Best Available Rate. Perfect for a countryside retreat, a romantic getaway or a longer break to discover Warwickshire.",
     ["20% off stays of three nights or more", "Charming country house accommodation", "Time to explore the surrounding countryside"],
     "Subject to availability. Applies to stays of three consecutive nights or more. Terms and conditions apply.",
     PR + "pricelist/offers/?currency=GBP&amp;r1_adults=2&amp;codes=Stay_More", "exterior-lawn.jpg", "The hotel across the lawn"),
    ("stay-2-save-15", "Stay 2 nights and save 15%", "15% off our Best Available Rate",
     "Book a minimum two-night stay and enjoy 15% off our Best Available Rate. Whether it's a countryside escape, a romantic break or a weekend exploring, stay a little longer and save.",
     ["15% off stays of two nights or more", "Charming country house accommodation", "The perfect base for exploring Warwickshire"],
     "Subject to availability. Applies to stays of two consecutive nights or more. Terms and conditions apply.",
     PR + "pricelist/offers/?currency=GBP&amp;r1_adults=2&amp;codes=Stay_More", "bedroom-yellow.jpg", "A bright double bedroom"),
]

def offers():
    p = "../"
    h = head(p, f"Offers | {HOTEL}",
             "Stay longer and save at Brandon Hall Hotel and Spa: Suite Dreams with dinner for two, your fifth night free, and up to 20% off when you book direct.")
    blocks = ""
    for i, (slug, title, kick, intro, items, terms, link, img, alt) in enumerate(OFFERS):
        lis = "".join(f"<li>{x}</li>" for x in items)
        flip = i % 2 == 1
        blocks += f"""
<section class="section{' section--white' if i % 2 == 0 else ''}" id="{slug}">
  <div class="wrap split{' split--flip' if flip else ''}">
    <div class="a"><figure class="mount"><img src="../assets/img/{img}" alt="{alt}" loading="lazy"></figure></div>
    <div class="b">
      <span class="kicker">{kick}</span>
      <h2>{title}</h2>
      <p>{intro}</p>
      <ul class="ticks ticks--one mt-1">{lis}</ul>
      <p class="small mt-1">{terms}</p>
      <div class="btn-row"><a class="btn btn--book" href="{link}" target="_blank" rel="noopener">Book this offer</a></div>
    </div>
  </div>
</section>"""
    body = f"""
<section class="section page-open">
  <div class="wrap intro">
    <div class="t"><h1 class="h1-page">Offers</h1></div>
    <div class="c">
      <p class="lede">Stay a little longer and save when you book direct with us.</p>
      <p>Our best rates are always here on our own website, with nothing added for booking through a third party.</p>
      <div class="btn-row">{''.join(f'<a class="btn btn--line" href="#{o[0]}">{o[1]}</a>' for o in OFFERS)}</div>
    </div>
  </div>
</section>
{blocks}
"""
    write("offers/index.html", h + header(p, "offers") + body + footer(p))


# ----------------------------------------------------------------
# WEDDINGS (content from the 2026 wedding and self-catering brochures)
# ----------------------------------------------------------------
WED_ENQ = "mailto:" + EMAIL + "?subject=Wedding%20enquiry%20and%20tour"

def weddings():
    p = "../"
    h = head(p, f"Weddings | {HOTEL}",
             "Country house weddings in 17 acres of Warwickshire gardens and woodland. Ceremonies, receptions for up to 280, wedding packages and self-catering weddings.")
    pk = [
        ("Classic", False,
         ["Private room hire from 7am to 11.59pm", "One arrival drink per guest*", "White linen tablecloths and napkins", "Three-course set wedding breakfast from the Classic menu"],
         [("High season, May to October", "£70", "£70", "£75"), ("Low season, November to April", "£60", "£60", "£65"), ("Evening guests buffet", "£25", "£25", "£30")]),
        ("Special", True,
         ["Private room hire from 7am to 11.59pm", "One arrival drink per guest*", "White linen tablecloths and napkins", "Three-course set wedding breakfast from the Classic menu", "Half a bottle of house wine per guest", "Tea, coffee and mints", "Evening buffet", "Overnight stay for the newlyweds in a standard room, with breakfast"],
         [("High season, May to October", "£115", "£115", "£120"), ("Low season, November to April", "£107", "£107", "£112"), ("Evening guests buffet", "£25", "£25", "£30")]),
        ("Extra Special", False,
         ["Private room hire from 7am to 11.59pm", "One arrival drink per guest*", "Three canapés per guest", "White linen tablecloths and napkins", "Five-course set wedding breakfast from the Extra Special menu", "Half a bottle of upgraded wine per guest", "A glass of Champagne per guest for the toast", "Tea, coffee and mints", "Evening buffet", "Overnight stay for the newlyweds in a honeymoon suite, with breakfast"],
         [("High season, May to October", "£159", "£159", "£168"), ("Low season, November to April", "£149", "£149", "£154"), ("Evening guests buffet", "£25", "£25", "£30")]),
    ]
    def pkg(name, popular, items, prices):
        lis = "".join(f"<li>{i}</li>" for i in items)
        rows = "".join(f"<tr><th scope='row'>{a}</th><td>{b_}</td><td>{c}</td><td>{d}</td></tr>" for a, b_, c, d in prices)
        return f"""<article class="wpkg{' wpkg--pop' if popular else ''}">
          {'<span class="wpkg-flag">Most popular</span>' if popular else ''}
          <h3>{name}</h3>
          <p class="wpkg-from">From <strong>{prices[1][1]}</strong> per guest</p>
          <ul class="ticks ticks--one">{lis}</ul>
          <table class="wprice"><caption class="visually-hidden">{name} prices per guest</caption>
            <thead><tr><th scope="col">Per guest</th><th scope="col">2026</th><th scope="col">2027</th><th scope="col">2028</th></tr></thead>
            <tbody>{rows}</tbody></table>
        </article>"""
    pkgs = "".join(pkg(*x) for x in pk)
    faq = [
        ("Final details", "We'd like to meet you and your chosen caterer six to eight weeks before your wedding to go through the finer details of your booking."),
        ("Minimum and maximum numbers", "Each function suite has a minimum number of guests, although we can be flexible, subject to availability. The Woodlands Suite holds up to 280 guests when no equipment is required, and the Brandon Suite holds up to 100 guests."),
        ("Candles", "For fire safety reasons, naked flames aren't permitted. LED candelabras may be used instead and are just as effective."),
        ("Entertainment", "We can arrange entertainment through our preferred suppliers. You're also welcome to book your own, once we've approved the supplier and checked their public liability insurance and PAT testing certificates."),
        ("Your caterer", "Before confirming your caterer, please ask them to send us evidence of insurance cover, food hygiene certificates, PAT testing certificates for equipment, food handler training certificates, a full menu with a list of dishes, an alcohol licence, details of how the food will be delivered and set up, and a detailed plan for setting up and clearing the event space."),
        ("Cancellation", "If your wedding is cancelled, a cancellation fee applies in line with the terms and conditions of your contract."),
    ]
    faqs = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    body = f"""
<section class="hero">
  <img src="../assets/img/wedding-lawn.jpg" alt="A bride and groom dancing on the lawn in front of the hotel" fetchpriority="high">
  <div class="wrap">
    <span class="kicker" style="color:var(--gold)">Weddings at {HOTEL}</span>
    <h1>The day you've always imagined</h1>
    <p>A country house setting in 17 acres of gardens and woodland, with a team who'll look after every detail.</p>
    <div class="btn-row"><a class="btn btn--book" href="{WED_ENQ}">Book a tour</a><a class="btn btn--light" href="#packages">Wedding packages</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap intro">
    <div class="t"><span class="kicker">Welcome</span><h2>Celebrate in countryside style</h2></div>
    <div class="c">
      <p class="lede">As you make your way up the driveway, the beauty of {HOTEL} gradually reveals itself, with charm at every turn.</p>
      <p>Exchange your vows in 17 acres of gardens and woodland that give the hotel a secluded, romantic atmosphere. Our wedding packages are designed to bring your vision to life, with exclusive, personal touches.</p>
      <p>Whether you're planning an intimate gathering or a grand celebration, we'll be the backdrop for a day full of joy and lasting memories.</p>
    </div>
  </div>
  <div class="wrap mt-3">
    <div class="facts">
      <div><strong>17 acres</strong><span>of gardens and woodland for photographs</span></div>
      <div><strong>280</strong><span>guests in the Woodlands Suite</span></div>
      <div><strong>100</strong><span>guests in the Brandon Suite</span></div>
      <div><strong>7am–midnight</strong><span>private room hire on your day</span></div>
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap split">
    <div class="a"><figure class="mount mount--tall"><img src="../assets/img/wed-02.jpg" alt="A function suite set for a ceremony with rows of chairs and an aisle" loading="lazy"></figure></div>
    <div class="b">
      <span class="kicker">Your ceremony</span>
      <h2>The "I do" moment</h2>
      <p>Wherever you choose to say your vows, you'll find the perfect place here.</p>
      <p>Celebrate in timeless elegance in the Brandon Suite or the Woodlands Suite, where expansive windows fill the room with natural light and look out over the gardens. Or hold your ceremony outdoors, surrounded by grounds that offer endless options for a stunning backdrop.</p>
      <p>Saying "I do" is your moment. We'll simply help you choose the space that makes it magical.</p>
      <p><a class="textlink" href="../meetings-events/spaces/?room=woodlands">See the Woodlands Suite</a> &nbsp; <a class="textlink" href="../meetings-events/spaces/?room=brandon-suite">See the Brandon Suite</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="intro mb-2">
      <div class="t"><span class="kicker">Our grounds</span><h2>Seventeen acres of settings</h2></div>
      <div class="c"><p>Gardens and woodland with endless settings for ceremonies, drinks receptions and photographs, from the lawn in front of the house to the shade of the old trees.</p></div>
    </div>
    <div class="wgallery">
      <img src="../assets/img/wed-12.jpg" alt="A couple under a pergola in the garden" loading="lazy">
      <img src="../assets/img/wedding-tree.jpg" alt="A couple in traditional dress beneath an ancient tree" loading="lazy">
      <img src="../assets/img/wed-16.jpg" alt="A couple embracing under the trees at golden hour" loading="lazy">
      <img src="../assets/img/wedding-walk.jpg" alt="A bride and groom walking across the lawn towards the house" loading="lazy">
      <img src="../assets/img/wed-18.jpg" alt="A couple in the woodland" loading="lazy">
      <img src="../assets/img/wed-06.jpg" alt="An outdoor ceremony in the garden" loading="lazy">
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap split split--flip">
    <div class="a"><figure class="mount"><img src="../assets/img/canapes.jpg" alt="Tomato and mozzarella canapés on a slate" loading="lazy"></figure></div>
    <div class="b">
      <span class="kicker">Your drinks reception</span>
      <h2>Time to toast</h2>
      <p>Take a breath: you're married! Mark those first moments and start celebrating with your loved ones in your exclusive-use suite, styled just for you.</p>
      <p>Enjoy the manicured gardens for your drinks reception and sip Champagne on the patio with your guests. For your wedding breakfast, choose from our menus, each designed to suit your tastes and the season.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="strip">
      <img src="../assets/img/wed-21.jpg" alt="The Woodlands Suite dressed for an evening reception with gold chair covers" loading="lazy">
      <img src="../assets/img/wed-03.jpg" alt="Round tables with pampas grass centrepieces" loading="lazy">
      <img src="../assets/img/table-setting.jpg" alt="A round table laid with white linen and gold chargers" loading="lazy">
      <img src="../assets/img/wed-08.jpg" alt="A tall floral centrepiece by the window" loading="lazy">
      <img src="../assets/img/suite-banquet.jpg" alt="Long banquet tables with pink sashes" loading="lazy">
    </div>
  </div>
</section>

<section class="section section--white" id="packages">
  <div class="wrap">
    <div class="intro mb-3">
      <div class="t"><span class="kicker">Your wedding, your way</span><h2>Wedding packages</h2></div>
      <div class="c">
        <p>From the moment you say "Yes!" to the moment you wave goodbye to your last guest, our wedding packages, inspiring extras, seasonal menus and dedicated team mean you can design the day you've always dreamt of.</p>
        <p class="small">Prices per guest, based on 50 guests. Bespoke packages are available and can be discussed during your tour.</p>
      </div>
    </div>
    <div class="wpkgs">{pkgs}</div>
    <p class="small mt-2">*Choice of Prosecco, bottled beer or a soft drink. If you have any dietary requirements or concerns about food allergies, please ask your wedding coordinator for help when choosing your menu.</p>
  </div>
</section>

<section class="section section--navy" id="self-catering">
  <div class="wrap">
    <div class="intro mb-3">
      <div class="t"><span class="kicker">Your venue, your caterer, your way</span><h2>Self-catering weddings</h2></div>
      <div class="c">
        <p>Our self-catering packages give you exclusive use of a beautiful event space and the support of our experienced team, while you bring in the caterer who knows your tastes best. Your wedding coordinator can recommend preferred suppliers.</p>
      </div>
    </div>
    <div class="sc-grid">
      <div class="sc-card">
        <h3>Room hire for up to 280 guests</h3>
        <table class="wprice wprice--dark"><thead><tr><th scope="col"></th><th scope="col">High season<br><small>May–October</small></th><th scope="col">Low season<br><small>November–April</small></th></tr></thead>
          <tbody><tr><th scope="row">2026</th><td>from £6,000</td><td>from £5,500</td></tr><tr><th scope="row">2027</th><td>from £6,500</td><td>from £6,000</td></tr></tbody></table>
        <h4 class="mt-2">Included</h4>
        <ul class="ticks ticks--one"><li>Room hire from 7am to 11.59pm</li><li>One hotel food and beverage supervisor for eight hours</li><li>No corkage on soft drinks, including fruit juices</li></ul>
      </div>
      <div class="sc-card">
        <h3>Optional extras</h3>
        <ul class="pricelist pricelist--dark">
          <li><span>Day-use bedroom, 10am to 6pm</span><strong>£80 per room</strong></li>
          <li><span>Room-only accommodation in a standard bedroom</span><strong>from £100 per night</strong></li>
          <li><span>Hotel bar in your function room, with two bar staff and glassware</span><strong>£500</strong></li>
          <li><span>Additional waiting staff (minimum eight hours)</span><strong>£15 per hour</strong></li>
          <li><span>Audiovisual equipment and staging</span><strong>On request</strong></li>
          <li><span>Additional linen</span><strong>On request</strong></li>
          <li><span>Alcohol corkage</span><strong>Ask your coordinator</strong></li>
        </ul>
      </div>
    </div>
    <h3 class="mt-3" style="color:#fff">Planning your day</h3>
    <div class="faqs faqs--dark">{faqs}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="a"><figure class="mount"><img src="../assets/img/bedroom-suite.jpg" alt="A suite with a wedding dress hanging by the window" loading="lazy"></figure></div>
    <div class="b">
      <span class="kicker">Stay with us</span>
      <h2>More than a night's sleep</h2>
      <p>Make your wedding last longer by staying with us before and after your big day in one of our bedrooms.</p>
      <p>Unwind in the leisure club, then meet, greet and mingle with your loved ones in a private dining space the night before. The morning after you say "I do", carry on the celebrations over breakfast with your guests, then clear your head with a countryside walk.</p>
      <p>We cater for everyone, with discounted room rates for your wedding guests.</p>
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap split" style="align-items:start">
    <div class="a">
      <span class="kicker">Come and see us</span>
      <h2>Book a tour</h2>
      <p class="lede">Our wedding team would love to show you around and start planning your day.</p>
      <p>Email <a class="textlink" href="mailto:{EMAIL}">{EMAIL}</a> or call <a class="textlink" href="tel:{PHONE_HREF}">{PHONE}</a>. You can also build your plans online, choose your suite and layout, and send them to us in one go.</p>
      <div class="btn-row"><a class="btn btn--book" href="{WED_ENQ}">Book a tour</a><a class="btn btn--line" href="../meetings-events/planner/?type=wedding">Plan your wedding online</a></div>
    </div>
    <div class="b">
      <h3>Brochures</h3>
      {dl(p, "wedding-brochure-2026.pdf", "Wedding brochure 2026", "PDF, 2.7 MB")}
      {dl(p, "self-catering-wedding-brochure-2026.pdf", "Self-catering weddings 2026 and 2027", "PDF, 2.9 MB")}
    </div>
  </div>
</section>
"""
    write("weddings/index.html", h + header(p, "weddings") + body + footer(p))

# ----------------------------------------------------------------
# DINING: The Clarendon and the bar (content from the menus)
# ----------------------------------------------------------------
KEY = "V Vegetarian · VE Vegan · GF Gluten-free · GI Gluten · E Egg · M Milk · F Fish · Mo Molluscs · S Soya · Se Sesame"
ALLERGY = "Please tell a team member about any allergy or intolerance. Our kitchen handles all allergens and cross-contact may occur. Current ingredient and allergen information is available on request."

MENU_DINNER = [
    ("Starters", "A selection of dishes to begin your meal.", [
        ("Soup of the day", "", "Served with rustic bread and butter. Ask the team for today's recipe and allergen details.", "£6.50"),
        ("Pork belly burnt ends", "GI · S", "Pickled red onion, charred corn, spring onion, coriander and soy emulsion.", "£9.95"),
        ("Crispy calamari", "E · Mo", "Lime mayonnaise, pickled red onion and crispy shallots.", "£12.75"),
        ("Southern fried chicken", "GI · E · M", "Ranch dressing.", "£9.95"),
        ("Halloumi fries", "V · M", "Crispy shallots and hot honey.", "£9.95"),
        ("The Brandon Platter", "", "A generous selection of starters, served for sharing. Ask the team for today's components.", "£29.95"),
    ]),
    ("From the grill", "All grill dishes come with fries, roasted tomato, onion and garlic, watercress and Worcestershire dressing.", [
        ("Sirloin steak, 8oz", "", "", "£25.00"),
        ("Ribeye steak, 10oz", "", "", "£28.00"),
        ("Harissa salmon", "F", "", "£24.00"),
        ("Grilled butterfly chicken", "", "", "£20.00"),
        ("Add a sauce", "", "Black garlic and red wine · Miso mushroom (S) · Whisky peppercorn (M)", "£3.50"),
    ]),
    ("Mains", "", [
        ("The 1857 House Burger", "GI · E · M", "6oz British beef patty, Monterey Jack cheese, gem lettuce and red pepper relish in a toasted brioche bun, with skin-on fries.", "£20.95"),
        ("The 1857 Vegan Burger", "VE", "Vegan patty, gem lettuce and red pepper relish, with skin-on fries.", "£17.00"),
        ("Butter chicken curry", "GI · M", "Basmati rice, warm naan bread, mango chutney and poppadoms.", "£22.00"),
        ("Vegetable jalfrezi", "V · GI", "Basmati rice, warm naan bread and poppadoms.", "£22.00"),
        ("Mushroom risotto", "V · M", "Creamy mushroom risotto, truffle and Parmesan.", "£18.00"),
        ("Roasted beetroot and crispy chickpea salad", "V · Se", "Watercress, mixed leaves, roasted beetroot, charred corn, pickled red onion, crispy chickpeas, toasted seeds and maple-mustard dressing. Add grilled butterfly chicken or harissa salmon for £6.00.", "£16.00"),
        ("Cumberland sausage ring", "GI · M", "Mash, black garlic and red wine sauce and crispy shallots.", "£22.95"),
    ]),
    ("Sides", "", [
        ("Creamy mash", "V · M", "", "£4.50"),
        ("Skin-on fries", "", "", "£4.50"),
        ("Sweet potato fries", "", "", "£5.50"),
        ("Garden salad", "VE", "", "£4.50"),
        ("Loaded mac 'n' cheese", "GI · M", "Bacon bits, crispy onions, spring onion and red pepper.", "£4.50"),
    ]),
    ("Desserts", "A sweet finish, served with a little indulgence.", [
        ("Biscoff toffee cheesecake", "V · GI · M", "Toffee popcorn and cream cheese.", "£8.00"),
        ("Vegan orange chocolate mousse", "VE", "Vanilla plant cream and orange tuile.", "£8.00"),
        ("Blondie", "V · GI · E · M · S", "Miso caramel and vanilla ice cream.", "£8.00"),
        ("Sticky toffee pudding", "V · GI · E · M", "Toffee sauce and vanilla ice cream.", "£8.00"),
    ]),
]
MENU_LUNCH = [
    ("Sandwiches", "All sandwiches are served with salad and crisps.", [
        ("Tuna mayonnaise and cucumber", "F · E", "Tuna mayonnaise, crisp cucumber and mixed leaves.", "£8.50"),
        ("Pastrami, mature Cheddar and English mustard mayo", "M", "A generously filled deli-style sandwich.", "£9.50"),
        ("Egg mayonnaise and chive", "V · E", "Creamy egg mayonnaise with fresh chives.", "£7.50"),
        ("Mature Cheddar and pickle", "V", "A proper British classic with tangy pickle.", "£7.50"),
    ]),
    ("Salads and sides", "", [
        ("Chicken Caesar salad", "GI · E · F · M", "Grilled chicken, gem lettuce, Parmesan, anchovies, croutons and Caesar dressing.", "£11.95"),
        ("Skin-on fries", "", "", "£4.50"),
    ]),
    ("Cakes, pastries and hot drinks", "", [
        ("Today's cake and pastry selection", "", "Ask the team for today's selection.", "£4.20"),
        ("Tea, filter coffee or Americano", "", "", "£3.50"),
        ("Latte, cappuccino or flat white", "", "", "£3.95"),
        ("Coffee and croissant", "", "Tea, filter coffee or Americano with a fresh all-butter croissant.", "£6.50"),
    ]),
]
MENU_KIDS = [
    ("Mains", "Little favourites, generously served.", [
        ("Southern fried chicken", "GI · E · M", "Ranch dip and fries.", "£10.00"),
        ("10-inch gluten-free Margherita pizza", "V · GF · M", "Tomato, mozzarella and basil.", "£10.00"),
        ("10-inch gluten-free pepperoni pizza", "GF · M", "Tomato, mozzarella and pepperoni.", "£10.00"),
        ("Sausage and mash", "GI · M", "", "£10.00"),
        ("Mac 'n' cheese", "V · GI · M", "Served with garlic bread.", "£10.00"),
        ("Grilled chicken and chips", "", "", "£10.00"),
    ]),
    ("Desserts", "", [
        ("Triple chocolate brownie sundae", "V · GI · E · M", "", "£6.00"),
        ("Blondie and ice cream", "V · GI · E · M · S", "", "£8.00"),
        ("Waffle", "V · GI · E · M", "Cookies and cream ice cream and chocolate sauce.", "£6.00"),
    ]),
]
MENU_DRINKS = [
    ("White wines", "175ml · 250ml · bottle", [
        ("Vito Lucido Pinot Grigio", "Italy", "Light, crisp and easy-drinking, with delicate blossom aromas.", "£5.65 · £8.00 · £24.00"),
        ("Nyala Sauvignon Blanc", "South Africa", "Fresh and aromatic, with vibrant tropical fruit.", "£6.50 · £9.00 · £27.00"),
        ("Bello Tramonto Pinot Grigio", "Italy", "Light and refreshing, with green apple and zesty citrus.", "£7.50 · £10.00 · £29.50"),
        ("Turtle Bay Sauvignon Blanc", "New Zealand", "Vibrant Marlborough acidity, green apple and citrus.", "£10.00 · £13.25 · £39.95"),
        ("Hay Stack Chardonnay", "South Africa", "Ripe orchard fruit and a soft, buttery finish.", "£9.50 · £13.50 · £40.00"),
        ("Icauna Petit Chablis", "France", "Classic Burgundy white: crisp, flinty and refined.", "Bottle £38.00"),
    ]),
    ("Red wines", "175ml · 250ml · bottle", [
        ("Corte Vigna Merlot", "Italy", "Soft, smooth and medium-bodied, with plum and cherry.", "£5.65 · £8.00 · £25.00"),
        ("Nyala Cabernet Sauvignon", "South Africa", "Ripe blackcurrant, dark berries and subtle spice.", "£6.50 · £9.00 · £27.00"),
        ("St Hallett Faith Shiraz", "Australia", "Dark berries, cracked black pepper and warm spice.", "£9.00 · £12.00 · £32.00"),
        ("Club de Campo Malbec", "Argentina", "Blackberry, dark plum and velvety tannins.", "£9.50 · £12.50 · £36.95"),
        ("Carlos Serres Rioja (organic)", "Spain", "Red berries, subtle vanilla and toasted oak.", "£10.95 · £14.50 · £42.95"),
        ("Nicolis Amarone della Valpolicella", "Italy", "Dried fig, raisin, dark chocolate and spice.", "Bottle £87.00"),
    ]),
    ("Rosé, sparkling and Champagne", "", [
        ("Wicked Lady White Zinfandel", "California", "Medium-sweet, with juicy strawberry and raspberry.", "£5.65 · £8.00 · £24.00"),
        ("Mirabeau Forever Summer", "Provence", "Dry Provence rosé with crisp red berries.", "£8.80 · £12.00 · £36.00"),
        ("Galanti Prosecco Extra Dry", "Italy", "Green apple, crisp pear and fine bubbles.", "£6.00 · £8.00 · £30.00"),
        ("Serenello Prosecco Superiore", "Italy", "Pear, white peach and jasmine.", "£8.50 · £12.00 · £42.00"),
        ("Taittinger Brut Réserve", "Champagne", "Fine bubbles, peach, white flowers and brioche.", "Bottle £110.00"),
    ]),
    ("Beers and soft drinks", "", [
        ("Corona, Peroni, Peroni 0.0% or Heineken 0.0%", "330ml", "", "£4.80"),
        ("Folkington's apple or orange juice", "250ml", "", "£4.50"),
        ("J2O", "", "Orange and passionfruit, apple and raspberry, or apple and mango.", "£4.50"),
        ("Coca-Cola, Diet Coke or Coke Zero", "330ml", "", "£3.20"),
        ("Harrogate still or sparkling water", "330ml / 750ml", "", "£2.50 / £4.50"),
    ]),
]

def menu_html(sections, note=""):
    out = ""
    for title, sub, items in sections:
        rows = "".join(
            f'<li><div class="mi-top"><span class="mi-name">{n}</span>{f"<span class=mi-tag>{t}</span>" if t else ""}<span class="mi-dots" aria-hidden="true"></span><span class="mi-price">{pr}</span></div>{f"<p>{d}</p>" if d else ""}</li>'
            for n, t, d, pr in items)
        out += f'<div class="menu-sec"><h3>{title}</h3>{f"<p class=menu-sub>{sub}</p>" if sub else ""}<ul class="menu-list">{rows}</ul></div>'
    return out + (f'<p class="menu-note">{note}</p>' if note else "")

def dining():
    p = "../"
    h = head(p, f"The Clarendon restaurant and bar | {HOTEL}",
             "The Clarendon at Brandon Hall Hotel and Spa: bistro-style country house dining near Coventry. Grill, classics, vegan dishes, lunch and a relaxed bar. Dinner 6pm daily.")
    tabs = [("dinner", "Restaurant", menu_html(MENU_DINNER, KEY)), ("lunch", "Lunch", menu_html(MENU_LUNCH, KEY)),
            ("children", "Children", menu_html(MENU_KIDS, KEY)), ("drinks", "Wine and drinks", menu_html(MENU_DRINKS, "Wines contain sulphites. All wines are served subject to availability."))]
    tabbtns = "".join(f'<button role="tab" id="tab-{i}" aria-controls="panel-{i}" aria-selected="{"true" if k == 0 else "false"}" tabindex="{0 if k == 0 else -1}">{t}</button>' for k, (i, t, _) in enumerate(tabs))
    panels = "".join(f'<div role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}" class="menu-panel"{"" if k == 0 else " hidden"}>{c}</div>' for k, (i, _, c) in enumerate(tabs))
    body = f"""
<section class="section page-open">
  <div class="wrap split">
    <div class="a">
      <span class="kicker">Dining at {HOTEL}</span>
      <h1 class="h1-page">The Clarendon</h1>
      <p class="lede">Bistro-style dining meets the elegance of a country house.</p>
      <p>Refined yet informal, The Clarendon is for those who want to relax, unwind and be truly looked after. Our kitchen celebrates local produce and the rhythm of the seasons, with honest flavours, classic techniques and a modern twist.</p>
      <div class="hours"><strong>Dinner</strong><span>6pm to 11pm daily, last table at 9pm</span></div>
      <div class="btn-row"><a class="btn btn--book" href="#book-table">Book a table</a><a class="btn btn--line" href="#menus">See the menus</a></div>
    </div>
    <div class="b"><figure class="mount mount--tall"><img src="../assets/img/restaurant.jpg" alt="The Clarendon restaurant with arched windows and tables laid for dinner" fetchpriority="high"></figure></div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <div class="features">
      <article class="feature"><figure class="mount">{rimg(p, "dine-steak.jpg", "2025/09/809d258c6222a6af236ab8c0521abf6a.jpg", "Steak with fries, mushrooms and greens")}</figure><h3>From the grill</h3><p>Sirloin and ribeye steaks, harissa salmon and butterfly chicken, with your choice of sauce.</p></article>
      <article class="feature"><figure class="mount">{rimg(p, "dine-restaurant.jpg", "2025/09/68027_18010908440060921672.jpg", "The restaurant with mirrors and warm lighting")}</figure><h3>Country house classics</h3><p>The 1857 House Burger, butter chicken curry, Cumberland sausage ring and plenty for vegetarians and vegans.</p></article>
      <article class="feature"><figure class="mount">{rimg(p, "dine-cocktail.jpg", "2025/09/fef4bddaeaee390da06b932b53ef4857.jpg", "A gin cocktail with lemon and ice")}</figure><h3>The bar</h3><p>Wines by the glass, Prosecco and Champagne, beers and soft drinks in the relaxed surroundings of our bar and lounge.</p></article>
    </div>
  </div>
</section>

<section class="section" id="menus">
  <div class="wrap">
    <div class="intro mb-2">
      <div class="t"><h2>Our menus</h2></div>
      <div class="c"><p>Seasonal dishes, thoughtfully prepared and made to share. Settle in, take your time and let our team look after the rest.</p><p class="small">{ALLERGY}</p></div>
    </div>
    <div class="menu-card">
      <div class="menu-tabs" role="tablist" aria-label="Menus">{tabbtns}</div>
      {panels}
    </div>
    <p class="small mt-1">Staying on dinner, bed and breakfast? Choose from the restaurant menu, with a small supplement for the sirloin, ribeye and salmon. Menus and prices can change with the seasons.</p>
  </div>
</section>

<section class="section section--white">
  <div class="wrap split split--flip">
    <div class="a"><figure class="mount"><img src="../assets/img/bar-lounge.jpg" alt="The bar with armchairs and a clock above the back bar" loading="lazy"></figure></div>
    <div class="b">
      <span class="kicker">The bar and lounge</span>
      <h2>Sit back and take your time</h2>
      <p>Meet friends for a glass of wine, wind down after a day of meetings, or start the evening with a Prosecco before dinner. Our bar and lounge is the easy-going heart of the hotel.</p>
      <p><a class="textlink" href="#menus" data-open-tab="drinks">See the wine and drinks list</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="a"><figure class="mount">{rimg(p, "dine-tea.jpg", "2025/09/38ae6766b4595803c8c492be14d4e6c8.jpg", "Scones, pastries and cakes on a tiered stand")}</figure></div>
    <div class="b">
      <span class="kicker">Private dining and celebrations</span>
      <h2>Dining for groups</h2>
      <p>Birthday dinners, family celebrations, team nights out and the meal the night before a wedding. Our events team can set a private room just for you, with a menu to match.</p>
      <div class="btn-row"><a class="btn btn--navy" href="../meetings-events/planner/?type=dinner&amp;layout=cabaret">Plan a private dinner</a><a class="btn btn--line" href="../christmas/#festive-dining">Festive dining</a></div>
    </div>
  </div>
</section>


<section class="section section--white" id="book-table">
  <div class="wrap split split--form" style="align-items:start">
    <div class="a">
      <span class="kicker">The Clarendon</span>
      <h2>Book a table</h2>
      <p class="lede">Tell us when you'd like to join us and we'll confirm your table by email or phone.</p>
      <div class="hours"><strong>Dinner</strong><span>6pm to 11pm daily, last table at 9pm</span></div>
      <p class="small mt-1">Your booking is a request until we confirm it. For tables of more than 10, or anything urgent, call us on <a class="textlink" href="tel:{PHONE_HREF}">{PHONE}</a>.</p>
      <figure class="mount mt-2 hide-mobile"><img src="../assets/img/table-setting.jpg" alt="A table laid with white linen, gold chargers and flowers" loading="lazy"></figure>
    </div>
    <div class="b table-form-wrap">
      <form id="t-form" class="t-form" novalidate>
        <div class="grid-3" style="margin-top:0">
          <label class="field" for="t-date">Date<input id="t-date" type="date" required><span class="err" id="t-date-err"></span></label>
          <label class="field" for="t-time">Time<select id="t-time" required></select><span class="err" id="t-time-err"></span></label>
          <label class="field" for="t-guests">Guests<select id="t-guests"></select></label>
        </div>
        <p class="notice" id="t-large" hidden>For 11 or more guests, please call us on {PHONE} or <a href="../meetings-events/planner/?type=dinner&amp;layout=cabaret">plan a private dinner</a>.</p>
        <div class="grid-2 mt-1">
          <label class="field" for="t-name">Name<input id="t-name" type="text" autocomplete="name" required><span class="err" id="t-name-err"></span></label>
          <label class="field" for="t-phone">Phone number<input id="t-phone" type="tel" autocomplete="tel" required><span class="err" id="t-phone-err"></span></label>
        </div>
        <label class="field mt-1" for="t-email">Email<input id="t-email" type="email" autocomplete="email" required><span class="err" id="t-email-err"></span></label>
        <div class="grid-2 mt-1">
          <label class="field" for="t-occasion">Occasion <span class="hint">Optional</span><select id="t-occasion"><option value="">None</option><option>Birthday</option><option>Anniversary</option><option>Celebration</option><option>Business</option><option>Staying at the hotel</option></select></label>
          <label class="field" for="t-highchair">High chairs <span class="hint">Optional</span><select id="t-highchair"><option value="0">None</option><option>1</option><option>2</option><option>3</option></select></label>
        </div>
        <label class="field mt-1" for="t-notes">Dietary needs or requests <span class="hint">Optional</span><textarea id="t-notes" rows="3"></textarea></label>
        <label class="check mt-1" style="border:0"><input type="checkbox" id="t-consent"><span>I'm happy for {HOTEL} to contact me about my booking. See our <a href="../privacy/">privacy notice</a>.</span></label>
        <p class="err" id="t-consent-err"></p>
        <div class="visually-hidden" aria-hidden="true"><label for="t-website">Leave this empty</label><input id="t-website" type="text" tabindex="-1" autocomplete="off"></div>
        <div class="btn-row"><button class="btn btn--book" type="submit" id="t-submit">Request my table</button></div>
      </form>
      <div class="t-done" id="t-done" hidden tabindex="-1">
        <h3 id="t-done-title"></h3>
        <p id="t-done-text"></p>
        <dl id="t-done-list"></dl>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="intro">
      <div class="t"><h2>Printable menus</h2></div>
      <div class="c">
      {dl(p, "clarendon-restaurant-menu.pdf", "Restaurant menu", "PDF, 1.4 MB")}
      {dl(p, "clarendon-lunch-menu.pdf", "Lunch menu", "PDF, 0.2 MB")}
      {dl(p, "clarendon-dinner-bed-breakfast-menu.pdf", "Dinner, bed and breakfast menu", "PDF, 0.2 MB")}
      {dl(p, "clarendon-restaurant-bar-wine-list.pdf", "Restaurant and bar wine list", "PDF, 0.2 MB")}
      {dl(p, "clarendon-wine-list.pdf", "Wine list", "PDF, 0.2 MB")}
      </div>
    </div>
  </div>
</section>
"""
    write("dining/index.html", h + header(p, "dining") + body + footer(p, ["venue-data.js", "table.js"]))

# ----------------------------------------------------------------
# CONTACT
# ----------------------------------------------------------------
MAP_EMBED = "https://www.google.com/maps?q=Brandon+Hall+Hotel+and+Spa,+Main+Street,+Brandon,+Coventry+CV8+3FW&amp;output=embed"

def contact():
    p = "../"
    h = head(p, f"Contact and directions | {HOTEL}",
             "Contact Brandon Hall Hotel and Spa, Main Street, Brandon, Wolston, Coventry CV8 3FW. Call 024 7710 2555 or email events@brandonhallhotelandspa.com.")
    body = f"""
<section class="section page-open">
  <div class="wrap intro">
    <div class="t"><h1 class="h1-page">Contact us</h1></div>
    <div class="c">
      <p class="lede">We're here to help, whether you're booking a stay, planning an event or have a question before you arrive.</p>
      <p>Our reception is open 24 hours a day.</p>
    </div>
  </div>
</section>

<section class="section section--white" style="padding-top:64px">
  <div class="wrap contact-grid">
    <div>
      <div class="c-block"><h3>Call us</h3><p><a class="big-link" href="tel:{PHONE_HREF}">{PHONE}</a></p></div>
      <div class="c-block"><h3>Email us</h3><p><a class="big-link" href="mailto:{EMAIL}">{EMAIL}</a></p><p class="small">For events, weddings, meetings and general enquiries.</p></div>
      <div class="c-block"><h3>Find us</h3>
        <address>{HOTEL}<br>Main Street, Brandon, Wolston<br>Coventry CV8 3FW</address>
        <p class="small mt-1">Use CV8 3FW for sat nav. On-site parking is available for guests.</p>
        <p><a class="textlink" href="{MAPS}" target="_blank" rel="noopener">Get directions in Google Maps</a></p>
      </div>
      <div class="c-block"><h3>Quick links</h3>
        <ul class="ticks ticks--one">
          <li><a href="{BOOK}" target="_blank" rel="noopener">Book a room</a></li>
          <li><a href="../dining/#book-table">Book a table at The Clarendon</a></li>
          <li><a href="../meetings-events/planner/">Plan a meeting or event</a></li>
          <li><a href="../weddings/">Book a wedding tour</a></li>
        </ul>
      </div>
    </div>
    <div>
      <h2>Send us a message</h2>
      <form id="c-form" class="c-form" novalidate>
        <div class="grid-2">
          <label class="field" for="c-name">Name<input id="c-name" type="text" autocomplete="name" required><span class="err" id="c-name-err"></span></label>
          <label class="field" for="c-phone">Phone number<input id="c-phone" type="tel" autocomplete="tel"></label>
        </div>
        <label class="field mt-1" for="c-email">Email<input id="c-email" type="email" autocomplete="email" required><span class="err" id="c-email-err"></span></label>
        <label class="field mt-1" for="c-topic">What's it about?<select id="c-topic"><option>A stay</option><option>Dining</option><option>A wedding</option><option>A meeting or event</option><option>Christmas and New Year</option><option>Something else</option></select></label>
        <label class="field mt-1" for="c-msg">Your message<textarea id="c-msg" rows="6" required></textarea><span class="err" id="c-msg-err"></span></label>
        <label class="check mt-1" style="border:0"><input type="checkbox" id="c-consent"><span>I'm happy for {HOTEL} to contact me about my message. See our <a href="../privacy/">privacy notice</a>.</span></label>
        <p class="err" id="c-consent-err"></p>
        <div class="visually-hidden" aria-hidden="true"><label for="c-website">Leave this empty</label><input id="c-website" type="text" tabindex="-1" autocomplete="off"></div>
        <div class="btn-row"><button class="btn btn--book" type="submit" id="c-submit">Send message</button></div>
        <p class="notice" id="c-done" hidden tabindex="-1"></p>
      </form>
    </div>
  </div>
</section>

<section class="map-wrap">
  <iframe title="Map showing {HOTEL}" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</section>
"""
    write("contact/index.html", h + header(p, "contact") + body + footer(p, ["venue-data.js", "contact.js"]))


# ----------------------------------------------------------------
# PRIVACY (draft based on how this website handles data; to be
# checked by the hotel before launch)
# ----------------------------------------------------------------
def privacy():
    p = "../"
    h = head(p, f"Privacy notice | {HOTEL}", "How Brandon Hall Hotel and Spa collects, uses and protects your personal information when you use this website.")
    body = f"""
<section class="section page-open">
  <div class="wrap prose">
    <h1 class="h1-page">Privacy notice</h1>
    <p class="lede">This notice explains how we collect, use and look after your personal information when you use this website or get in touch with us.</p>

    <h2>Who we are</h2>
    <p>{HOTEL} is operated by 7 Hospitality Management Ltd, which is the controller of your personal information. You can contact us at {HOTEL}, Main Street, Brandon, Wolston, Coventry CV8 3FW, by email at <a href="mailto:{EMAIL}">{EMAIL}</a> or by phone on {PHONE}.</p>

    <h2>What we collect</h2>
    <p>When you use our event planner, contact form or email us, we collect the details you give us: your name, company or organisation, email address, phone number, and information about your stay, event or enquiry, such as dates, numbers, room choices, catering, accommodation and any notes you add. Please only tell us about dietary or access needs if you want us to take them into account.</p>
    <p>When you book a room, the booking is handled by our booking partner, Profitroom, and their privacy notice also applies.</p>

    <h2>How we use it</h2>
    <p>We use your information to reply to your enquiry, prepare quotes and proposals, manage your booking or event, and keep a record of our conversations with you. We rely on our legitimate interest in responding to people who contact us, and on taking steps at your request before entering into a contract. We won't send you marketing unless you've asked us to, and we never sell your information.</p>

    <h2>Where it's stored</h2>
    <p>Enquiries from this website go into our own enquiry system, which is hosted on Google Cloud (Firebase). Only authorised members of our team can see them. Emails are held in our email system.</p>

    <h2>How long we keep it</h2>
    <p>We keep enquiry details for as long as we need them to deal with your enquiry and any booking that follows, and for a reasonable time afterwards for our records and to meet legal and accounting requirements. After that we delete them.</p>

    <h2>Cookies and your browser</h2>
    <p>This website doesn't use advertising or tracking cookies. To save you retyping, the event planner remembers the name and contact details you enter on your own device (in your browser's local storage), and the site notes whether you've already seen the opening screen on your phone. You can clear these at any time by clearing your browser data. Our contact page shows a Google map, and our booking pages are provided by Profitroom; these services may set their own cookies.</p>

    <h2>Your rights</h2>
    <p>You can ask to see the personal information we hold about you, ask us to correct or delete it, object to how we use it, or ask us to restrict it. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we'll respond within one month.</p>
    <p>If you're unhappy with how we've handled your information, please tell us first. You also have the right to complain to the Information Commissioner's Office (ICO) at <a href="https://ico.org.uk" target="_blank" rel="noopener">ico.org.uk</a> or on 0303 123 1113.</p>

    <p class="small mt-3">Last updated: September 2026.</p>
  </div>
</section>
"""
    write("privacy/index.html", h + header(p, "") + body + footer(p))


def accessibility():
    p = "../"
    h = head(p, f"Accessibility | {HOTEL}", "Our commitment to making the Brandon Hall Hotel and Spa website easy to use for everyone, and how to get help.")
    body = f"""
<section class="section page-open">
  <div class="wrap prose">
    <h1 class="h1-page">Accessibility</h1>
    <p class="lede">We want everyone to be able to use this website and enjoy their visit to {HOTEL}.</p>

    <h2>This website</h2>
    <p>We've built this site to meet the Web Content Accessibility Guidelines (WCAG) 2.2 at level AA. That means you should be able to:</p>
    <ul class="ticks ticks--one">
      <li>zoom in up to 400% without text spilling off the screen</li>
      <li>move around the site using only a keyboard, with a "Skip to main content" link at the top of every page</li>
      <li>use the site with a screen reader, with descriptions on our photographs</li>
      <li>read text with good contrast against its background</li>
      <li>turn off animations using your device's reduced-motion setting</li>
    </ul>

    <h2>What we know isn't fully accessible</h2>
    <ul class="ticks ticks--one">
      <li>Some of our brochures and printable menus are PDFs, which may not work well with screen readers. The same information is on the website pages themselves, and we're happy to send it in another format.</li>
      <li>The floor plans in our event planner are pictures. The room sizes and capacities are also shown in text and in the capacity chart.</li>
      <li>The map on our contact page and our room booking pages are provided by other companies.</li>
    </ul>

    <h2>At the hotel</h2>
    <p>We have accessible Classic and Executive rooms. If you or anyone in your party has access needs, please let us know when you book, or call us before you arrive, and we'll do everything we can to help.</p>

    <h2>Tell us about a problem</h2>
    <p>If you find something on this website hard to use, or need information in a different format, please email <a href="mailto:{EMAIL}">{EMAIL}</a> or call {PHONE}. We'll reply as soon as we can.</p>

    <p class="small mt-3">This statement was prepared in September 2026.</p>
  </div>
</section>
"""
    write("accessibility/index.html", h + header(p, "") + body + footer(p))

if __name__ == "__main__":
    home(); meetings(); spaces(); planner(); rooms(); leisure(); out_about(); christmas(); offers(); weddings(); dining(); contact(); privacy(); accessibility(); seo_files()
