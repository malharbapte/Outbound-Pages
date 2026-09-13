"""Builds samples/side-landscape.html — landscape (4:3) stock card with the photo and name in the left
two-thirds and the specs in the right third, laid out on a rule-of-thirds grid.

Card: 825.69 x 619.27 (4:3)  ->  columns every 275.23, rows every 206.42.
Photos are placeholders (range shots with backgrounds) until the interior images are supplied.
"""

CARDS = [
    ("AMAROO", "Couples", "range-amaroo.jpg", "50% 62%", "16'6\"", "3,300", "2,500", 2),
    ("HORNET", "Couples", "range-hornet.jpg", "50% 64%", "18'6\"", "3,500", "2,650", 2),
    ("SOLARA", "Couples", "range-solara.jpg", "45% 70%", "18'6\"", "3,500", "2,580", 2),
    ("XTR", "Family", "range-xtr.jpg", "40% 60%", "20'6\"", "3,800", "2,950", 5),
]


def card(name, layout, img, focus, length, atm, tare, sleeps):
    badge = '<span class="badge">Composite</span>' if name == "SOLARA" else ""
    return (f'<a class="card side" href="#">'
            f'<div class="photo"><img src="../assets/{img}" alt="" style="object-position:{focus}">{badge}'
            f'<div class="title"><p class="layout">{layout} Layout</p><h3>{name}</h3></div></div>'
            f'<dl class="rail">'
            f'<div class="row r1"><div class="atm"><dt>ATM</dt><dd>{atm}<small>kg</small></dd></div></div>'
            f'<div class="row r2"><div class="tare"><dt>Tare</dt><dd>{tare}<small>kg</small></dd></div></div>'
            f'<div class="row r3"><div class="sleeps"><dt>Sleeps</dt><dd>{sleeps}</dd></div>'
            f'<div class="length"><dt>Length</dt><dd>{length}</dd></div></div>'
            f'</dl><span class="grid" aria-hidden="true"></span></a>')


