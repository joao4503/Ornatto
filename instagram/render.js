// Gera um PNG 1080x1350 para cada <section class="slide" id="..."> de um HTML.
// Uso: node render.js semana1/carrosseis.html semana1/png
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const [src, outDir] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const ids = await page.$$eval('section.slide', els => els.map(e => e.id));
  for (const id of ids) {
    await page.locator('#' + id).screenshot({ path: path.join(outDir, id + '.png') });
  }
  await browser.close();
  console.log(ids.length + ' slides');
})();
