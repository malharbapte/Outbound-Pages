"""Builds samples/cards.html — three alternative stock card layouts for the Drive Away section.

Cards are shown at the artboard slide size (503.91 x 619.27) inside the bone band,
so each option can be judged exactly as it would sit on the homepage.
"""

CARDS = [
    ("AMAROO", "Couples", "stock-amaroo.png", "16'6\"", "3,300", "2,500", 2),
    ("HORNET", "Couples", "stock-hornet.png", "18'6\"", "3,500", "2,650", 2),
    ("SOLARA", "Couples", "stock-solara.png", "18'6\"", "3,500", "2,580", 2),
    ("HORNET", "Family", "stock-hornet.png", "20'6\"", "3,800", "2,950", 5),
]


def specs(atm, tare, length, sleeps):
    return [("ATM", f"{atm} kg"), ("Tare", f"{tare} kg"), ("Length", length), ("Sleeps", str(sleeps))]


def badge(name):
    return '<span class="badge">Composite</span>' if name == "SOLARA" else ""


# ---- Sample 1: Night Diamond ------------------------------------------------------------
def card_1(name, layout, img, length, atm, tare, sleeps):
    cells = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in specs(atm, tare, length, sleeps))
    return (f'<article class="card c1">{badge(name)}'
            f'<div class="media"><span class="diamond"></span><img src="../assets/{img}" alt=""></div>'
            f'<div class="body"><p class="layout">{layout} Layout</p><h3>{name}</h3>'
            f'<dl>{cells}</dl></div>'
            f'<a class="cta" href="#">View van</a></article>')


# ---- Sample 2: Spec Ticket ------------------------------------------------------------------
def card_2(name, layout, img, length, atm, tare, sleeps):
    rows = "".join(f'<div><dt>{k}</dt><span class="dots"></span><dd>{v}</dd></div>' for k, v in specs(atm, tare, length, sleeps))
    return (f'<article class="card c2">{badge(name)}'
            f'<p class="layout">{layout} Layout</p><h3>{name}</h3><span class="rule"></span>'
            f'<div class="media"><img src="../assets/{img}" alt=""></div>'
            f'<div class="perf"></div>'
            f'<dl>{rows}</dl>'
            f'<a class="cta" href="#">View van</a></article>')


# ---- Sample 3: Watermark Stats --------------------------------------------------------------
def card_3(name, layout, img, length, atm, tare, sleeps):
    stats = "".join(f"<div><dd>{v.replace(' kg', '<small>kg</small>')}</dd><dt>{k}</dt></div>" for k, v in specs(atm, tare, length, sleeps))
    return (f'<article class="card c3">{badge(name)}'
            f'<div class="media"><span class="watermark" aria-hidden="true">{name}</span><img src="../assets/{img}" alt="">'
            f'<span class="pill">{layout} Layout</span></div>'
            f'<div class="head"><h3>{name}</h3><a class="cta" href="#" aria-label="View {name.title()}"><span class="arrow"></span></a></div>'
            f'<dl>{stats}</dl></article>')


SAMPLES = [
    ("1", "Night Diamond", "Dark card with the brand diamond behind the van. Specs in a 2 × 2 grid, full-width green button.", card_1),
    ("2", "Spec Ticket", "Light, typographic card. Big name up top, a ticket-style tear line, and specs laid out like a spec sheet.", card_2),
    ("3", "Watermark Stats", "Model name as a large outline behind the van, layout tag on the photo, specs as bold numbers.", card_3),
]

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

html = open("cards_template.html").read().replace("{{SAMPLES}}", "".join(sections))
open("cards.html", "w").write(html)
print("samples/cards.html written")
