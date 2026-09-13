"""Builds samples/specs.html — three ways to show the spec hierarchy ATM > Tare > Sleeps > Length
on the Night Diamond card (as used on the homepage). Reuses the shell of cards_template.html.
"""

CARDS = [
    ("AMAROO", "Couples", "stock-amaroo.png", "16'6\"", "3,300", "2,500", 2),
    ("HORNET", "Couples", "stock-hornet.png", "18'6\"", "3,500", "2,650", 2),
    ("SOLARA", "Couples", "stock-solara.png", "18'6\"", "3,500", "2,580", 2),
    ("HORNET", "Family", "stock-hornet.png", "20'6\"", "3,800", "2,950", 5),
]


def shell(name, layout, img, specs_html, variant):
    badge = '<span class="badge">Composite</span>' if name == "SOLARA" else ""
    return (f'<a class="card nd {variant}" href="#">{badge}'
            f'<div class="media"><span class="diamond"></span><img src="../assets/{img}" alt=""></div>'
            f'<div class="body"><p class="layout">{layout} Layout</p><h3>{name}</h3>{specs_html}</div></a>')


def kg(v):
    return f'{v}<small>kg</small>'


# A — Lead & support: ATM is the headline figure, Tare sits beside it, Sleeps/Length are a footnote.
def sample_a(name, layout, img, length, atm, tare, sleeps):
    specs = (f'<div class="primary">'
             f'<div class="atm"><dt>ATM</dt><dd>{kg(atm)}</dd></div>'
             f'<div class="tare"><dt>Tare</dt><dd>{kg(tare)}</dd></div></div>'
             f'<p class="minor"><span>Sleeps {sleeps}</span><span>{length}</span></p>')
    return shell(name, layout, img, f'<dl>{specs}</dl>', "sa")


# B — Stepped scale: one row, each figure a step smaller and quieter than the one before.
def sample_b(name, layout, img, length, atm, tare, sleeps):
    cells = "".join(f'<div class="s{i}"><dt>{k}</dt><dd>{v}</dd></div>' for i, (k, v) in
                    enumerate([("ATM", kg(atm)), ("Tare", kg(tare)), ("Sleeps", sleeps), ("Length", length)], 1))
    return shell(name, layout, img, f'<dl>{cells}</dl>', "sb")


# C — Colour block: ATM gets the brand green panel, Tare is plain, Sleeps/Length are small tags.
def sample_c(name, layout, img, length, atm, tare, sleeps):
    specs = (f'<div class="weights">'
             f'<div class="atm"><dt>ATM</dt><dd>{kg(atm)}</dd></div>'
             f'<div class="tare"><dt>Tare</dt><dd>{kg(tare)}</dd></div></div>'
             f'<div class="tags"><span><b>Sleeps</b> {sleeps}</span><span><b>Length</b> {length}</span></div>')
    return shell(name, layout, img, f'<dl>{specs}</dl>', "sc")


SAMPLES = [
    ("A", "Lead &amp; Support", "ATM is the biggest number on the card. Tare sits beside it, smaller. Sleeps and Length drop to a quiet line underneath.", sample_a),
    ("B", "Stepped Scale", "All four in one row, read left to right. Each figure is a step smaller and lighter than the one before it.", sample_b),
    ("C", "Colour Block", "ATM gets the green panel so it's seen first. Tare stays plain white text. Sleeps and Length become small tags.", sample_c),
]

