/* ==========================================================
   Brandon Hall Hotel and Spa — public venue data
   ----------------------------------------------------------
   Edit this one file to update rooms, capacities, packages
   and contact settings. Everything on the Meetings & Events
   pages and in the Event Planner reads from here.

   Source: HOSPRO room data + M&E audit (20 March 2026) and the
   Meetings at Brandon Hall Hotel and Spa brochure (rates inc VAT).
   Rooms flagged "not ready to sell" in HOSPRO (Beech, Hunt,
   Warwick) are left out on purpose. Add them back when ready.
   ========================================================== */

window.BH_CONFIG = {
  hotelName: "Brandon Hall Hotel and Spa",
  phone: "024 7710 2555",
  phoneHref: "+442477102555",
  eventsEmail: "events@brandonhallhotelandspa.com",

  /* Enquiries go straight into HOSPRO (Firestore "enquiries"
     collection, project brandonhall-7bdef). They appear in the
     HOSPRO enquiry list with source "Website". If HOSPRO can't be
     reached, the visitor's email app opens instead, addressed to
     eventsEmail with the full specification filled in.
     The web API key below is a public identifier, not a secret.
     Access is controlled by the Firestore rules (see README). */
  hospro: {
    enabled: true,
    sdk: "https://www.gstatic.com/firebasejs/10.12.2/",
    firebase: {
      apiKey: "AIzaSyDnPWrPGInDRTCF1Go710XC_8_77l_72i0",
      authDomain: "brandonhall-7bdef.firebaseapp.com",
      projectId: "brandonhall-7bdef",
      storageBucket: "brandonhall-7bdef.firebasestorage.app",
      messagingSenderId: "391317900568",
      appId: "1:391317900568:web:643c9d6691f7f16d65226d"
    }
  },

  /* Show package "from" prices (as printed in the brochure). */
  showPackagePrices: true,

  bookingUrl: "https://booking.profitroom.com/en/brandonhallhotelspawarwickshire/home?no-cache=&currency=GBP"
};

/* Seating layouts. Order sets the order everywhere on the site. */
window.BH_LAYOUTS = [
  { id: "theatre",   label: "Theatre",   desc: "Rows of chairs facing the front. Best for presentations, talks and ceremonies." },
  { id: "cabaret",   label: "Cabaret",   desc: "Round tables with an open side facing the front. Ideal for workshops, awards and dinners." },
  { id: "boardroom", label: "Boardroom", desc: "One table with everyone seated around it. Suited to board meetings and discussions." },
  { id: "ushape",    label: "U-shape",   desc: "Tables in a U, open towards the presenter. Good for training with plenty of interaction." },
  { id: "reception", label: "Reception", desc: "Standing, with a few poseur tables. For drinks receptions and networking." }
];

/* Rooms.
   m2      floor area as published
   length / width in metres, used to draw the plans to scale
   cap     capacity per layout. 0 or null = not offered in that layout
   group   rooms that divide or combine are grouped together
   tech    what's in the room (from the M&E audit)            */
