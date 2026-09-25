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
SITE_URL = "https://www.brandonhallhotelandspa.com"

NAV_LEFT = [("stay", "rooms-suites/", "Stay"), ("dining", "dining/", "Dining"), ("spa", "spa-leisure/", "Spa &amp; Leisure")]
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
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE_URL}/assets/img/exterior-summer.jpg">
<link rel="icon" href="{p}assets/brand/favicon.png">
<link rel="preload" href="{p}assets/fonts/italiana-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/lato-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/site.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
'''


def header(p, active):
    def links(items):
        out = []
        for key, href, label in items:
            cur = ' aria-current="page"' if key == active else ""
            out.append(f'<a href="{p}{href}"{cur}>{label}</a>')
        return "\n      ".join(out)
    drawer_links = "".join(f'<a href="{p}{h}">{l}</a>' for _, h, l in NAV_LEFT + NAV_RIGHT + [("o", "offers/", "Offers"), ("c", "contact/", "Contact")])
    return f'''<div class="utility">
  <div class="wrap">
    <span class="u-hide">Main Street, Brandon, near Coventry</span>
    <div class="u-links">
      <a href="tel:{PHONE_HREF}">{PHONE}</a>
      <a class="u-hide" href="{p}offers/">Offers</a>
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
          <li><a href="{p}spa-leisure/">Spa and leisure</a></li>
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
<div class="be-panel"></div>
<script src="https://wis.upperbooking.com/brandonhallhotelspawarwickshire/be-panel?locale=en" defer></script>
{s}<script src="{p}assets/js/site.js"></script>
</body>
</html>
'''


def dl(p, file, title, sub):
    return f'<a class="download" href="{p}downloads/{file}" download><span class="doc" aria-hidden="true"></span><span><strong>{title}</strong><span>{sub}</span></span></a>'


def write(path, html):
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
        "image": SITE_URL + "/assets/img/exterior-summer.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": "Main Street, Brandon", "addressLocality": "Wolston, Coventry", "postalCode": "CV8 3FW", "addressCountry": "GB"},
        "geo": {"@type": "GeoCoordinates", "latitude": 52.383, "longitude": -1.4061},
        "sameAs": [IG, FB],
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in ["Free on-site parking", "Indoor swimming pool", "Restaurant", "Meeting rooms", "Pet-friendly rooms on request"]]
    }
    h = head(p, f"{HOTEL} | Country house hotel near Coventry, Warwickshire",
             "A historic country house hotel and spa in 17 acres of Warwickshire gardens and woodland, near Coventry. Rooms, The Clarendon restaurant, weddings, meetings and events.",
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
      <div><strong>Free</strong><span>on-site parking for every guest</span></div>
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
      <a class="path" href="spa-leisure/"><img src="assets/img/pool.jpg" alt="The indoor swimming pool under a glazed roof" loading="lazy"><div class="t"><h3>Spa and leisure</h3><span>Pool, leisure club and treatments</span></div></a>
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
      <a class="offer" href="offers/"><h3>Book 4 nights, receive the 5th free</h3><p>Extend your escape and make the most of the countryside.</p></a>
      <a class="offer" href="offers/"><h3>Stay 2 nights and save 15%</h3><p>A little longer to unwind, for a little less.</p></a>
      <a class="offer" href="offers/"><h3>Stay 3 nights and save 20%</h3><p>20% off stays of three nights or more.</p></a>
      <a class="offer" href="offers/"><h3>Suite Dreams</h3><p>Everything you need for a relaxing countryside escape.</p></a>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="wrap split split--flip">
    <div class="a"><figure class="mount"><img src="assets/img/christmas-table.jpg" alt="A festive dinner table with candles, crackers and glasses of wine" loading="lazy"></figure></div>
    <div class="b">
      <span class="kicker">Christmas and New Year 2026</span>
      <h2>Celebrate the season with us</h2>
      <p>Private and joiner party nights with live entertainment, a traditional Christmas Day lunch and a New Year's Eve gala dinner, all in the warmth of the country house.</p>
      <div class="btn-row">
        <a class="btn btn--book" href="christmas/">Christmas and New Year</a>
        <a class="btn btn--light" href="downloads/christmas-brochure-2026.pdf" download>Download the brochure</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="a">
      <span class="kicker">Getting here</span>
      <h2>In the heart of Warwickshire</h2>
      <p>We're on Main Street in the village of Brandon, just outside Coventry. Warwick, Kenilworth and Stratford-upon-Avon are all within easy reach, with good links to the M6, M69 and M45.</p>
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
             "Meeting rooms and event spaces near Coventry for up to 280 guests. Day delegate packages from £35, 24-hour packages, on-site bedrooms and an online event planner.")
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
             "Compare all 14 meeting and event rooms at Brandon Hall Hotel and Spa: sizes, capacities for theatre, cabaret, boardroom, U-shape and reception, floor plans and technology.")
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
             "Plan your meeting, conference or celebration at Brandon Hall Hotel and Spa. Choose a room and layout drawn to scale, add catering, extras and group bedrooms, and request a quote.")
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


if __name__ == "__main__":
    home(); meetings(); spaces(); planner()
    holding("rooms-suites", "stay", "Rooms and suites", "Comfortable rooms and suites looking out over our Warwickshire gardens.", "bedroom-yellow.jpg", "A bright double bedroom with yellow accents")
    holding("dining", "dining", "The Clarendon", "Seasonal menus, relaxed lunches and dinner in the country house.", "restaurant.jpg", "The Clarendon restaurant with arched windows",
            [("clarendon-restaurant-menu.pdf", "Restaurant menu", "PDF, 1.4 MB"), ("clarendon-lunch-menu.pdf", "Lunch menu", "PDF, 0.2 MB"), ("clarendon-dinner-bed-breakfast-menu.pdf", "Dinner, bed and breakfast menu", "PDF, 0.2 MB"), ("clarendon-wine-list.pdf", "Wine list", "PDF, 0.2 MB"), ("clarendon-restaurant-bar-wine-list.pdf", "Restaurant and bar wine list", "PDF, 0.2 MB")])
    holding("weddings", "weddings", "Weddings", "A country house setting, 17 acres of gardens and woodland, for the day you've always imagined.", "wedding-lawn.jpg", "A bride and groom dancing on the lawn in front of the hotel",
            [("wedding-brochure-2026.pdf", "Wedding brochure 2026", "PDF, 2.7 MB"), ("self-catering-wedding-brochure-2026.pdf", "Self-catering weddings 2026", "PDF, 2.9 MB")])
    holding("christmas", "christmas", "Christmas and New Year", "Party nights, Christmas Day lunch and a New Year's Eve gala dinner.", "christmas-party.jpg", "Friends celebrating with sparklers",
            [("christmas-brochure-2026.pdf", "Christmas and New Year brochure 2026", "PDF, 9.6 MB")])
    holding("spa-leisure", "spa", "Spa and leisure", "An indoor pool, leisure club and treatments to help you unwind.", "pool.jpg", "The indoor swimming pool under a glazed roof")
    holding("offers", "offers", "Offers", "Book direct with us for the best available rate.", "exterior-lawn.jpg", "The hotel across the lawn",
            extra=f'<div class="btn-row"><a class="btn btn--book" href="{BOOK}" target="_blank" rel="noopener" data-book>Check availability</a></div>')
    holding("contact", "contact", "Contact and directions", "Main Street, Brandon, Wolston, Coventry CV8 3FW.", "exterior-dusk.jpg", "The hotel lit up at dusk",
            extra=f'<p><a class="textlink" href="{MAPS}" target="_blank" rel="noopener">Find us on Google Maps</a></p>')
    holding("privacy", "", "Privacy notice", "How we look after your personal information.", "exterior-front.jpg", "The front of the hotel")
    holding("accessibility", "", "Accessibility", "Our commitment to making the hotel and this website easy to use for everyone.", "reception.jpg", "The reception desk")
