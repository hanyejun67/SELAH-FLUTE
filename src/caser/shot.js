const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await (await b.newContext({ viewport: { width: 1000, height: 470 }, deviceScaleFactor: 1 })).newPage();
  for (const s of ['gold', 'silver']) {
    await p.goto('file://' + __dirname + '/case.html#' + s); await p.reload(); await p.waitForTimeout(400);
    await p.screenshot({ path: __dirname + '/case-' + s + '.jpg', type: 'jpeg', quality: 88 });
  }
  await b.close();
})();
