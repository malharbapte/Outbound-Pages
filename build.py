"""Builds index.html from the Illustrator homepage artboards.

All coordinates below are the raw SVG coordinates from "Outbound Homepage.svg"
so the page can be checked against the design one-to-one.
Artboard 1 origin: (3528.15, 157.34). Artboard 2 origin: (6788.78, 157.34).
"""

AB_W = 2376
AB1 = (3528.15, 157.34)
AB2 = (6788.78, 157.34)

# Font vertical metrics (ascent, ascent+descent in em) used to place SVG baselines.
METRICS = {"P": (1.05, 1.4), "O": (1.193, 1.482)}

COL = {
    "black": "#0b0a07", "bone": "#f4f1ea", "green": "#8b9b4d", "olive": "#6b7a32",
    "grey": "#7a736a", "mauve": "#8e6673", "pink": "#d5aca9", "blue": "#284b63",
    "orange": "#ee964b", "silver": "#bcbec0",
}

def r(n):
    return f"{n:.2f}".rstrip("0").rstrip(".")


class Section:
    def __init__(self, tag, cls, ab, y0, y1, extra="", flow_top=None):
        self.tag, self.cls, self.ab, self.y0, self.y1, self.extra = tag, cls, ab, y0, y1, extra
        self.flow_top = flow_top  # when set, the section grows with in-flow content below this offset
        self.items = []

    def lx(self, x):
        return x - self.ab[0]

    def ly(self, y):
        return y - self.y0

    def add(self, html):
        self.items.append(html)

    def render(self):
        h = self.y1 - self.y0
        size = f"padding-top:{r(self.flow_top)}px" if self.flow_top is not None else f"height:{r(h)}px"
        body = "\n".join("    " + i for i in self.items)
        return (f'  <{self.tag} class="sec {self.cls}" style="{size}" {self.extra}>\n'
                f"{body}\n  </{self.tag}>")

    # ---- helpers -------------------------------------------------------
    def text(self, x, y, lines, font="P", size=36, weight=400, color="#000", lh=None,
             italic=False, center=False, tag="p", cls="", attrs=""):
        if isinstance(lines, str):
            lines = [lines]
        lh = lh or size * 1.2
        asc, full = METRICS[font]
        top = y - ((lh - full * size) / 2 + asc * size)
        fam = "var(--poppins)" if font == "P" else "var(--oswald)"
        style = (f"top:{r(self.ly(top))}px;"
                 + ("left:0;width:2376px;text-align:center;" if center else f"left:{r(self.lx(x))}px;")
                 + f"font-family:{fam};font-size:{r(size)}px;font-weight:{weight};"
                 f"line-height:{r(lh)}px;" + (f"color:{color};" if color else "")
                 + ("font-style:italic;" if italic else ""))
        c = f' class="t {cls}"'.replace("t ", "t ", 1) if cls else ' class="t"'
        self.add(f'<{tag}{c} style="{style}" {attrs}>{"<br>".join(lines)}</{tag}>'.replace(" >", ">"))

    def box(self, x, y, w, h, style="", tag="div", cls="", inner="", attrs=""):
        c = f' class="{cls}"' if cls else ""
        self.add(f'<{tag}{c} style="position:absolute;left:{r(self.lx(x))}px;top:{r(self.ly(y))}px;'
                 f'width:{r(w)}px;height:{r(h)}px;{style}" {attrs}>{inner}</{tag}>'.replace(" >", ">"))

    def img(self, x, y, w, h, src, alt="", style="", cls=""):
        c = f' class="{cls}"' if cls else ""
        self.add(f'<img{c} src="assets/{src}" alt="{alt}" style="position:absolute;left:{r(self.lx(x))}px;'
                 f'top:{r(self.ly(y))}px;width:{r(w)}px;height:{r(h)}px;{style}">')

    def svg(self, content, z=0, cls="shapes"):
        """Shapes pasted with raw coordinates; the viewBox maps them onto the section."""
        h = self.y1 - self.y0
        self.add(f'<svg class="{cls}" style="z-index:{z}" width="{AB_W}" height="{r(h)}" '
                 f'viewBox="{r(self.ab[0])} {r(self.y0)} {AB_W} {r(h)}" aria-hidden="true">{content}</svg>')


def btn(sec, x, y, w, h, label, tx, ty, href="#", tag="a"):
    """Green rectangle CTA with its label placed on the design baseline."""
    asc, full = METRICS["P"]
    lh = 43.2
    top = ty - ((lh - full * 36) / 2 + asc * 36)
    pad_top = top - y
    sec.box(x, y, w, h, tag=tag, cls="btn",
            style=f"padding-top:{r(pad_top)}px;",
            inner=label, attrs=(f'href="{href}"' if tag == "a" else 'type="submit"'))


# Reusable shape snippets (raw coordinates) ----------------------------------
# =============================================================================
# ARTBOARD 1
# =============================================================================
ab1 = []

# ---- Navigation --------------------------------------------------------------
# Sleeker sticky header: 160 tall (was 215.79). Logo mark sits on the left margin, links centred vertically.
NAV_H = 160
s = Section("header", "nav", AB1, 157.34, 157.34 + NAV_H)
s.box(3528.15, 157.34, 2376, NAV_H, cls="nav-bg")
s.add(f'<a href="#" class="logo" style="position:absolute;left:380.3px;top:-62.2px">'
      f'<img src="assets/outbound-logo.png" alt="Outbound RVs" style="width:402.8px;height:284.5px;display:block"></a>')