window.BH_ROOMS = [
  {
    id: "woodlands", name: "Woodlands Suite", group: "Woodlands",
    m2: 279, length: 19.0, width: 13.05,
    cap: { theatre: 120, cabaret: 200, boardroom: 112, ushape: 90, reception: 280 },
    summary: "Our largest space, with windows along its length looking out over the gardens. Hosts conferences, gala dinners, awards and wedding celebrations. Divides into Woodlands 1 and Woodlands 2.",
    tech: ["Screen and HDMI connection", "PA system and microphones", "Complimentary Wi-Fi", "Flipchart with pads and pens", "Natural daylight"]
  },
  {
    id: "woodlands-1", name: "Woodlands 1", group: "Woodlands",
    m2: 140, length: 9.5, width: 13.05,
    cap: { theatre: 55, cabaret: 90, boardroom: 50, ushape: 40, reception: 120 },
    summary: "One half of the Woodlands Suite, with its own natural light. A generous room for mid-sized conferences and dinners.",
    tech: ["Screen and HDMI connection", "PA system and microphones", "Complimentary Wi-Fi", "Flipchart with pads and pens", "Natural daylight"]
  },
  {
    id: "woodlands-2", name: "Woodlands 2", group: "Woodlands",
    m2: 140, length: 9.5, width: 13.05,
    cap: { theatre: 55, cabaret: 90, boardroom: 50, ushape: 40, reception: 120 },
    summary: "The other half of the Woodlands Suite. Works well as a plenary room or paired with Woodlands 1 as a breakout.",
    tech: ["Screen and HDMI connection", "PA system and microphones", "Complimentary Wi-Fi", "Flipchart with pads and pens", "Natural daylight"]
  },
  {
    id: "brandon-suite", name: "Brandon Suite", group: "Brandon",
    m2: 130, length: null, width: null,
    cap: { theatre: 40, cabaret: 90, boardroom: 36, ushape: 30, reception: 100 },
    summary: "Brandon 1 and Brandon 2 opened into one light-filled suite, with large windows over the gardens. A favourite for ceremonies, celebrations and presentations.",
    tech: ["Two 98\" 4K smart screens", "ClickShare wireless screen sharing", "HDMI and USB-C connections", "Set up for Teams and Zoom calls", "PA system", "Complimentary Wi-Fi", "Natural daylight"]
  },
  {
    id: "brandon-1", name: "Brandon 1", group: "Brandon",
    m2: 54, length: 13.26, width: 6.55,
    cap: { theatre: 26, cabaret: 30, boardroom: 26, ushape: 26, reception: 60 },
    summary: "A bright, flexible room with its own refreshment area. The screen tucks away when the room is set for a social event.",
    tech: ["98\" 4K smart screen on a height-adjustable stand", "ClickShare wireless screen sharing", "HDMI and USB-C connections", "Set up for Teams and Zoom calls", "Complimentary Wi-Fi", "Flipchart with pads and pens"]
  },
  {
    id: "brandon-2", name: "Brandon 2", group: "Brandon",
    m2: 76, length: 9.23, width: 6.08,
    cap: { theatre: 40, cabaret: 60, boardroom: 36, ushape: 30, reception: 100 },
    summary: "The larger half of the Brandon Suite, equally at home as a training room or a private dining space.",
    tech: ["98\" 4K smart screen on a height-adjustable stand", "ClickShare wireless screen sharing", "HDMI and USB-C connections", "Set up for Teams and Zoom calls", "Complimentary Wi-Fi", "Flipchart with pads and pens"]
  },
  {
    id: "wolston-suite", name: "Wolston Suite", group: "Wolston",
    m2: 88, length: 17.9, width: 4.75,
    cap: { theatre: 35, cabaret: 50, boardroom: 30, ushape: 28, reception: 80 },
    summary: "A long, elegant room with a second screen halfway down so everyone has a clear view of the presentation.",
    tech: ["75\" 4K smart screen plus a second screen", "ClickShare wireless screen sharing", "HDMI and USB-C connections", "Set up for Teams and Zoom calls", "PA system", "Complimentary Wi-Fi", "Flipchart with pads and pens"]
  },
  {
    id: "wolston-1", name: "Wolston 1", group: "Wolston",
    m2: 37, length: 7.91, width: 4.75,
    cap: { theatre: 12, cabaret: 20, boardroom: 14, ushape: 12, reception: 30 },
    summary: "A quiet meeting room for small teams, interviews and training.",
    tech: ["Screen and HDMI connection", "Complimentary Wi-Fi", "Flipchart with pads and pens"]
  },
  {
    id: "wolston-2", name: "Wolston 2", group: "Wolston",
    m2: 38, length: 5.75, width: 5.0,
    cap: { theatre: 12, cabaret: 20, boardroom: 14, ushape: 12, reception: 30 },
    summary: "A square, comfortable room that suits workshops and syndicate groups.",
    tech: ["Screen and HDMI connection", "Complimentary Wi-Fi", "Flipchart with pads and pens"]
  },
  {
    id: "wolston-3", name: "Wolston 3", group: "Wolston",
    m2: 24, length: 5.3, width: 4.75,
    cap: { theatre: 12, cabaret: 10, boardroom: 10, ushape: 10, reception: 24 },
    summary: "An intimate room for one-to-ones, interviews and small board meetings.",
    tech: ["Screen and HDMI connection", "Complimentary Wi-Fi", "Flipchart with pads and pens"]
  },
  {
    id: "allkins", name: "Allkins", group: "Meeting rooms",
    m2: 53, length: null, width: null,
    cap: { theatre: 30, cabaret: null, boardroom: 26, ushape: 20, reception: 40 },
    summary: "A well-proportioned meeting room for boardroom sessions and presentations.",
    tech: ["Screen and HDMI connection", "Complimentary Wi-Fi", "Flipchart with pads and pens"]
  },
  {
    id: "parke", name: "Parke", group: "Meeting rooms",
    m2: 40, length: 6.98, width: 6.67,
    cap: { theatre: 16, cabaret: null, boardroom: 17, ushape: 16, reception: 40 },
    summary: "A near-square room that makes a comfortable boardroom for up to 17.",
    tech: ["Screen and HDMI connection", "Complimentary Wi-Fi", "Flipchart with pads and pens"]
  },
  {
    id: "jones", name: "Jones", group: "Meeting rooms",
    m2: 40, length: 8.20, width: 4.88,
    cap: { theatre: 10, cabaret: null, boardroom: 14, ushape: 10, reception: 20 },
    summary: "A private boardroom for small teams and interviews.",
    tech: ["Screen and HDMI connection", "Complimentary Wi-Fi", "Flipchart with pads and pens"]
  },
  {
    id: "johnson", name: "Johnson", group: "Meeting rooms",
    m2: 23, length: 5.08, width: 4.22,
    cap: { theatre: 10, cabaret: null, boardroom: 10, ushape: 10, reception: 10 },
    summary: "Our smallest room, for focused meetings of up to ten.",
    tech: ["Screen and HDMI connection", "Complimentary Wi-Fi", "Flipchart with pads and pens"]
  }
];

