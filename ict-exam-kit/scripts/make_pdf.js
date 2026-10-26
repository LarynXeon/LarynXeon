const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage();
  for (const [src, out] of [[process.argv[2], process.argv[3]], [process.argv[4], process.argv[5]]]) {
    await pg.goto('file://' + src);
    await pg.evaluate(async () => { await document.fonts.ready; });
    const ok = await pg.evaluate(() => document.fonts.check('16px "Hind Siliguri"', 'বাংলা'));
    await pg.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
    console.log(out, 'fontOK', ok);
  }
  await b.close();
})();