for x, label in [(4668.37, "CARAVANS"), (4876.06, "SUPPORT"), (5057.65, "CONTACT"), (5248.87, "ABOUT"), (5403.9, "REVIEWS")]:
    s.text(x, 157.34 + 88.4, label, size=24, weight=600, color="#000", tag="a", cls="navlink", attrs='href="#"')
ab1.append(s)

# ---- Hero ----------------------------------------------------------------------
s = Section("section", "hero", AB1, 373.13, 1709.63, 'style="overflow:hidden"')
s.img(3356.06, 319.85, 2565.74, 1443.24, "hero.jpg", "Wonderland RV caravan on an outback road")
s.text(0, 942.24, "INSPIRING JOURNEYS", font="O", size=146.18, weight=700, color="#fff", center=True, tag="h1")
s.text(5284.82, 1635.59, "JESSICA ISSABELLE", size=24, weight=600, color=COL["bone"])
ab1.append(s)

# ---- Exclusive dealership ---------------------------------------------------------
s = Section("section", "exclusive", AB1, 1709.63, 3168.16)
s.text(0, 1933.44, "EXCLUSIVE DEALERSHIP OF", font="O", size=84, weight=700, color="#000", center=True, tag="h2")
s.box(3528.15, 2014.19, 2376, 383.93, style=f"background:{COL['black']};")
s.img(4225.12, 2056.88, 981.1, 275.86, "wonderland-stacked-white.png", "Wonderland RV")
s.text(3923.54, 2766.58, ["We are the victorian dealership of Wonderland RV ",
                          "Caravans. While Wonderland RV’s is a Caravan ",
                          "manufacturer, we are exclusively dedicated to ",
                          "selling their caravans."], size=36, color="#000")
s.add(f'<div class="t" style="left:{r(s.lx(5142.87))}px;top:{r(s.ly(2644.95))}px;width:714.48px;height:312px;'
      f'opacity:.7;mix-blend-mode:multiply"><img src="assets/van-shadow.png" alt="" style="width:100%;height:100%;display:block"></div>')
s.img(4943.26, 2206.15, 1188.04, 776.87, "van-right.png", "Wonderland RV caravan, front three-quarter view", cls="van van-r")
s.img(3084.39, 1941.01, 1373.91, 915.94, "van-left.png", "Wonderland RV Solara caravan, side view", cls="van van-l")
ab1.append(s)

# ---- The Wonderland RV Range -------------------------------------------------------
s = Section("section", "range", AB1, 3168.16, 5000)
s.box(3528.15, 3168.16, 2376, 1782.27, style=f"background:{COL['bone']};")
cards = [
    (3528.15, "range-amaroo.jpg", 3507.58, 3174.77, 821 * .7734, 1915 * .7734, "AMAROO", 3652.18, "Classic Offroad", 3724.21),
    (4121.99, "range-hornet.jpg", 4060.50, 3348.16, 941 * .7055, 1672 * .7055, "HORNET", 4264.69, "Rugged Offroad", 4312.77),
    (4715.82, "range-solara.jpg", 4525.74, 3140.69, 941 * .8446, 1672 * .8446, "SOLARA", 4873.03, "Luxury Offroad", 4928.68),
    (5309.66, "range-xtr.jpg", 5196.33, 2864.86, 821 * .9799, 1915 * .9799, "XTR", 5531.39, "Extreme Offroad", 5503.52),
]
for cx, src, ix, iy, iw, ih, name, nx, sub, subx in cards:
    s.add(f'<a href="#" class="range-card" style="left:{r(s.lx(cx))}px;top:{r(s.ly(3393.53))}px;width:593.84px;height:1134.2px">'
          f'<img src="assets/{src}" alt="Wonderland RV {name.title()}" style="left:{r(ix - cx)}px;top:{r(iy - 3393.53)}px;width:{r(iw)}px;height:{r(ih)}px"></a>')
    s.text(nx, 4371.34, name, size=72, weight=600, color="#fff", tag="h3", cls="nopoint")
    s.text(subx, 4413.45, sub, size=24, weight=300, italic=True, color="#fff", cls="nopoint")
s.svg('<path fill="#ee964b" d="M3745.53,3383.54l-217.39,217.39v112.94l330.33-330.33c36.61-36.61,36.61-95.97,0-132.58l-82.8-82.8h-112.94l82.8,82.8c54.03,54.03,54.8,77.78,0,132.58Z"/>'
      '<polygon fill="#ee964b" points="5003.69 3448.68 5030.04 3474.86 5003.69 3503.42 5308.13 3503.42 5308.13 3448.68 5003.69 3448.68"/>', z=2)
s.text(3923.79, 3316.19, "The Wonderland RV Range", font="O", size=84, weight=500, color="#000", tag="h2")
s.text(5045.64, 3486.71, "Full Composite", size=33.07, color="#fff", cls="z3")
s.text(0, 4631.96, ["You can always customize the Van depending on your needs. The length and features ",
                    "will vary depending on your customization."], size=36, weight=600, color=COL["blue"], center=True)
