"""Builds samples/thirds.html — Night Diamond card laid out on a rule-of-thirds grid,
three ways, keeping the spec hierarchy ATM > Tare > Sleeps > Length.

Card: 503.91 x 619.27  ->  columns every 167.97, rows every 206.42.
"""

CARDS = [
    ("AMAROO", "Couples", "stock-amaroo.png", "16'6\"", "3,300", "2,500", 2),
    ("HORNET", "Couples", "stock-hornet.png", "18'6\"", "3,500", "2,650", 2),
    ("SOLARA", "Couples", "stock-solara.png", "18'6\"", "3,500", "2,580", 2),
    ("HORNET", "Family", "stock-hornet.png", "20'6\"", "3,800", "2,950", 5),
]


def kg(v):
    return f'{v}<small>kg</small>'


def badge(name):
    return '<span class="badge">Composite</span>' if name == "SOLARA" else ""


def media(img):
    return f'<div class="media"><span class="diamond"></span><img src="../assets/{img}" alt=""></div>'


def spec(cls, label, value):
    return f'<div class="{cls}"><dt>{label}</dt><dd>{value}</dd></div>'


# 1 — Three Bands: name / van / specs, one third each. ATM takes the top two-thirds of the
#     spec band; Tare, Sleeps and Length share the last third.
def t1(name, layout, img, length, atm, tare, sleeps):
    return (f'<a class="card nd t1" href="#">{badge(name)}'
            f'<div class="head"><p class="layout">{layout} Layout</p><h3>{name}</h3></div>'
            f'{media(img)}'
            f'<dl class="specs">{spec("atm", "ATM", kg(atm))}'
            f'<div class="row">{spec("tare", "Tare", kg(tare))}{spec("sleeps", "Sleeps", sleeps)}{spec("length", "Length", length)}</div></dl>'
            f'<span class="grid" aria-hidden="true"></span></a>')


# 2 — Power Point: the van fills the top two-thirds and bleeds off the right edge, with the diamond
#     on the upper-right intersection. ATM owns two-thirds of the bottom band; Tare, Sleeps and
#     Length stack in the last third.
def t2(name, layout, img, length, atm, tare, sleeps):
    return (f'<a class="card nd t2" href="#">{badge(name)}'
            f'{media(img)}'
            f'<div class="head"><p class="layout">{layout} Layout</p><h3>{name}</h3></div>'
            f'<dl class="specs">{spec("atm", "ATM", kg(atm))}'
            f'<div class="side">{spec("tare", "Tare", kg(tare))}<p class="minor"><span>Sleeps {sleeps}</span><span>{length}</span></p></div></dl>'
            f'<span class="grid" aria-hidden="true"></span></a>')


# 3 — Side Third: a spec column runs down the right third. ATM sits alone at the top,
#     Tare > Sleeps > Length step down at the bottom; the van crosses the middle band.
def t3(name, layout, img, length, atm, tare, sleeps):
    return (f'<a class="card nd t3" href="#">{badge(name)}'
            f'<span class="rail"></span>'
            f'<dl class="specs">{spec("atm", "ATM", kg(atm))}'
            f'<div class="lower">{spec("tare", "Tare", kg(tare))}{spec("sleeps", "Sleeps", sleeps)}{spec("length", "Length", length)}</div></dl>'
            f'{media(img)}'
            f'<div class="head"><p class="layout">{layout} Layout</p><h3>{name}</h3></div>'
            f'<span class="grid" aria-hidden="true"></span></a>')


SAMPLES = [
    ("1", "Three Bands", "The card is split into three equal rows: name, van, specs. In the spec row, ATM takes the top two-thirds. Tare, Sleeps and Length share the last third, each smaller than the one before.", t1),
    ("2", "Power Point", "The van fills the top two-thirds and runs off the right edge, with the diamond on a grid crossing. ATM takes two-thirds of the bottom row, and the last third holds Tare, then Sleeps and Length.", t2),
    ("3", "Side Third", "A spec column runs down the right third of the card. ATM sits alone at the top, and Tare, Sleeps and Length step down at the bottom. The van crosses the middle row, and the name sits bottom-left.", t3),
]