EXTRA_CSS = """
  .band { height: 832.44px; }
  .track { padding-top: 106.57px; gap: 48px; }

  .side { width: 825.69px; height: 619.27px; display: grid; grid-template-columns: 550.46px 275.23px; background: var(--black); color: var(--bone);
          transition: transform .3s ease, box-shadow .3s ease; }
  .side:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(11, 10, 7, .25); }

  /* Left two-thirds: photo as large as possible, name in the lower third */
  .side .photo { position: relative; overflow: hidden; }
  .side .photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transition: transform .6s ease; }
  .side:hover .photo img { transform: scale(1.05); }
  .side .photo::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 55%; background: linear-gradient(to bottom, rgba(11, 10, 7, 0), rgba(11, 10, 7, .88)); }
  .side .title { position: absolute; left: 34px; right: 24px; top: 412.85px; bottom: 0; z-index: 1; display: flex; flex-direction: column; justify-content: center; }
  .side .layout { display: flex; align-items: center; gap: 12px; font: 600 18px/1 var(--poppins); letter-spacing: .14em; text-transform: uppercase; color: var(--bone); }
  .side .layout::before { content: ""; width: 12px; height: 12px; background: var(--green); transform: rotate(45deg); }
  .side h3 { margin-top: 12px; font: 700 80px/1 var(--oswald); letter-spacing: .01em; color: #fff; }
  .side .badge { top: 26px; right: auto; left: 0; padding: 10px 38px 10px 22px; clip-path: polygon(0 0, 100% 0, calc(100% - 20px) 50%, 100% 100%, 0 100%); }

  /* Right third: specs, one thirds-row each — ATM, then Tare, then Sleeps + Length side by side */
  .side .rail { margin: 0; display: grid; grid-template-rows: repeat(3, 206.42px); }
  .side .row { padding: 0 24px 0 30px; display: flex; flex-direction: column; justify-content: center; }
  .side .row + .row { border-top: 1px solid rgba(244, 241, 234, .16); }
  .side dt { font: 400 14px/1 var(--poppins); letter-spacing: .12em; text-transform: uppercase; color: var(--silver); }
  .side dd { margin: 10px 0 0; font-family: var(--oswald); font-weight: 500; line-height: 1; white-space: nowrap; color: var(--bone); }
  .side dd small { margin-left: 6px; font: 500 .3em/1 var(--poppins); letter-spacing: .04em; color: var(--silver); }
  .side .atm dt { font-size: 16px; font-weight: 600; color: var(--green); }
  .side .atm dd { font-size: 70px; }
  .side .r1 { background: rgba(139, 155, 77, .12); }
  .side .tare dd { font-size: 50px; }
  .side .r3 { flex-direction: row; align-items: center; justify-content: flex-start; gap: 0; }
  .side .r3 > div { flex: 1; }
  .side .length { padding-left: 22px; border-left: 1px solid rgba(244, 241, 234, .16); }
  .side .sleeps dd { font-size: 38px; color: #d9d5cc; }
  .side .length dd { font-size: 30px; color: var(--silver); }
  .side .sleeps dt, .side .length dt { font-size: 13px; }

  /* Thirds overlay */
  .side .grid { position: absolute; inset: 0; z-index: 6; pointer-events: none; opacity: 0; transition: opacity .25s;
    background:
      linear-gradient(to right, transparent calc(33.333% - 1px), rgba(238,150,75,.9) calc(33.333% - 1px), rgba(238,150,75,.9) calc(33.333% + 1px), transparent calc(33.333% + 1px),
                                transparent calc(66.666% - 1px), rgba(238,150,75,.9) calc(66.666% - 1px), rgba(238,150,75,.9) calc(66.666% + 1px), transparent calc(66.666% + 1px)),
      linear-gradient(to bottom, transparent calc(33.333% - 1px), rgba(238,150,75,.9) calc(33.333% - 1px), rgba(238,150,75,.9) calc(33.333% + 1px), transparent calc(33.333% + 1px),
                                 transparent calc(66.666% - 1px), rgba(238,150,75,.9) calc(66.666% - 1px), rgba(238,150,75,.9) calc(66.666% + 1px), transparent calc(66.666% + 1px)); }
  body.show-grid .side .grid { opacity: 1; }
  .grid-toggle { position: fixed; right: 24px; bottom: 24px; z-index: 50; font: 600 14px/1 var(--poppins); letter-spacing: .06em; text-transform: uppercase;
                 background: var(--black); color: var(--bone); border: 0; padding: 14px 18px; cursor: pointer; display: flex; align-items: center; gap: 10px; }
  .grid-toggle::before { content: ""; width: 10px; height: 10px; border: 2px solid var(--orange); transform: rotate(45deg); }
  body.show-grid .grid-toggle::before { background: var(--orange); }
"""

cards = "".join(card(*c) for c in CARDS[:3])
section = f'''
  <section class="sample">
    <div class="intro">
      <span class="num">3C</span>
      <div><h2>Side Specs — Landscape 4:3</h2><p>Same layout turned landscape. The photo and name fill the left two-thirds and the specs take the right third. The spec rows are ATM, then Tare, then Sleeps and Length side by side. ATM stands out by size alone, with no side line.</p></div>
    </div>
    <div class="band">
      <div class="track">{cards}</div>
      <div class="progress"><span></span></div>
    </div>
  </section>'''

html = open("cards_template.html").read()
html = html.replace("<title>Drive Away card samples | Outbound RVs</title>", "<title>Side specs landscape sample | Outbound RVs</title>")
html = html.replace("<h1>DRIVE AWAY — CARD SAMPLES</h1>", "<h1>SIDE SPECS — LANDSCAPE SAMPLE</h1>")
html = html.replace("Three layout options for the stock cards, shown at the homepage size. Hover a card to see its interaction.",
                    "Built from option 3 with your changes. The photos are placeholders until the interior photos are ready. Use the button at the bottom right to show the thirds grid.")
html = html.replace(".num { flex: none; width: 100px;", ".num { flex: none; width: 110px;")
html = html.replace("</style>", EXTRA_CSS + "</style>")
html = html.replace("{{SAMPLES}}", section)
html = html.replace('<main class="page" id="page">',
                    '<button class="grid-toggle" type="button" onclick="document.body.classList.toggle(\'show-grid\')">Show thirds grid</button>\n<main class="page" id="page">')
open("side-landscape.html", "w").write(html)
print("samples/side-landscape.html written")