btn(s, 4428.3, 4745.06, 574.93, 93.15, "BUILD YOUR CARAVAN", 4521.21, 4802.96)
s.box(3527.76, 4950.43, 2376, 37.79, cls="shadow-down")
ab1.append(s)

# ---- Drive Away (stock) ------------------------------------------------------------------
s = Section("section", "drive", AB1, 5000, 6430, flow_top=5592.05 - 5000)
s.text(3923.79, 5288.68, "DRIVE AWAY", font="O", size=84, weight=700, color="#000", tag="h2")
s.add(f'<input class="search" type="search" placeholder="Search" style="left:{r(s.lx(3923.5))}px;top:{r(s.ly(5406.76))}px">')
s.add(f'<button class="filter" style="left:{r(s.lx(4464.04))}px;top:{r(s.ly(5406.76))}px">Filter</button>')
s.text(5149.95, 5451.13, "View", size=24, weight=300, color=COL["grey"])
s.add(f'<div class="view-toggle" role="group" aria-label="Stock view" style="left:{r(s.lx(5230.53))}px;top:{r(s.ly(5406.76))}px">'
      '<button class="on" data-view="slide" aria-pressed="true" aria-label="Sliding cards"><svg viewBox="5230.53 5406.76 75.84 74.99"><clipPath id="vt1"><rect x="5230.55" y="5406.76" width="75.84" height="74.99" rx="2.55"/></clipPath><g clip-path="url(#vt1)"><rect fill="#8b9b4d" x="5285.19" y="5415.92" width="24.31" height="56.44" rx="2"/><rect fill="#8b9b4d" x="5256.32" y="5415.92" width="24.31" height="56.44" rx="2"/><rect fill="#8b9b4d" x="5227.44" y="5415.92" width="24.31" height="56.44" rx="2"/></g></svg></button>'
      '<button data-view="cols" aria-pressed="false" aria-label="Two columns"><svg viewBox="5331.19 5406.76 75.84 74.99"><rect fill="#8b9b4d" stroke="#0b0a07" stroke-width=".25" x="5370.67" y="5412.83" width="30.88" height="62.93" rx="2"/><rect fill="#8b9b4d" stroke="#0b0a07" stroke-width=".25" x="5337.08" y="5412.76" width="30.88" height="62.93" rx="2"/></svg></button>'
      '<button data-view="grid" aria-pressed="false" aria-label="Grid"><svg viewBox="5431.83 5406.76 75.84 74.99"><rect fill="#8b9b4d" stroke="#0b0a07" stroke-width=".25" x="5471.08" y="5412.67" width="30.18" height="30.2" rx="2"/><rect fill="#8b9b4d" stroke="#0b0a07" stroke-width=".25" x="5438.26" y="5412.64" width="30.18" height="30.2" rx="2"/><rect fill="#8b9b4d" stroke="#0b0a07" stroke-width=".25" x="5471.08" y="5445.68" width="30.18" height="30.2" rx="2"/><rect fill="#8b9b4d" stroke="#0b0a07" stroke-width=".25" x="5438.26" y="5445.65" width="30.18" height="30.2" rx="2"/></svg></button>'
      '</div>')

# Placeholder stock list until the real stock feed is supplied.
# Photos are range shots standing in for the interior images.
PHOTO = {"AMAROO": ("range-amaroo.jpg", "50% 62%"), "HORNET": ("range-hornet.jpg", "50% 64%"),
         "SOLARA": ("range-solara.jpg", "45% 70%"), "XTR": ("range-xtr.jpg", "40% 60%")}
# (range, layout, length, ATM kg, Tare kg, sleeps)
STOCK = [
    ("AMAROO", "Couples", "16'6\"", "3,300", "2,500", 2),
    ("HORNET", "Couples", "18'6\"", "3,500", "2,650", 2),
    ("SOLARA", "Couples", "18'6\"", "3,500", "2,580", 2),
    ("XTR", "Family", "20'6\"", "3,800", "2,950", 5),
    ("AMAROO", "Family", "19'6\"", "3,500", "2,780", 4),
    ("HORNET", "Family", "20'6\"", "3,800", "2,950", 5),
    ("SOLARA", "Family", "21'6\"", "3,800", "2,890", 4),
    ("XTR", "Couples", "19'6\"", "3,500", "2,700", 2),
]


def stock_card(name, layout, length, atm, tare, sleeps):
    """Landscape 4:3 card on a thirds grid: photo + name in the left two-thirds, specs in the right third."""
    img, focus = PHOTO[name]
    badge = '<span class="stock-badge">Composite</span>' if name == "SOLARA" else ""
    return (f'<a class="stock-card" href="#" draggable="false" aria-label="Wonderland RV {name.title()}, {layout.lower()} layout">'
            f'<div class="stock-photo"><img src="assets/{img}" alt="" draggable="false" style="object-position:{focus}">{badge}'
            f'<div class="stock-title"><p class="stock-layout">{layout} Layout</p><h3 class="stock-name">{name}</h3></div></div>'
            f'<dl class="stock-rail">'
            f'<div class="row r1"><div><dt>ATM</dt><dd>{atm}<small>kg</small></dd></div></div>'
            f'<div class="row r2"><div><dt>Tare</dt><dd>{tare}<small>kg</small></dd></div></div>'
            f'<div class="row r3"><div class="sleeps"><dt>Sleeps</dt><dd>{sleeps}</dd></div>'
            f'<div class="length"><dt>Length</dt><dd>{length}</dd></div></div>'
            f'</dl></a>')


