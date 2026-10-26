const { chromium } = require('playwright');
const path = process.argv[2], shots = process.argv[3];
(async () => {
  const b = await chromium.launch();
  const errs = [];
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const pg = await ctx.newPage();
  pg.on('pageerror', e => errs.push('pageerror: ' + e.message));
  pg.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await pg.goto('file://' + path);
  await pg.waitForTimeout(600);
  const fontOk = await pg.evaluate(async () => { await document.fonts.ready; return [document.fonts.check('16px "Hind Siliguri"', 'বাংলা যুক্তাক্ষর ক্ষ'), document.fonts.check('700 16px "Noto Serif Bengali"', 'বাংলা')]; });
  console.log('fonts', fontOk);
  await pg.screenshot({ path: shots + '/q_light.png' });
  // answer the first card wrong on purpose
  const info = await pg.evaluate(() => { const c = window.__kit.cur().c; return { id: c.id, a: c.a, order: window.__kit.cur().order }; });
  const wrongPos = info.order.findIndex(oi => oi !== info.a);
  await pg.click('#opt' + wrongPos);
  await pg.waitForTimeout(200);
  console.log('verdict', await pg.textContent('.verdict'));
  console.log('rate', await pg.textContent('.rate .rlabel'));
  await pg.screenshot({ path: shots + '/fb_light.png', fullPage: true });
  let st = await pg.evaluate(id => JSON.stringify(window.__kit.S.cs[id]) + ' tick=' + window.__kit.S.tick, info.id);
  console.log('state after wrong', st);
  // override to Good
  await pg.click('#rateRow button[data-r="good"]');
  st = await pg.evaluate(id => JSON.stringify(window.__kit.S.cs[id]), info.id);
  console.log('after override good', st);
  await pg.click('#rateRow button[data-r="again"]');
  st = await pg.evaluate(id => JSON.stringify(window.__kit.S.cs[id]), info.id);
  console.log('after override again', st);
  // play 8 more cards answering correctly, check wrong card returns
  const seen = [];
  for (let i = 0; i < 8; i++) {
    await pg.click('#nextBtn');
    const c = await pg.evaluate(() => { const k = window.__kit.cur(); return { id: k.c.id, ch: k.c.c, pos: k.order.indexOf(k.c.a) }; });
    seen.push(c.id + '/' + c.ch);
    await pg.click('#opt' + c.pos);
  }
  console.log('first', info.id, 'sequence', seen.join(' '));
  // dark theme via settings
  await pg.click('#tab-set');
  await pg.click('#sTheme button[data-v="dark"]');
  console.log('theme attr', await pg.evaluate(() => document.documentElement.getAttribute('data-theme')));
  await pg.screenshot({ path: shots + '/set_dark.png', fullPage: true });
  await pg.click('#tab-quiz');
  await pg.click('#nextBtn');
  await pg.screenshot({ path: shots + '/q_dark.png' });
  await pg.click('#tab-notes'); await pg.waitForTimeout(200);
  await pg.screenshot({ path: shots + '/notes_dark.png' });
  await pg.click('#tab-prog'); await pg.waitForTimeout(200);
  await pg.screenshot({ path: shots + '/prog_dark.png', fullPage: true });
  // modes
  await pg.click('#tab-quiz');
  for (const m of ['chapter', 'wrong', 'star', 'morning', 'mix']) {
    await pg.click(`#modes .chip[data-m="${m}"]`);
    const t = await pg.evaluate(() => [document.querySelector('#stLeft').textContent, document.querySelector('#stRight').textContent, !!document.querySelector('.opt')]);
    console.log('mode', m, t.join(' | '));
  }
  // overflow check
  const ow = await pg.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  console.log('h-overflow px', ow);
  // reload persistence
  await pg.reload(); await pg.waitForTimeout(300);
  console.log('persist tick', await pg.evaluate(() => window.__kit.S.tick), 'theme', await pg.evaluate(() => document.documentElement.getAttribute('data-theme')));
  console.log('ERRORS', errs.length ? errs.join('\n') : 'none');
  await b.close();
})();
