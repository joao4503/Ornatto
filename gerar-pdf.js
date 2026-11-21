// Gera o PDF (A4) e uma prévia PNG a partir de tabela-precos.html
// Uso: node gerar-pdf.js
const { chromium } = require('playwright');
const path = require('path');
const { execSync } = require('child_process');

(async () => {
  const html = 'file://' + path.resolve(__dirname, 'tabela-precos.html');
  const pdf = path.resolve(__dirname, 'output/TabelaPrecos_Ornatto.pdf');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(html, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  // aviso se o conteúdo passar de uma página
  const overflow = await page.evaluate(() => {
    const m = document.querySelector('main'); return m.scrollHeight - m.clientHeight;
  });
  if (overflow > 0) console.warn(`ATENÇÃO: conteúdo excede a página em ${overflow}px`);
  await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  // prévia PNG (requer poppler-utils)
  execSync(`pdftoppm -png -r 200 -singlefile "${pdf}" "${pdf.replace(/\.pdf$/, '')}"`);
  console.log('OK:', pdf);
})();