cards_html = "".join(stock_card(*row) for row in STOCK)
s.add('<div class="stock-panel" data-view="slide">'
      '<div class="shadow-down"></div>'
      f'<div class="stock-viewport"><div class="stock-track">{cards_html}</div></div>'
      '<div class="stock-progress" aria-hidden="true"><span></span></div>'
      '<div class="shadow-up"></div>'
      '</div>')
ab1.append(s)

# ---- Come see us -----------------------------------------------------------------------
s = Section("section", "visit", AB1, 6430, 8796.01)
s.img(3515.81, 6475.22, 3285 * .727, 2320 * .727, "dealership.png", "Outbound RVs dealership at 58B Lara Way, Campbellfield")
s.text(3923.79, 6699.61, "COME SEE US", font="O", size=84, weight=700, color="#000", tag="h2")
s.text(3923.79, 7915.29, ["We are located at 58B Laraway, Campbellfeild VIC.", "You are welcome to visit us "], size=36, weight=600, color=COL["bone"])
btn(s, 3921.65, 8003.33, 507.27, 93.15, "Let Us know", 4071.5, 8061.23)
s.text(3923.79, 8251.26, "WE ARE OPEN ON :", size=36, weight=700, color=COL["black"])
s.text(3924.03, 8331.12, "Mon - Fri", size=36, weight=600, color=COL["black"])
s.text(3924.03, 8379.49, "9 am - 5 pm", size=36, color=COL["olive"])
s.text(4464.06, 8331.12, "Sat", size=36, weight=600, color=COL["black"])
s.text(4464.06, 8379.49, "Let us know beforehand by booking an appointment", size=36, color=COL["olive"])
s.svg('<rect fill="#284b63" x="3839.58" y="8465.45" width="50.99" height="50.99" transform="translate(-4871.9499 5219.9602) rotate(-45)"/>', z=1)
s.text(3923.79, 8482.66, ["We are closed on Sundays, and we acknowledge your patience. However, you can still ",
                          "reach out to us through the contact Us form."], size=36, weight=600, color=COL["blue"])
btn(s, 3921.65, 8581.59, 507.27, 93.15, "Fill the form", 4070.93, 8639.48)
ab1.append(s)

# ---- Ownership journey + we care (locked "static scroll" stage) ---------------------------------
# While the stage is locked each scroll lights the next diamond: Custom Caravan first (5 steps up to the
# meeting diamond), then Stock Van (4 steps, mirrored below), then "we care" holds for a few scrolls and
# Beyond Sale fades in. Behaviour lives in template.html.
TOP_Y, MERGE = 9359.63, (5463.43, 9711.08)
BOT_Y = 2 * MERGE[1] - TOP_Y  # the stock path mirrors the custom path about the meeting diamond
TOP_PATH = ("M3966.34 9359.63 H5049.2 C5049.2 9359.63 5194.89 9345.97 5250.48 9458.28 "
            "C5306.08 9570.59 5330.77 9711.47 5432.95 9711.08 H6800")  # runs past the edge; the stage clips it
BOT_PATH = (f"M3966.34 {r(BOT_Y)} H5049.2 C5049.2 {r(BOT_Y)} 5194.89 10076.19 5250.48 9963.88 "
            "C5306.08 9851.57 5330.77 9710.69 5432.95 9711.08")

# Placeholder step copy until the real journey text is supplied. (title, description)
CUSTOM_STEPS = [
    ("Understanding your needs", "We sit down with you to learn how you travel, where you want to go and what matters most in a caravan."),
    ("Designing your layout", "Together we choose the model, floor plan and features, and lock in a build spec that suits your journey."),
    ("Confirming your build", "Your order is placed with Wonderland RV and your caravan is booked into the factory build schedule."),
    ("Built for you", "Your caravan is built to your spec, with updates from our team along the way."),
]
STOCK_STEPS = [
    ("Understanding your needs", "Tell us how you like to travel and we match you with the vans we have in stock."),
    ("Choosing your van", "Walk through it in person at our Campbellfield yard, or take a virtual tour."),
    ("Finance and paperwork", "We help with finance, registration and pre-delivery checks so everything is ready."),
]
HANDOVER = ("Handover", "We walk you through every feature before you hitch up and head off. This is where the journey really begins.")

XS = [3966.34, 4335.63, 4704.92, 5074.2]
# Stock diamonds: first lines up with custom 1, last with custom 4 (where the curve starts), middle halfway.
STOCK_XS = [XS[0], (XS[0] + XS[3]) / 2, XS[3]]
journey_steps = ([("custom", i + 1, XS[i], TOP_Y, *c) for i, c in enumerate(CUSTOM_STEPS)]
                 + [("custom", 5, *MERGE, *HANDOVER)]
                 + [("stock", i + 1, STOCK_XS[i], BOT_Y, *c) for i, c in enumerate(STOCK_STEPS)]
                 + [("stock", 4, *MERGE, *HANDOVER)])

