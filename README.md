# Brandon Hall Hotel and Spa website

Static multi-page site for GitHub Pages. No build step is needed to publish: every page is plain HTML.

## Publish on GitHub Pages
1. Upload the contents of this folder to the root of the `orngroup/brandon-website` repository (keep `.nojekyll`).
2. Repository **Settings > Pages**: Source "Deploy from a branch", branch `main`, folder `/ (root)`.
3. Preview address: `https://orngroup.github.io/brandon-website/`. All links are relative, so the site works there and on the real domain.
4. To go live on the hotel domain, add a `CNAME` file containing `www.brandonhallhotelandspa.com`, then point the domain's DNS at GitHub Pages. Do this only when the full site is signed off, as it replaces the current WordPress site.

## Editing
- **Rooms, capacities, packages, catering, extras, contact settings:** `assets/js/venue-data.js`. The Meetings pages and the Event Planner all read from this one file.
- **Where quote requests go:** straight into HOSPRO. The Event Planner signs in anonymously to the HOSPRO Firebase project (brandonhall-7bdef) and adds the enquiry to the `enquiries` collection with source "Website" and status "new", using HOSPRO's own room and event IDs. If HOSPRO can't be reached, the visitor's email app opens with everything filled in, addressed to events@. Settings: `hospro` in `assets/js/venue-data.js`.
- **Page text:** edit the HTML directly, or edit `tools/build.py` and run `python3 tools/build.py` to regenerate every page with the shared header and footer.
- **Brochures and menus:** replace the PDFs in `/downloads` keeping the same file names.
- **Brand heading font:** add a licensed `kenao.woff2` to `assets/fonts/` and uncomment the Kenao rule at the top of `assets/css/site.css`. Until then Italiana is used.

## HOSPRO set-up (one-off)
1. Firebase console > Authentication > Sign-in method: make sure **Anonymous** is enabled (HOSPRO's events chat already uses it).
2. Firebase console > Authentication > Settings > Authorised domains: add `orngroup.github.io` and `www.brandonhallhotelandspa.com`.
3. If the web API key has HTTP-referrer restrictions in Google Cloud, add the same two domains.
4. Firestore rules: the current rule lets any signed-in user, including an anonymous website visitor, read every enquiry. Replace the enquiries, meta and marketing rules with `docs/firestore.rules.recommended` so the public can only create enquiries and only staff can read them.
5. Send a test enquiry from the live planner and check it appears in HOSPRO.

## Meeting photographs (one-off)
The six meeting photographs currently live on the WordPress site. Until they're copied here, the site shows them from there. To copy them in: GitHub > Actions > **Fetch meeting photos** > Run workflow. It downloads them into `assets/img/meetings` and commits them. Do this before the WordPress site is switched off.

## Stage status
Built: Home, Meetings & Events, Our event spaces, Event planner.
Holding pages (with downloads attached): Rooms & Suites, Dining, Weddings, Christmas, Spa & Leisure, Offers, Contact, Privacy, Accessibility.

## To confirm with the hotel
- Brandon 1 (54 m², 13.26 x 6.55 m) and Brandon 2 (76 m², 9.23 x 6.08 m): areas and dimensions don't match.
- Woodlands 2 length listed as 19.5 m in HOSPRO; drawn here at 9.5 m (half the suite).
- Wolston partition removed: can Wolston 1, 2 and 3 still be booked separately?
- Beech, Hunt and Warwick are hidden until they are ready to sell.
- Meeting room photographs are still needed.
