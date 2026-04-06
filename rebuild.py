#!/usr/bin/env python3
"""
Twilight Biathlon — Site Rebuild Script
Reads site-data.json and regenerates dynamic sections of HTML files.

Usage:
    python3 rebuild.py

Markers required in HTML files:
  index.html   : <!-- HOME-EVENTS-START --> / <!-- HOME-EVENTS-END -->
               : <!-- SCHEMA-START --> / <!-- SCHEMA-END -->
  events.html  : <!-- EVENTS-START --> / <!-- EVENTS-END -->
  results.html : <!-- RESULTS-START --> / <!-- RESULTS-END -->
  media.html   : <!-- PHOTOS-START --> / <!-- PHOTOS-END -->
"""

import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "site-data.json")


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def replace_between_markers(content, start_marker, end_marker, new_inner):
    """Replace everything between start_marker and end_marker (inclusive of markers)."""
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    replacement = f"{start_marker}\n{new_inner}\n        {end_marker}"
    result, count = pattern.subn(replacement, content)
    if count == 0:
        raise ValueError(f"Markers not found: {start_marker!r} ... {end_marker!r}")
    return result


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def he(text):
    """Minimal HTML entity escape for plain-text values."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# HTML generators
# ---------------------------------------------------------------------------

def build_event_card_home(ev):
    """Generate an event card for index.html (home page)."""
    lines = []
    lines.append('        <div class="event-card reveal">')
    lines.append(f'          <div class="event-date">{he(ev["date_display"])}</div>')
    lines.append('          <div class="event-details">')
    lines.append(f'            <span class="lbl">{he(ev["nv_day"])}</span>'
                 f'<span class="val">{he(ev["nv_divisions"])}</span>')
    lines.append(f'            <span class="lbl">{he(ev["wl_day"])}</span>'
                 f'<span class="val">{he(ev["wl_divisions"])}</span>')
    lines.append(f'            <span class="lbl">Check-in</span>'
                 f'<span class="val">{he(ev["checkin"])}</span>')
    lines.append(f'            <span class="lbl">Shooters meeting</span>'
                 f'<span class="val">{he(ev["shooters_meeting"])}</span>')
    lines.append(f'            <span class="lbl">First release</span>'
                 f'<span class="val">{he(ev["first_release"])}</span>')
    if ev.get("gates_open"):
        lines.append(f'            <span class="lbl">Gates open</span>'
                     f'<span class="val">{he(ev["gates_open"])}</span>')
    lines.append(f'            <span class="lbl">Registration</span>'
                 f'<span class="val">{he(ev["reg_window"])}</span>')
    lines.append(f'            <span class="lbl">Entry fee</span>'
                 f'<span class="val">{he(ev["entry_fee"])}</span>')
    payment_safe = (
        he(ev["payment_note"])
        .replace("NOT complete", "<strong>NOT complete</strong>")
    )
    lines.append(f'            <span class="lbl">Payment</span>'
                 f'<span class="val">{payment_safe}</span>')
    lines.append('          </div>')
    lines.append(f'          <a href="{he(ev["reg_url"])}" target="_blank" '
                 f'rel="noopener noreferrer" class="btn btn--primary">'
                 f'Register &mdash; {he(ev["name"])}</a>')
    lines.append('        </div>')
    return "\n".join(lines)


def build_event_card_events(ev):
    """Generate an event card for events.html (shows season in date line)."""
    season_label = ev["name"].upper() + " \u2014 " + ev["dates"].upper().replace("\u2013", "\u2013")
    lines = []
    lines.append(f'        <!-- {ev["name"].upper()} -->')
    lines.append('        <div class="event-card reveal">')
    lines.append(f'          <div class="event-date">{he(season_label)}</div>')
    lines.append('          <div class="event-details">')
    lines.append(f'            <span class="lbl">{he(ev["nv_day"])}</span>'
                 f'<span class="val">{he(ev["nv_divisions"])}</span>')
    lines.append(f'            <span class="lbl">{he(ev["wl_day"])}</span>'
                 f'<span class="val">{he(ev["wl_divisions"])}</span>')
    lines.append(f'            <span class="lbl">Check-in</span>'
                 f'<span class="val">{he(ev["checkin"])}</span>')
    lines.append(f'            <span class="lbl">Shooters meeting</span>'
                 f'<span class="val">{he(ev["shooters_meeting"])}</span>')
    lines.append(f'            <span class="lbl">First release</span>'
                 f'<span class="val">{he(ev["first_release"])}</span>')
    if ev.get("gates_open"):
        lines.append(f'            <span class="lbl">Gates open</span>'
                     f'<span class="val">{he(ev["gates_open"])}</span>')
    lines.append(f'            <span class="lbl">Registration</span>'
                 f'<span class="val">{he(ev["reg_window"])}</span>')
    lines.append(f'            <span class="lbl">Entry fee</span>'
                 f'<span class="val">{he(ev["entry_fee"])}</span>')
    payment_safe = (
        he(ev["payment_note"])
        .replace("NOT complete", "<strong>NOT complete</strong>")
    )
    lines.append(f'            <span class="lbl">Payment</span>'
                 f'<span class="val">{payment_safe}</span>')
    lines.append('          </div>')
    lines.append(f'          <a href="{he(ev["reg_url"])}" target="_blank" '
                 f'rel="noopener noreferrer" class="btn btn--primary">'
                 f'Register &mdash; {he(ev["name"])}</a>')
    lines.append('        </div>')
    return "\n".join(lines)


def build_results_list(results):
    """Generate the <ul class="results-list"> content."""
    lines = []
    lines.append('          <ul class="results-list reveal">')
    for r in results:
        name = r["name"]
        url = r.get("url", "")
        if url:
            lines.append(
                f'            <li><a href="{he(url)}" target="_blank" rel="noopener noreferrer">'
                f'<span class="results-arrow">&rarr;</span>{he(name)} Results'
                f'<span class="results-year">{he(name)}</span></a></li>'
            )
        else:
            lines.append(
                f'            <li><div class="results-tba">'
                f'<span class="results-arrow" style="color: var(--color-text-faint);">&rarr;</span>'
                f'{he(name)}<span class="results-year">{he(name)}</span></div></li>'
            )
    lines.append('          </ul>')
    return "\n".join(lines)


def build_photos_grid(photos):
    """Generate the photos grid and optional external gallery link."""
    lines = []
    external_url = photos.get("external_gallery_url", "")
    items = photos.get("items", [])

    if external_url:
        lines.append(
            f'        <div class="mb-6">'
            f'<a href="{he(external_url)}" target="_blank" rel="noopener noreferrer" '
            f'class="btn btn--primary">View Full Photo Gallery &rarr;</a></div>'
        )

    lines.append('        <div class="photos-grid mb-8">')
    for item in items:
        src = item.get("src", "")
        alt = item.get("alt", "")
        caption = item.get("caption", "")
        if src:
            cell = f'<img src="{he(src)}" alt="{he(alt)}" loading="lazy" style="width:100%;height:100%;object-fit:cover;">'
            if caption:
                cell += f'<div class="photo-caption" style="padding:var(--space-2);font-size:var(--text-xs);color:var(--color-text-muted);">{he(caption)}</div>'
            lines.append(f'          <div class="photo-cell">{cell}</div>')
        else:
            lines.append(
                f'          <div class="photo-cell"><div class="photo-placeholder">{he(alt)}</div></div>'
            )
    lines.append('        </div>')
    return "\n".join(lines)


def build_schema_json(events):
    """Generate schema.org/Event JSON-LD array for all events."""
    schema_events = []

    # Map event id to time offset and start time
    time_info = {
        "spring-2026": ("T22:00:00-05:00", "T23:59:00-05:00"),
        "fall-2026":   ("T20:30:00-05:00", "T23:59:00-05:00"),
    }

    for ev in events:
        eid = ev.get("id", "")
        start_suffix, end_suffix = time_info.get(eid, ("T21:00:00-05:00", "T23:59:00-05:00"))
        start_date = ev["start_date"] + start_suffix
        end_date = ev["end_date"] + end_suffix

        avail = "https://schema.org/InStock" if ev.get("reg_status") == "open" else "https://schema.org/SoldOut"

        schema_ev = {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": f"Twilight Biathlon \u2014 {ev['name']}",
            "description": "Nighttime 5K run-and-gun biathlon with 4 live-fire shooting stages. NV divisions Friday, white-light divisions Saturday.",
            "startDate": start_date,
            "endDate": end_date,
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": {
                "@type": "Place",
                "name": "The Burial Mound Shooting Center",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "42251 S 34500 Rd",
                    "addressLocality": "Pawnee",
                    "addressRegion": "OK",
                    "postalCode": "74058",
                    "addressCountry": "US",
                },
            },
            "organizer": {
                "@type": "Organization",
                "name": "Oklahoma Multi-Gun",
                "email": "OkMultiGun@gmail.com",
            },
            "offers": {
                "@type": "Offer",
                "price": "100.00",
                "priceCurrency": "USD",
                "url": ev["reg_url"],
                "availability": avail,
            },
        }
        schema_events.append(schema_ev)

    json_str = json.dumps(schema_events, indent=4, ensure_ascii=False)
    # Indent entire block by 2 spaces to match existing style
    indented = "\n".join("  " + line for line in json_str.splitlines())
    return f'  <script type="application/ld+json">\n{indented}\n  </script>'


# ---------------------------------------------------------------------------
# File updaters
# ---------------------------------------------------------------------------

def update_index(data):
    path = os.path.join(BASE_DIR, "index.html")
    content = read_file(path)

    # Home event cards
    home_events = [ev for ev in data["events"] if ev.get("show_on_home", False)]
    home_cards = "\n\n".join(build_event_card_home(ev) for ev in home_events)
    content = replace_between_markers(
        content,
        "<!-- HOME-EVENTS-START -->",
        "<!-- HOME-EVENTS-END -->",
        home_cards,
    )

    # Schema JSON-LD — replace the entire script block between markers
    schema_html = build_schema_json(data["events"])
    # Replace between SCHEMA-START and SCHEMA-END (markers stay, content replaced)
    schema_pattern = re.compile(
        r"(<!-- SCHEMA-START -->).*?(<!-- SCHEMA-END -->)",
        re.DOTALL,
    )
    content = schema_pattern.sub(r"\1\n  " + schema_html + r"\n  \2", content)

    write_file(path, content)
    return "index.html: updated home event cards and schema JSON-LD"


def update_events(data):
    path = os.path.join(BASE_DIR, "events.html")
    content = read_file(path)

    cards = "\n\n".join(build_event_card_events(ev) for ev in data["events"])
    content = replace_between_markers(
        content,
        "<!-- EVENTS-START -->",
        "<!-- EVENTS-END -->",
        cards,
    )

    write_file(path, content)
    return "events.html: updated event cards"


def update_results(data):
    path = os.path.join(BASE_DIR, "results.html")
    content = read_file(path)

    results_html = build_results_list(data["results"])
    content = replace_between_markers(
        content,
        "<!-- RESULTS-START -->",
        "<!-- RESULTS-END -->",
        results_html,
    )

    write_file(path, content)
    return "results.html: updated results list"


def update_media(data):
    path = os.path.join(BASE_DIR, "media.html")
    content = read_file(path)

    photos_html = build_photos_grid(data["photos"])
    content = replace_between_markers(
        content,
        "<!-- PHOTOS-START -->",
        "<!-- PHOTOS-END -->",
        photos_html,
    )

    write_file(path, content)
    return "media.html: updated photos grid"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not os.path.exists(DATA_FILE):
        print(f"ERROR: {DATA_FILE} not found", file=sys.stderr)
        sys.exit(1)

    data = load_data()
    print("Loaded site-data.json")

    updaters = [update_index, update_events, update_results, update_media]
    for fn in updaters:
        try:
            msg = fn(data)
            print(f"  OK  {msg}")
        except Exception as e:
            print(f"  ERR {fn.__name__}: {e}", file=sys.stderr)

    print("\nRebuild complete.")


if __name__ == "__main__":
    main()