journey = Section("div", "journey-layer", AB1, 8796.01, 10360.79)
journey.text(3923.79, 9035.77, "OWNERSHIP JOURNEY", font="O", size=84, weight=700, color=COL["bone"], tag="h2")
journey.text(3923.79, 9100.07, "THE BEGINNING OF A EVERLASTING RELATIONSHIP", font="O", size=48, weight=300, color="#fff")
journey.text(3923.79, 9264.98, "CUSTOM CARAVAN (9-12 MONTHS)", size=48, color=COL["bone"], cls="path-label", attrs='data-path="custom"')
journey.text(3923.79, 10184.97, "STOCK VAN (1 MONTH)", size=48, color=COL["bone"], cls="path-label", attrs='data-path="stock"')

svg = (f'<path class="track track-stock" d="{BOT_PATH}"/><path class="track" d="{TOP_PATH}"/>'
       + f'<path class="fill fill-custom" d="{TOP_PATH}"/><path class="fill fill-stock" d="{BOT_PATH}"/>')
for k, (path, n, x, y, title, desc) in enumerate(journey_steps):
    if path == "stock" and (x, y) == MERGE:
        continue  # the meeting diamond is shared, drawn once
    svg += (f'<rect class="step-diamond d-{path}" data-step="{k}" x="-30.06" y="-30.06" width="60.11" height="60.11" '
            f'transform="translate({r(x)} {r(y)}) rotate(45)"/>')
journey.svg(svg, z=1, cls="shapes journey-svg")

# All step text is anchored where step 1 sits (pink square at 3932.78, 9605.52) and cross-fades.
for k, (path, n, x, y, title, desc) in enumerate(journey_steps):
    journey.add(f'<div class="step-panel" data-step="{k}" data-path="{path}" data-x="{r(x)}" data-y="{r(y)}" '
                f'style="left:{r(journey.lx(3932.78))}px;top:{r(journey.ly(9605.52))}px">'
                f'<span class="step-num">{n}</span><div class="step-text"><h3>{title}</h3><p>{desc}</p></div></div>')

care = Section("div", "care-layer", AB1, 10360.79, 11925.41)
care.svg('<rect fill="#f4f1ea" x="4645.81" y="10970.73" width="140.67" height="140.67" rx="33.79" transform="translate(-6425.8867 6568.6819) rotate(-45.0001)"/>', z=1)
care.text(0, 11061.86, "we care", size=79.65, weight=600, color=COL["pink"], center=True, tag="h2")
care.text(0, 11204.52, ["We understand the growing uncertainity in the Caravan industry, with a lot of companies ",
                        "going under. We assure you your money is safe with us. We ensure that by :"],
          size=36, weight=300, color=COL["pink"], center=True)

STAGE_H = 1564.77


class JourneyScroll:
    cls = "journey-scroll"

    def render(self):
        def layer(sec):
            # Content scales to fit the window height and centres; edge shapes stay pinned to the screen edges.
            edge = lambda side: "".join(i for i in sec.items if f"edge-{side}" in i)
            body = "\n".join("        " + i for i in sec.items if "edge-left" not in i and "edge-right" not in i)
            return (f'    <div class="layer {sec.cls}">\n      <div class="layer-content">\n{body}\n      </div>\n'
                    f'      <div class="layer-edge left">{edge("left")}</div><div class="layer-edge right">{edge("right")}</div>\n    </div>')
        return (f'  <section class="sec journey-scroll" id="journey" style="height:{r(STAGE_H)}px" aria-label="Ownership journey">\n'
                f'   <div class="journey-stage" id="journey-stage">\n{layer(journey)}\n{layer(care)}\n   </div>\n  </section>')


ab1.append(JourneyScroll())

# ---- Beyond sale --------------------------------------------------------------------------
s = Section("section", "beyond", AB1, 11925.41, 12991.65, 'id="after-journey"')
s.box(3528.27, 11925.41, 2375.75, 1066.24, style="background:#fff;border-bottom:.25px solid #0b0a07;")  # divider before Stories
s.text(3923.79, 12188.19, "BEYOND SALE", font="O", size=84, weight=700, color="#000", tag="h2")
# Expanding panels (see samples/beyond-sale.html): hovering a panel widens it to show its description;
# it stays open until another panel is hovered. Panels start on the upper third line of the section.
ICONS = {
    "FINANCE": '<circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/>',
    "SERVICING": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "WARRANTY": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
}
services = [
    ("FINANCE", "The right caravan deserves a finance plan that feels just as considered. We’ll help you explore suitable options and guide you through the process clearly."),
    ("SERVICING", "From your first 1,000 km service to annual servicing and general repairs, our experienced team will help keep your caravan ready for what comes next."),
    ("WARRANTY", "Every new Wonderland RV comes with a three-year factory-backed warranty. If something needs attention, our team will help guide you through the process."),
]
panels = "".join(
    f'<div class="bs-item{" on" if i == 0 else ""}" tabindex="0">'
    f'<svg class="bs-icon" viewBox="0 0 24 24" aria-hidden="true">{ICONS[title]}</svg>'
    f'<h3>{title}</h3><p class="bs-desc">{desc}</p></div>'
    for i, (title, desc) in enumerate(services))
s.add(f'<div class="bs-items" style="left:{r(s.lx(3923.5))}px;top:{r(s.ly(11925.41 + 1066.24 / 3))}px">{panels}</div>')
ab1.append(s)