/* Packages — prices from the Meetings brochure, per person, inc VAT */
window.BH_PACKAGES = [
  {
    id: "ddr", name: "Day Delegate", midweek: 35, weekend: 30,
    includes: ["Meeting room hire", "Unlimited tea, coffee and water", "Sweet and savoury refreshments mid-morning and mid-afternoon", "Hot and cold lunch options", "Screen and HDMI cable", "Flipchart with pads and pens", "Complimentary Wi-Fi", "Complimentary car parking"]
  },
  {
    id: "24hr", name: "24-Hour", midweek: 155, weekend: 155,
    includes: ["Everything in the Day Delegate package", "One night's accommodation", "Breakfast the next morning"]
  },
  {
    id: "hire", name: "Room hire", midweek: null, weekend: null,
    includes: ["The room, set to your layout", "Choose catering and extras separately", "We'll price it in your quote"]
  }
];

/* À la carte catering. Prices are left off the public site by
   default. They are quoted by the events team. */
window.BH_CATERING = [
  { id: "arrival-tea", name: "Tea, coffee and pastries on arrival" },
  { id: "breakfast-rolls", name: "Bacon and egg rolls" },
  { id: "unlimited-tea", name: "Unlimited tea and coffee all day" },
  { id: "sandwich-lunch", name: "Sandwich lunch" },
  { id: "soup-sandwich", name: "Soup and sandwich lunch" },
  { id: "cold-buffet", name: "Cold buffet lunch in the restaurant" },
  { id: "hot-buffet", name: "Hot buffet lunch in the restaurant" },
  { id: "chefs-lunch", name: "Chef's choice lunch" },
  { id: "fruit", name: "Fresh fruit platters" },
  { id: "canapes", name: "Canapés" },
  { id: "arrival-drink", name: "Arrival drink (wine, beer or soft drink)" },
  { id: "prosecco", name: "Prosecco reception" },
  { id: "dinner", name: "Evening dinner" }
];

/* Extras and equipment */
window.BH_EXTRAS = [
  { id: "breakout", name: "An additional breakout room" },
  { id: "pa", name: "PA system and microphones" },
  { id: "second-screen", name: "Additional screen" },
  { id: "clickshare", name: "Wireless screen sharing (ClickShare)" },
  { id: "video-call", name: "Hybrid meeting set-up for Teams or Zoom" },
  { id: "flipcharts", name: "Extra flipcharts" },
  { id: "stage", name: "Staging" },
  { id: "dj", name: "DJ (Sound Kicks, our preferred supplier)" },
  { id: "spa", name: "Spa or leisure access for delegates" },
  { id: "teambuilding", name: "Team-building in the grounds" }
];