EXTRA_CSS = """
  /* Night Diamond base, matching the homepage card (no CTA, larger van). */
  .nd { display: flex; flex-direction: column; background: var(--black); color: var(--bone); transition: transform .3s ease, box-shadow .3s ease; }
  .nd:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(11, 10, 7, .25); }
  .nd .media { position: relative; height: 340px; display: flex; align-items: flex-end; justify-content: center; padding: 0 14px 22px; }
  .nd .diamond { position: absolute; left: 50%; top: 50%; width: 250px; height: 250px; background: var(--olive); opacity: .55; transform: translate(-50%, -54%) rotate(45deg); transition: transform .5s ease; }
  .nd:hover .diamond { transform: translate(-50%, -54%) rotate(135deg); }
  .nd .media img { position: relative; }
  .nd .body { flex: 1; display: flex; flex-direction: column; padding: 8px 30px 26px; }
  .nd .layout { display: flex; align-items: center; gap: 12px; font: 600 18px/1 var(--poppins); letter-spacing: .14em; text-transform: uppercase; color: var(--green); }
  .nd .layout::before { content: ""; width: 12px; height: 12px; background: var(--green); transform: rotate(45deg); }
  .nd h3 { margin-top: 10px; font: 700 60px/1 var(--oswald); letter-spacing: .01em; }
  .nd dl { margin-top: auto; }
  .nd dt { font: 400 15px/1 var(--poppins); letter-spacing: .1em; text-transform: uppercase; color: var(--silver); }
  .nd dd { font-family: var(--oswald); font-weight: 500; line-height: 1; white-space: nowrap; }
  .nd dd small { font: 500 .42em var(--poppins); margin-left: 5px; letter-spacing: .02em; }
  .line { border-color: rgba(244, 241, 234, .18); }

  /* A — Lead & Support */
  .sa .primary { display: grid; grid-template-columns: 1.25fr 1fr; align-items: end; border-top: 1px solid rgba(244, 241, 234, .18); padding-top: 16px; }
  .sa .atm dd { margin-top: 8px; font-size: 58px; color: var(--bone); }
  .sa .atm dt { color: var(--green); font-weight: 600; }
  .sa .tare { padding-left: 22px; border-left: 1px solid rgba(244, 241, 234, .18); }
  .sa .tare dd { margin-top: 8px; font-size: 36px; color: var(--bone); }
  .sa .minor { display: flex; gap: 22px; margin-top: 14px; font: 400 19px/1 var(--poppins); color: var(--silver); }
  .sa .minor span + span::before { content: ""; display: inline-block; width: 7px; height: 7px; background: var(--grey); transform: translateY(-3px) rotate(45deg); margin-right: 22px; }

  /* B — Stepped Scale */
  .sb dl { display: grid; grid-template-columns: 1.5fr 1.2fr .72fr .88fr; align-items: end; border-top: 1px solid rgba(244, 241, 234, .18); padding-top: 18px; }
  .sb dl div + div { padding-left: 12px; }
  .sb dd { margin-top: 8px; }
  .sb .s1 dt { color: var(--green); font-weight: 600; }
  .sb .s1 dd { font-size: 48px; color: var(--bone); }
  .sb .s2 dd { font-size: 36px; color: var(--bone); }
  .sb .s3 dd { font-size: 28px; color: #c9c5bb; }
  .sb .s4 dd { font-size: 24px; color: var(--silver); }
  .sb .s3 dt, .sb .s4 dt { font-size: 13px; color: var(--grey); }
  .sb .s1 { position: relative; }
  .sb .s1::after { content: ""; position: absolute; left: 0; bottom: -14px; width: 56px; height: 5px; background: var(--green); }

  /* C — Colour Block */
  .sc .weights { display: grid; grid-template-columns: 1.3fr 1fr; align-items: stretch; margin: 0 -30px; }
  .sc .atm { background: var(--green); padding: 14px 30px 16px; }
  .sc .atm dt { color: var(--bone); font-weight: 600; opacity: .85; }
  .sc .atm dd { margin-top: 8px; font-size: 52px; color: var(--bone); }
  .sc .tare { padding: 14px 30px 16px 24px; display: flex; flex-direction: column; justify-content: flex-end; }
  .sc .tare dd { margin-top: 8px; font-size: 34px; color: var(--bone); }
  .sc .tags { display: flex; gap: 12px; margin-top: 16px; }
  .sc .tags span { font: 500 18px/1 var(--poppins); color: var(--bone); padding: 9px 14px; border: 1px solid rgba(244, 241, 234, .25); }
  .sc .tags b { font-weight: 400; color: var(--silver); text-transform: uppercase; letter-spacing: .08em; font-size: 14px; margin-right: 6px; }
  .sc .body { padding-bottom: 22px; }
"""

sections = []
for num, title, desc, fn in SAMPLES:
    cards = "".join(fn(*c) for c in CARDS)
    sections.append(f'''
  <section class="sample">
    <div class="intro">
      <span class="num">{num}</span>
      <div><h2>{title}</h2><p>{desc}</p></div>
    </div>
    <div class="band">
      <div class="track">{cards}</div>
      <div class="progress"><span></span></div>
    </div>
  </section>''')

html = open("cards_template.html").read()
html = html.replace("<title>Drive Away card samples | Outbound RVs</title>", "<title>Spec hierarchy samples | Outbound RVs</title>")
html = html.replace("<h1>DRIVE AWAY — CARD SAMPLES</h1>", "<h1>SPEC HIERARCHY — SAMPLES</h1>")
html = html.replace("Three layout options for the stock cards, shown at the homepage size. Hover a card to see its interaction.",
                    "ATM &gt; Tare &gt; Sleeps &gt; Length. Three ways to make that order obvious at a glance, on the Night Diamond card.")
html = html.replace("</style>", EXTRA_CSS + "</style>")
html = html.replace("{{SAMPLES}}", "".join(sections))
open("specs.html", "w").write(html)
print("samples/specs.html written")