# ---- Stories from our customers ------------------------------------------------------------------
s = Section("section", "stories", AB1, 12991.65, 15046.76)
s.text(0, 13329.64, "STORIES FROM OUR CUSTOMERS", font="O", size=84, weight=700, color=COL["mauve"], center=True, tag="h2")
tile = "position:absolute;box-sizing:border-box;width:791.96px;height:791.96px;"
s.box(3528.27, 13461.35, 791.96, 791.96, cls="tile tile-white")
s.box(4320.23, 13461.35, 791.96, 791.96, cls="tile", style=f"background:{COL['bone']};")
s.box(5112.19, 13461.35, 791.96, 791.96, cls="tile tile-green")
s.box(3528.27, 14253.31, 791.96, 791.96, cls="tile tile-green")
s.box(4320.23, 14253.31, 791.96, 791.96, cls="tile tile-white")
s.box(5112.19, 14253.31, 791.96, 791.96, cls="tile tile-white")
s.svg('<path fill="#d5aca9" d="M4450.96,13460.7l-131.03,131.03,131.03,131.03,131.03-131.03-131.03-131.03ZM4450.84,13690.64l-98.8-98.8,98.8-98.8,98.8,98.8-98.8,98.8Z"/>', z=2)
s.text(4463.32, 13775.28, "Wonderland is ....", size=32, color=COL["mauve"])
s.text(4463.18, 14158.23, "Kevin Smalley", size=32, color=COL["mauve"])
s.text(3735.16, 13847.4, "Image to be added.", size=32, color=COL["mauve"])
s.text(4540.4, 14641.06, "Image to be added.", size=32, color=COL["mauve"])
s.text(5363.59, 14641.06, "Image to be added.", size=32, color=COL["mauve"])
ab1.append(s)

# Decorative chevrons for artboard 1, attached to the section they start in (z0 behind, z4 in front)
AB1_TOP, AB1_BOTTOM = 157.34, 15046.76
sec = {x.cls: x for x in ab1}
sec["range"].svg('<polygon fill="#6b7a32" opacity=".4" points="4458.33 4621.05 3408.34 3571.06 3007.89 3971.52 3657.41 4621.05 3007.89 5270.58 3408.34 5671.03 4458.33 4621.05"/>'
                 '<polygon fill="#7a736a" opacity=".4" style="mix-blend-mode:multiply" points="4922.99 5700.13 5972.97 6750.12 6373.43 6349.66 5723.9 5700.13 6373.43 5050.6 5972.97 4650.15 4922.99 5700.13"/>', z=0, cls="shapes deco-back")
sec["visit"].svg('<polygon fill="#6b7a32" opacity=".4" points="4922.99 9310.93 5972.97 10360.92 6373.43 9960.46 5723.9 9310.93 6373.43 8661.4 5972.97 8260.95 4922.99 9310.93"/>', z=0, cls="shapes deco-back")
sec["stories"].svg('<polygon fill="#6b7a32" opacity=".4" points="5561.6 13460.7 5910.03 13809.13 6042.91 13676.24 5827.37 13460.7 6042.91 13245.16 5910.03 13112.28 5561.6 13460.7"/>', z=0, cls="shapes deco-back")
care.svg('<polygon fill="#f4f1ea" points="3360.73 10847.61 3468.71 10955.59 3751.83 10672.47 3468.71 10389.35 3360.73 10497.33 3535.87 10672.47 3360.73 10847.61"/>', z=4, cls="shapes edge-left")
care.svg('<polygon fill="#f4f1ea" points="6051.76 11298.51 5904.01 11150.76 5516.61 11538.16 5904.01 11925.56 6051.76 11777.81 5812.11 11538.16 6051.76 11298.51"/>', z=4, cls="shapes edge-right")
sec["beyond"].svg('<polygon fill="#7a736a" opacity=".4" style="mix-blend-mode:multiply" points="3862.45 12991.65 3514.02 12643.22 3381.14 12776.11 3596.68 12991.65 3381.14 13207.19 3514.02 13340.07 3862.45 12991.65"/>'
                  '<polygon fill="#6b7a32" opacity=".4" points="5608.66 12404.76 5756.41 12552.51 6143.81 12165.11 5904.26 11925.56 5608.66 11925.46 5848.31 12165.11 5608.66 12404.76"/>', z=4)

# =============================================================================
# ARTBOARD 2 (continues below artboard 1)
# =============================================================================
ab2 = []

# ---- What makes us different ------------------------------------------------------
s = Section("section", "different", AB2, 157.34, 1250)
s.text(7184.66, 449.96, "WHAT MAKES US DIFFERENT?", font="O", size=84, weight=700, color="#000", tag="h2")
s.text(7184.67, 583.84, "We listen first, guide honestly and stay for the journey.", size=36, weight=600, color=COL["black"])
s.svg('<line stroke="#6b7a32" stroke-width="4" x1="7184.62" y1="704.95" x2="8768.64" y2="704.95"/>'
      '<rect fill="#8b9b4d" x="7196.75" y="675.42" width="59.04" height="59.04" transform="translate(2614.9982 -4903.2735) rotate(45)"/>'
      '<rect fill="#f4f1ea" stroke="#8b9b4d" stroke-width="4" x="7695.66" y="675.42" width="59.04" height="59.04" transform="translate(2761.1248 -5256.0542) rotate(45)"/>'
      '<rect fill="#f4f1ea" stroke="#8b9b4d" stroke-width="4" x="8220.3" y="675.42" width="59.04" height="59.04" transform="translate(2914.7879 -5627.0299) rotate(45)"/>'
      '<rect fill="#f4f1ea" stroke="#8b9b4d" stroke-width="4" x="8697.63" y="675.42" width="59.04" height="59.04" transform="translate(3054.5945 -5964.5529) rotate(45)"/>', z=1)
