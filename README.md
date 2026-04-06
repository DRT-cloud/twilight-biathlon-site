# Twilight Biathlon Website

## How to Update Content

All dynamic content is managed through `site-data.json`. Edit that file, then run the rebuild script to regenerate the HTML pages. You never need to touch the HTML directly for routine updates.

---

## site-data.json Structure

### Adding/Removing Events

Events live in the `"events"` array. Each event has these fields:

| Field | Description |
|---|---|
| `id` | Unique slug, e.g. `"spring-2026"`. Used internally — no spaces. |
| `name` | Human-readable name, e.g. `"Spring 2026"` |
| `dates` | Display dates, e.g. `"May 15–16, 2026"` |
| `date_display` | ALL-CAPS version for the event card header, e.g. `"MAY 15–16, 2026"` |
| `start_date` | ISO date `"YYYY-MM-DD"` — used in schema.org markup |
| `end_date` | ISO date `"YYYY-MM-DD"` — used in schema.org markup |
| `nv_day` | Label for Friday NV line, e.g. `"Friday, May 15"` |
| `nv_divisions` | Value for Friday NV line, e.g. `"NV 2Gun / NV PCC — Night Vision Only"` |
| `wl_day` | Label for Saturday WL line, e.g. `"Saturday, May 16"` |
| `wl_divisions` | Value for Saturday WL line, e.g. `"2Gun / PCC — White Light"` |
| `checkin` | Check-in window, e.g. `"7:00–8:00 PM each night"` |
| `shooters_meeting` | Shooters meeting time |
| `first_release` | First competitor release time |
| `gates_open` | Gates open time. Leave `""` to omit this row from the card. |
| `reg_window` | Registration open/close text |
| `entry_fee` | Entry fee text |
| `payment_note` | Payment instructions (shown verbatim — use plain text) |
| `reg_url` | Full PractiScore registration URL |
| `reg_status` | `"open"` or `"closed"` — controls schema.org availability |
| `show_on_home` | `true` to show on home page, `false` for events.html only |

**To add a new event**, copy an existing event object and update all fields. Add it to the array in chronological order.

**To remove an event**, delete the entire `{ ... }` object for that event from the array.

**To close registration**, change `"reg_status"` to `"closed"` and optionally remove or clear the `reg_url`.

---

### Adding Results Links

Results live in the `"results"` array. Each entry has:

```json
{ "name": "Spring 2026", "url": "https://practiscore.com/results/..." }
```

- **With a URL**: displays as a clickable link labeled `"{name} Results"`.
- **Empty URL** (`"url": ""`): displays as a greyed-out placeholder labeled `"{name}"` — useful for future events.

**To add a result**, find the entry with the matching name and paste in the PractiScore results URL.

**To add a future placeholder**, append a new entry with an empty `url`:

```json
{ "name": "Spring 2028", "url": "" }
```

Results display in array order — keep them chronological.

---

### Adding Photos

Photos are managed in the `"photos"` object with two options:

#### Option 1 — External Gallery Link

Set `external_gallery_url` to point to a hosted gallery (Google Photos, SmugMug, Flickr, etc.):

```json
"photos": {
  "external_gallery_url": "https://photos.google.com/your-album",
  ...
}
```

This adds a prominent "View Full Photo Gallery" button at the top of the Photos page.

#### Option 2 — Individual Photos Grid

Add photo items to the `"items"` array:

```json
{ "src": "/photos/event-2026.jpg", "alt": "Competitor at stage 2", "caption": "Spring 2026 — Stage 2" }
```

- `src`: Path or URL to the image. Local paths like `/photos/img.jpg` work if the image is deployed with the site.
- `alt`: Descriptive alt text for accessibility and SEO.
- `caption`: Optional caption displayed below the image. Leave `""` to omit.

If `src` is empty, the item displays as a placeholder cell. This lets you reserve grid positions.

Both options can be used together: set `external_gallery_url` for a "View All" link and put select photos in `items` for the on-page grid.

---

## Running the Rebuild

After editing `site-data.json`, regenerate the HTML:

```bash
python3 rebuild.py
```

The script updates these files:
- `index.html` — Upcoming Events section + schema.org JSON-LD
- `events.html` — Event cards section
- `results.html` — Results list
- `media.html` — Photos grid and external gallery link

Then deploy the updated files as normal.

---

## File Overview

```
twilight-biathlon/
├── site-data.json      ← Edit this to update all dynamic content
├── rebuild.py          ← Run after editing site-data.json
├── index.html          ← Home page
├── events.html         ← Upcoming events
├── results.html        ← Past results
├── media.html          ← Photos
├── faq.html            ← FAQ
├── first-timer.html    ← First-timer guide
├── what-is-run-and-gun.html
├── night-vision-division.html
├── rules.html
├── register.html
├── location.html
├── contact.html
├── robots.txt
├── sitemap.xml         ← Update when adding pages
├── base.css            ← Base styles (do not edit)
├── style.css           ← Site styles (do not edit for content changes)
└── app.js              ← Site JS (do not edit for content changes)
```

---

## Deployment

This is a static site. Deploy all files to any web host (Netlify, Cloudflare Pages, GitHub Pages, etc.). No server-side processing required.