EXTRA_CSS = """
  /* Night Diamond base */
  .nd { display: block; background: var(--black); color: var(--bone); transition: transform .3s ease, box-shadow .3s ease; }
  .nd:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(11, 10, 7, .25); }
  .nd > * { position: absolute; }
  .nd .media { display: flex; align-items: flex-end; justify-content: center; }
  .nd .diamond { position: absolute; background: var(--olive); opacity: .55; transform: translate(-50%, -50%) rotate(45deg); transition: transform .5s ease; }
  .nd:hover .diamond { transform: translate(-50%, -50%) rotate(135deg); }
  .nd .media img { position: relative; z-index: 1; }
  .nd .layout { display: flex; align-items: center; gap: 12px; font: 600 18px/1 var(--poppins); letter-spacing: .14em; text-transform: uppercase; color: var(--green); }
  .nd .layout::before { content: ""; width: 12px; height: 12px; background: var(--green); transform: rotate(45deg); }
  .nd h3 { font: 700 64px/1 var(--oswald); letter-spacing: .01em; }
  .nd dl { margin: 0; }
  .nd dt { font: 400 14px/1 var(--poppins); letter-spacing: .1em; text-transform: uppercase; color: var(--silver); }
  .nd dd { font-family: var(--oswald); font-weight: 500; line-height: 1; white-space: nowrap; color: var(--bone); }
  .nd dd small { font: 500 .36em var(--poppins); margin-left: 5px; letter-spacing: .02em; }
  .nd .atm dt { color: var(--green); font-weight: 600; font-size: 16px; }
  .nd .badge { z-index: 5; }
  .hair { border-color: rgba(244, 241, 234, .16); }

  /* Thirds overlay */
  .nd .grid { inset: 0; z-index: 6; pointer-events: none; opacity: 0; transition: opacity .25s;
    background:
      linear-gradient(to right, transparent calc(33.333% - 1px), rgba(238,150,75,.9) calc(33.333% - 1px), rgba(238,150,75,.9) calc(33.333% + 1px), transparent calc(33.333% + 1px),
                                transparent calc(66.666% - 1px), rgba(238,150,75,.9) calc(66.666% - 1px), rgba(238,150,75,.9) calc(66.666% + 1px), transparent calc(66.666% + 1px)),
      linear-gradient(to bottom, transparent calc(33.333% - 1px), rgba(238,150,75,.9) calc(33.333% - 1px), rgba(238,150,75,.9) calc(33.333% + 1px), transparent calc(33.333% + 1px),
                                 transparent calc(66.666% - 1px), rgba(238,150,75,.9) calc(66.666% - 1px), rgba(238,150,75,.9) calc(66.666% + 1px), transparent calc(66.666% + 1px)); }
  body.show-grid .nd .grid { opacity: 1; }
  .grid-toggle { position: fixed; right: 24px; bottom: 24px; z-index: 50; font: 600 14px/1 var(--poppins); letter-spacing: .06em; text-transform: uppercase;
                 background: var(--black); color: var(--bone); border: 0; padding: 14px 18px; cursor: pointer; display: flex; align-items: center; gap: 10px; }
  .grid-toggle::before { content: ""; width: 10px; height: 10px; border: 2px solid var(--orange); transform: rotate(45deg); }
  body.show-grid .grid-toggle::before { background: var(--orange); }

  /* ---- 1. Three Bands --------------------------------------------------------------- */
  .t1 .head { left: 30px; right: 30px; top: 0; height: 206.42px; display: flex; flex-direction: column; justify-content: flex-end; padding-bottom: 22px; }
  .t1 .head h3 { margin-top: 12px; font-size: 72px; }
  .t1 .media { left: 0; right: 0; top: 206.42px; height: 206.42px; padding: 0 16px 12px; }
  .t1 .diamond { left: 50%; top: 50%; width: 180px; height: 180px; }
  .t1 .specs { left: 0; right: 0; top: 412.84px; height: 206.43px; display: flex; flex-direction: column; border-top: 1px solid rgba(244, 241, 234, .16); }
  .t1 .atm { height: 137.62px; padding: 0 30px; display: flex; align-items: center; justify-content: space-between; }
  .t1 .atm dd { font-size: 76px; }
  .t1 .row { flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid rgba(244, 241, 234, .16); }
  .t1 .row > div { padding: 12px 0 0 30px; }
  .t1 .row > div + div { border-left: 1px solid rgba(244, 241, 234, .16); padding-left: 20px; }
  .t1 .row dt { font-size: 12px; }
  .t1 .row dd { margin-top: 7px; }
  .t1 .tare dd { font-size: 28px; }
  .t1 .sleeps dd { font-size: 23px; color: #cfcac0; }
  .t1 .length dd { font-size: 20px; color: var(--silver); }

  /* ---- 2. Power Point --------------------------------------------------------------- */
  .t2 .media { left: 0; right: -70px; top: 0; height: 412.84px; padding: 0 0 124px 22px; justify-content: flex-start; }
  .t2 .media img { width: auto; max-width: none; height: 205px; }
  .t2 .diamond { left: 335.94px; top: 206.42px; width: 250px; height: 250px; }
  .t2 .head { left: 30px; top: 296px; z-index: 2; }
  .t2 .head h3 { margin-top: 10px; }
  .t2 .specs { left: 0; right: 0; top: 412.84px; bottom: 0; display: grid; grid-template-columns: 335.94px 1fr; border-top: 1px solid rgba(244, 241, 234, .16); }
  .t2 .atm { padding: 34px 0 0 30px; }
  .t2 .atm dd { margin-top: 12px; font-size: 88px; }
  .t2 .side { padding: 34px 0 0 22px; border-left: 1px solid rgba(244, 241, 234, .16); }
  .t2 .tare dd { margin-top: 10px; font-size: 38px; }
  .t2 .minor { margin-top: 22px; padding-top: 16px; border-top: 1px solid rgba(244, 241, 234, .16); display: flex; flex-direction: column; gap: 10px; }
  .t2 .minor span:first-child { font: 500 21px/1 var(--poppins); color: #cfcac0; }
  .t2 .minor span:last-child { font: 400 18px/1 var(--poppins); color: var(--silver); }

  /* ---- 3. Side Third ---------------------------------------------------------------- */
  .t3 .rail { right: 0; top: 0; bottom: 0; width: 167.97px; background: rgba(244, 241, 234, .06); border-left: 1px solid rgba(244, 241, 234, .14); }
  .t3 .specs { right: 0; top: 0; bottom: 0; width: 167.97px; z-index: 2; }
  .t3 .atm { position: absolute; left: 0; right: 0; top: 0; height: 206.42px; padding: 0 16px 0 20px; display: flex; flex-direction: column; justify-content: center; }
  .t3 .atm dd { margin-top: 10px; font-size: 50px; }
  .t3 .atm dd small { display: block; margin: 6px 0 0; font-size: 16px; color: var(--silver); }
  .t3 .lower { position: absolute; left: 0; right: 0; top: 412.84px; bottom: 0; padding: 0 16px 0 20px; display: flex; flex-direction: column; justify-content: center; gap: 16px; }
  .t3 .lower dd { margin-top: 5px; }
  .t3 .lower dt { font-size: 12px; }
  .t3 .tare dd { font-size: 32px; }
  .t3 .tare dd small { font-size: 13px; }
  .t3 .sleeps dd { font-size: 25px; color: #cfcac0; }
  .t3 .length dd { font-size: 21px; color: var(--silver); }
  .t3 .media { left: 0; right: 0; top: 206.42px; height: 206.42px; padding: 0 10px 8px; z-index: 3; }
  .t3 .diamond { left: 167.97px; top: 0; width: 210px; height: 210px; z-index: 0; }
  .t3 .media img { filter: drop-shadow(0 10px 14px rgba(0, 0, 0, .5)); }
  .t3 .head { left: 30px; bottom: 40px; z-index: 2; }
  .t3 .head h3 { margin-top: 12px; font-size: 76px; }
  .t3 .badge { right: auto; left: 0; padding: 10px 38px 10px 20px; clip-path: polygon(0 0, 100% 0, calc(100% - 20px) 50%, 100% 100%, 0 100%); }
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
html = html.replace("<title>Drive Away card samples | Outbound RVs</title>", "<title>Rule of thirds card samples | Outbound RVs</title>")
html = html.replace("<h1>DRIVE AWAY — CARD SAMPLES</h1>", "<h1>RULE OF THIRDS — CARD SAMPLES</h1>")
html = html.replace("Three layout options for the stock cards, shown at the homepage size. Hover a card to see its interaction.",
                    "Each card sits on a 3 × 3 grid, with the specs in the order ATM &gt; Tare &gt; Sleeps &gt; Length. Use the button at the bottom right to show the grid.")
html = html.replace("</style>", EXTRA_CSS + "</style>")
html = html.replace("{{SAMPLES}}", "".join(sections))
html = html.replace('<main class="page" id="page">',
                    '<button class="grid-toggle" type="button" onclick="document.body.classList.toggle(\'show-grid\')">Show thirds grid</button>\n<main class="page" id="page">')
open("thirds.html", "w").write(html)
print("samples/thirds.html written")