steps = [
    (7184.65, ["Guidance"], ["We take the time to understand your ", "lifestyle, travel plans and needs before ", "helping you find the right fit."]),
    (7689.80, ["Honest Advice, ", "Without Pressure"], ["Clear recommendations and transparent ", "conversations, always centred on what is ", "right for you."]),
]
for x, head, desc in steps:
    s.text(x, 848.75, head, size=36, weight=600, color=COL["black"], tag="h3")
    s.text(x, 940.2, desc, size=24, lh=28.8, color=COL["black"])
s.text(7184.67, 1118.82, ["Know more, ", "About Us."], size=36, weight=600, color=COL["olive"], tag="a", cls="link", attrs='href="#"')
ab2.append(s)

# ---- Contact us ---------------------------------------------------------------------
s = Section("section", "contact", AB2, 1250, 2538.18)
s.text(7184.66, 1387.8, "CONTACT US", font="O", size=84, weight=700, color="#000", tag="h2")
s.text(7184.66, 1458.85, "LET’S GET YOUR JOURNEY STARTED", font="O", size=48, weight=300, color="#000")
s.text(7184.67, 1597.04, ["Fill in your details, and our ", "team will get in touch with ", "you shortly"], size=36, weight=600, color=COL["olive"])
s.text(7184.67, 1747.96, "*Our team will contact you within 48 hrs.", size=24, color=COL["olive"])
s.add(f'<form class="contact-form" style="left:{r(s.lx(7725.18))}px;top:{r(s.ly(1560.12))}px" onsubmit="return false">'
      '<div class="row"><input class="line" name="first" placeholder="First Name"><input class="line" name="last" placeholder="Last Name"></div>'
      '<div class="row"><input class="line" name="phone" type="tel" placeholder="Phone no."><input class="line" name="email" type="email" placeholder="Email"></div>'
      '<div class="row"><select class="boxed" name="state"><option value="" selected disabled hidden>State</option><option>VIC</option><option>NSW</option><option>QLD</option><option>SA</option><option>WA</option><option>TAS</option><option>NT</option><option>ACT</option></select>'
      '<input class="line" name="postcode" placeholder="Post Code"></div>'
      '<fieldset class="tabs"><legend class="sr">How can we help?</legend>'
      '<label><input type="radio" name="intent" value="tour"><span>Book a<br>factory tour</span></label>'
      '<label><input type="radio" name="intent" value="virtual"><span>A virtual tour</span></label>'
      '<label><input type="radio" name="intent" value="callback" checked><span>Call back</span></label>'
      '<label><input type="radio" name="intent" value="quote"><span>Get a quote</span></label></fieldset>'
      '<textarea name="message" placeholder="Is there something else you want to tell us..."></textarea>'
      '<label class="consent"><input type="checkbox" name="marketing"><span>Tick to receive marketing communications with discounts, updates, new releases<br>and more from Wonderland RV.</span></label>'
      '<button class="btn submit" type="submit">SUBMIT</button>'
      '</form>')
s.text(7184.67, 2079.8, ["You too can reach ", "out to us at :"], size=36, weight=600, color="#000")
s.box(7187.04, 2176.31, 73.41, 73.41, tag="a", cls="social", attrs='href="#" aria-label="Instagram"')
s.box(7302.63, 2174.56, 73.41, 73.41, tag="a", cls="social", attrs='href="#" aria-label="Facebook"')
s.box(7185.5, 2281.33, 36.32, 36.32, cls="mini-icon")
s.box(7185.5, 2339.37, 36.32, 36.32, cls="mini-icon")
s.text(7240.46, 2308.38, "03 9958 6708", size=24, weight=600, color=COL["black"], tag="a", attrs='href="tel:0399586708"')
s.text(7240.46, 2366.41, "sales@outboundrvs.com.au", size=24, weight=600, color=COL["black"], tag="a", attrs='href="mailto:sales@outboundrvs.com.au"')
ab2.append(s)

# ---- Instagram ----------------------------------------------------------------------------
s = Section("section", "insta", AB2, 2538.18, 3337.77)
s.box(6785.48, 2538.18, 2379.31, 799.59, style=f"background:{COL['black']};")
s.text(7184.66, 2711.45, "FOLLOW US ON INSTAGRAM", font="O", size=48, weight=700, color=COL["bone"], tag="h2")
tiles = "".join('<a href="#" class="ig-tile" aria-label="Instagram post"></a>' for _ in range(6))
s.add(f'<div class="ig-track" style="left:{r(s.lx(6785.21))}px;top:{r(s.ly(2788.46))}px">{tiles}</div>')
ab2.append(s)