/* Event types and their typical layouts. */
/* hospro = the matching event type in HOSPRO */
window.BH_EVENT_TYPES = [
  { id: "meeting",     label: "Meeting",          hospro: "meeting",     layouts: ["boardroom", "ushape", "theatre"], carbonPerHead: 2.1 },
  { id: "conference",  label: "Conference",       hospro: "meeting",     layouts: ["theatre", "cabaret"],             carbonPerHead: 2.1 },
  { id: "training",    label: "Training day",     hospro: "meeting",     layouts: ["ushape", "cabaret", "boardroom"], carbonPerHead: 2.1 },
  { id: "dinner",      label: "Dinner or awards", hospro: "celebration", layouts: ["cabaret"],                        carbonPerHead: 6.0 },
  { id: "celebration", label: "Celebration",      hospro: "celebration", layouts: ["cabaret", "reception"],           carbonPerHead: 4.0 },
  { id: "christmas",   label: "Christmas party",  hospro: "christmas",   layouts: ["cabaret", "reception"],           carbonPerHead: 6.0 },
  { id: "other",       label: "Something else",   hospro: "celebration", layouts: ["theatre", "cabaret", "reception"],carbonPerHead: 3.0 }
];

/* Carbon estimate factors (HOSPRO model, indicative only).
   Room energy: kWh per m² per day × UK grid factor.
   Accommodation: kg CO2e per occupied room night (UK hotel benchmark). */
window.BH_CARBON = {
  kwhPerM2Day: 0.35,
  kgPerKwh: 0.207,
  kgPerRoomNight: 10.4
};

/* Where a room has no measured dimensions, derive a footprint
   from its area at a 1.4:1 ratio. */
window.bhRoomDims = function (room) {
  if (room.length && room.width) {
    return room.length >= room.width
      ? { L: room.length, W: room.width }
      : { L: room.width, W: room.length };
  }
  var W = Math.sqrt(room.m2 / 1.4);
  return { L: +(W * 1.4).toFixed(1), W: +W.toFixed(1) };
};

/* Meeting and event photographs.
   src = copy in this repo (assets/img/meetings). Run the
   "Fetch meeting photos" GitHub Action once to download them.
   Until then each image falls back to the current hotel website. */
window.BH_MEETING_PHOTOS = [
  { src: "assets/img/meetings/meeting-1.png",  remote: "https://www.brandonhallhotelandspa.com/wp-content/uploads/2025/09/1758893100-1000x667.png",  alt: "A meeting room set with seating and a presentation screen" },
  { src: "assets/img/meetings/meeting-2.png",  remote: "https://www.brandonhallhotelandspa.com/wp-content/uploads/2025/09/1758893782-1000x757.png",  alt: "A conference room with round tables, presentation boards and natural light" },
  { src: "assets/img/meetings/meeting-3.png",  remote: "https://www.brandonhallhotelandspa.com/wp-content/uploads/2025/09/1758893922-1000x757.png",  alt: "An event space set with comfortable seating" },
  { src: "assets/img/meetings/meeting-4.jpeg", remote: "https://www.brandonhallhotelandspa.com/wp-content/uploads/2025/09/brandon-hall-hotel-spa-warwickshire-brandon-warwickshire-pic-4-1000x750.jpeg", alt: "A conference room with round tables and a presentation screen" },
  { src: "assets/img/meetings/meeting-5.jpeg", remote: "https://www.brandonhallhotelandspa.com/wp-content/uploads/2025/09/brandon-hall-hotel-spa-warwickshire-brandon-warwickshire-pic-9-1000x750.jpeg", alt: "A function suite set for a corporate dinner" },
  { src: "assets/img/meetings/meeting-6.jpeg", remote: "https://www.brandonhallhotelandspa.com/wp-content/uploads/2025/09/brandon-hall-hotel-spa-warwickshire-brandon-warwickshire-pic-5.jpeg", alt: "A function suite dressed with white linen, red accents and candles" }
];
