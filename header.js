/* Shared header behaviour (site standard, every page loads this).
   The header bar is 60% opaque at the top of the page, goes fully solid while you scroll down, and lets go again to 60%
   as soon as you scroll back up. At the very top it is always 60%. The colour itself lives in site.css (--header-a). */
(() => {
  const header = document.getElementById('site-header');
  if (!header) return;
  const START = .6;        // opacity at rest
  const TOP = 40;          // px from the top that always counts as "at the top"
  const DEAD = 6;          // px of travel in one direction before the bar reacts, so a wobble doesn't flicker it
  let ref = scrollY;       // the furthest point reached in the current direction
  let solid = scrollY > TOP;   // arriving part-way down the page (a reload, an anchor link) counts as having scrolled down
  let ticking = false;

  const apply = () => header.style.setProperty('--header-a', solid ? 1 : START);
  const update = () => {
    const y = Math.max(0, scrollY);
    if (y <= TOP) { solid = false; ref = y; }
    else if (solid) { if (y > ref) ref = y; else if (ref - y > DEAD) { solid = false; ref = y; } }   // heading back up
    else { if (y < ref) ref = y; else if (y - ref > DEAD) { solid = true; ref = y; } }               // heading down
    apply();
  };

  addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { ticking = false; update(); });
  }, { passive: true });
  apply();
})();

/* Design aid, not part of the page: add ?grid to any address to draw the rule-of-thirds guide lines. */
if (/[?&]grid\b/.test(location.search)) document.body.classList.add('show-grid');