# ---- FAQ ------------------------------------------------------------------------------------
s = Section("section", "faq", AB2, 3337.77, 4196.81)
s.text(7184.66, 3530.09, "FAQ’S", font="O", size=84, weight=700, color="#000", tag="h2")
asc, full = METRICS["P"]
q_top = 3653.78 - ((42 - full * 32) / 2 + asc * 32)
s.add(f'<div class="faq-list" style="left:{r(s.lx(7184.67))}px;top:{r(s.ly(q_top))}px">'
      '<details><summary>How do I tow?</summary><div class="answer">Answer :</div></details>'
      '<details><summary>How can I claim warranty form?</summary><div class="answer">Answer :</div></details>'
      '<details open><summary>What components are not covered under warranty?</summary><div class="answer">Answer :</div></details>'
      '</div>')
ab2.append(s)

# ---- Footer ---------------------------------------------------------------------------------
s = Section("footer", "footer", AB2, 4196.81, 4542.3, 'style="overflow:hidden"')
s.box(6788.78, 4196.81, 2376, 345.38, style=f"background:{COL['black']};")
s.svg('<polygon fill="#6b7a32" points="6751.03 4196.81 6960.41 4196.81 7136.68 4370 6960.41 4542.19 6751.92 4542.3 6924.22 4370 6751.03 4196.81"/>'
      '<polygon fill="#8b9b4d" points="6878.76 4369.5 6649.59 4140.33 6562.19 4227.74 6703.95 4369.5 6562.19 4511.27 6649.59 4598.67 6878.76 4369.5"/>'
      '<rect fill="#8b9b4d" x="8786.13" y="4247.39" width="244.22" height="244.22" transform="translate(-480.537 7578.8858) rotate(-45.0001)"/>'
      '<polygon fill="#f4f1ea" points="8955.41 4196.81 9164.78 4196.81 9341.05 4370 9164.78 4542.19 8956.29 4542.3 9128.6 4370 8955.41 4196.81"/>', z=1)
s.text(7185.36, 4273.32, "Caravan Manufacturer", size=24, weight=600, color=COL["bone"])
s.add(f'<a href="#" style="position:absolute;left:{r(s.lx(7187.02))}px;top:{r(s.ly(4320.4))}px;z-index:2">'
      '<img src="assets/wonderland-line-white.png" alt="Wonderland RV" style="width:479.24px;height:68.78px;display:block"></a>')
s.text(7185.36, 4450.4, ['<a href="#">Privacy Policy</a> | <a href="#">Terms of Use</a> | ', "© 2026 Outbound RVs All Rights Reserved "],
       size=24, lh=28.8, weight=300, color=COL["bone"])
s.text(7784.04, 4279.92, "Reach us at :", size=24, weight=600, color=COL["bone"])
s.box(7785.57, 4305.15, 73.41, 73.41, tag="a", cls="social social-f", attrs='href="#" aria-label="Instagram"')
s.box(7901.16, 4303.39, 73.41, 73.41, tag="a", cls="social social-f", attrs='href="#" aria-label="Facebook"')
s.box(7784.04, 4400.05, 36.32, 36.32, cls="mini-icon mini-f")
s.box(7784.04, 4449.8, 36.32, 36.32, cls="mini-icon mini-f")
s.text(7838.99, 4427.09, "03 9958 6708", size=24, color=COL["bone"], tag="a", attrs='href="tel:0399586708"')
s.text(7838.99, 4476.84, "sales@outboundrvs.com.au", size=24, color=COL["bone"], tag="a", attrs='href="mailto:sales@outboundrvs.com.au"')
s.text(8264.47, 4278.53, "Address", size=24, weight=600, color=COL["bone"])
s.text(8265.09, 4319.75, ["Unit 58B Lara Way, ", "Campbellfield, VIC 3061"], size=24, lh=28.8, color=COL["bone"])
s.text(8264.47, 4403.82, "Trading Hours", size=24, weight=600, color=COL["bone"])
s.text(8265.09, 4440.44, ["Weekdays - 9 am to 5 pm", "Saturday - Appointments Only", "Sunday - Closed"], size=18, lh=21.6, color=COL["bone"])
ab2.append(s)

ab2_back = '<polygon fill="#7a736a" opacity=".4" style="mix-blend-mode:multiply" points="8484.97 1235.97 9347.81 2098.82 9676.9 1769.74 9143.13 1235.97 9676.9 702.21 9347.81 373.13 8484.97 1235.97"/>'
AB2_TOP, AB2_BOTTOM = 157.34, 4542.3


def layer(ab, top, bottom, content, z):
    h = bottom - top
    return (f'<svg class="deco" style="z-index:{z}" width="{AB_W}" height="{r(h)}" '
            f'viewBox="{r(ab[0])} {r(top)} {AB_W} {r(h)}" aria-hidden="true">{content}</svg>')


def artboard(name, sections, back, front, ab, top, bottom):
    parts = [f'<div class="artboard {name}">']
    if back:
        parts.append("  " + layer(ab, top, bottom, back, 0))
    parts += [sec.render() for sec in sections]
    if front:
        parts.append("  " + layer(ab, top, bottom, front, 4))
    parts.append("</div>")
    return "\n".join(parts)


html = open("template.html").read()
html = html.replace("{{ARTBOARD_1}}", artboard("ab1", ab1, "", "", AB1, AB1_TOP, AB1_BOTTOM))
html = html.replace("{{ARTBOARD_2}}", artboard("ab2", ab2, ab2_back, "", AB2, AB2_TOP, AB2_BOTTOM))
import sys
out = sys.argv[1] if len(sys.argv) > 1 else "index.html"
open(out, "w").write(html)
print(out, "written")
