const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {spawn} = require('node:child_process');
(async () => {
  const server = spawn(process.execPath, ['scripts/serve.cjs'], {env:{...process.env,PORT:'4179'},stdio:['ignore','pipe','pipe']});
  await new Promise((resolve,reject) => {server.stdout.once('data',resolve);server.once('error',reject);server.once('exit',code=>reject(new Error(`server exit ${code}`)));});
  const browser = await chromium.launch({channel:'chrome', headless:true});
  try {
    const context = await browser.newContext();
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('response', r => {if(r.status() >= 400) errors.push(`${r.status()} ${r.url()}`);});
    await page.goto('http://127.0.0.1:4179/diario.html');
    assert.equal(await page.locator('.planet-destination').count(), 8);
    assert.equal(await page.locator('.album-card').count(), 0);
    fs.mkdirSync('output/diario', {recursive:true});
    for (const width of [1440,390,320]) {
      await page.setViewportSize({width,height:900});
      await page.locator('.planet-destination img').evaluateAll(imgs => Promise.all(imgs.map(i => i.decode())));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.screenshot({path:`output/diario/planetas-${width}.png`,fullPage:true});
    }
    await page.locator('a[href="diario-planeta.html?planeta=tempus"]').click();
    await page.waitForFunction(() => document.body.dataset.planet === 'tempus');
    assert.equal(await page.locator('#planet-title').innerText(), 'Tempus');
    assert.equal(await page.locator('.is-owned').count(), 12);
    assert.equal(await page.locator('.card-action').count(), 0);
    await page.locator('#read-full-story').click();
    assert.deepEqual(await page.locator('#full-story-content p').allTextContents(), await page.evaluate(() => ORBITA_DIARY.cards.map(c => c.text)));
    await page.keyboard.press('Escape');
    for (let i=0;i<12;i++) {
      await page.locator('.card-image').nth(i).click();
      assert.equal(await page.locator('#viewer-text').innerText(), await page.evaluate(i => ORBITA_DIARY.cards[i].text, i));
      await page.locator('#viewer-image').evaluate(img => img.decode());
      await page.keyboard.press('Escape');
    }
    assert.equal(await page.evaluate(() => localStorage.getItem('orbita2-wallet-v1')), null);
    for (const [width,height] of [[1440,1000],[768,1024],[390,844],[320,740]]) {
      await page.setViewportSize({width,height});
      await page.evaluate(() => scrollTo(0,0));
      await page.locator('.card-image img').evaluateAll(imgs => Promise.all(imgs.map(img => img.decode())));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.screenshot({path:'output/diario/tempus-'+width+'.png',fullPage:true});
      await page.locator('.card-image').last().click();
      assert(await page.locator('#photo-viewer').evaluate(e => e.scrollWidth <= e.clientWidth));
      await page.screenshot({path:'output/diario/tempus-popup-'+width+'.png'});
      await page.keyboard.press('Escape');
    }
    await page.locator('.back-planets').click();
    if (process.env.DIARY_PLANET_ONLY === 'tempus') {
      assert.deepEqual(errors, []);
      console.log('OK: Tempus, eight-planet gallery, 12 images, full text, unchanged wallet, dialogs and four responsive widths.');
      return;
    }
    await page.locator('a[href="diario-planeta.html?planeta=papiron"]').click();
    await page.waitForFunction(() => document.body.dataset.planet === 'papiron');
    assert.equal(await page.locator('#planet-title').innerText(), 'Papiron');
    assert.equal(await page.locator('.is-owned').count(), 12);
    assert.equal(await page.locator('.card-action').count(), 0);
    await page.locator('#read-full-story').click();
    assert.deepEqual(await page.locator('#full-story-content p').allTextContents(), await page.evaluate(() => ORBITA_DIARY.cards.map(c => c.text)));
    await page.keyboard.press('Escape');
    for (let i=0;i<12;i++) {
      await page.locator('.card-image').nth(i).click();
      assert.equal(await page.locator('#viewer-text').innerText(), await page.evaluate(i => ORBITA_DIARY.cards[i].text, i));
      await page.locator('#viewer-image').evaluate(img => img.decode());
      await page.keyboard.press('Escape');
    }
    assert.equal(await page.evaluate(() => localStorage.getItem('orbita2-wallet-v1')), null);
    for (const [width,height] of [[1440,1000],[768,1024],[390,844],[320,740]]) {
      await page.setViewportSize({width,height});
      await page.evaluate(() => scrollTo(0,0));
      await page.locator('.card-image img').evaluateAll(imgs => Promise.all(imgs.map(img => img.decode())));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.screenshot({path:'output/diario/papiron-'+width+'.png',fullPage:true});
      await page.locator('.card-image').last().click();
      assert(await page.locator('#photo-viewer').evaluate(e => e.scrollWidth <= e.clientWidth));
      await page.screenshot({path:'output/diario/papiron-popup-'+width+'.png'});
      await page.keyboard.press('Escape');
    }
    await page.locator('.back-planets').click();
    await page.locator('a[href="diario-planeta.html?planeta=atria"]').click();
    await page.waitForFunction(() => document.body.dataset.planet === 'atria');
    assert.equal(await page.locator('#planet-title').innerText(), 'Átria');
    assert.equal(await page.locator('.is-owned').count(), 12);
    assert.equal(await page.locator('.card-action').count(), 0);
    await page.locator('#read-full-story').click();
    assert.deepEqual(await page.locator('#full-story-content p').allTextContents(), await page.evaluate(() => ORBITA_DIARY.cards.map(c => c.text)));
    await page.keyboard.press('Escape');
    for (let i=0;i<12;i++) {
      await page.locator('.card-image').nth(i).click();
      assert.equal(await page.locator('#viewer-text').innerText(), await page.evaluate(i => ORBITA_DIARY.cards[i].text, i));
      await page.locator('#viewer-image').evaluate(img => img.decode());
      await page.keyboard.press('Escape');
    }
    assert.equal(await page.evaluate(() => localStorage.getItem('orbita2-wallet-v1')), null);
    for (const [width,height] of [[1440,1000],[768,1024],[390,844],[320,740]]) {
      await page.setViewportSize({width,height});
      await page.evaluate(() => scrollTo(0,0));
      await page.locator('.card-image img').evaluateAll(imgs => Promise.all(imgs.map(img => img.decode())));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.screenshot({path:'output/diario/atria-'+width+'.png',fullPage:true});
      await page.locator('.card-image').last().click();
      assert(await page.locator('#photo-viewer').evaluate(e => e.scrollWidth <= e.clientWidth));
      await page.screenshot({path:'output/diario/atria-popup-'+width+'.png'});
      await page.keyboard.press('Escape');
    }
    await page.locator('.back-planets').click();
    await page.locator('a[href="diario-planeta.html?planeta=aerivia"]').click();
    await page.waitForFunction(() => document.body.dataset.planet === 'aerivia');
    assert.equal(await page.locator('#planet-title').innerText(), 'Aerívia');
    assert.equal(await page.locator('.is-owned').count(), 12);
    assert.equal(await page.locator('.card-action').count(), 0);
    await page.locator('#read-full-story').click();
    assert.deepEqual(await page.locator('#full-story-content p').allTextContents(), await page.evaluate(() => ORBITA_DIARY.cards.map(c => c.text)));
    await page.keyboard.press('Escape');
    for (let i=0;i<12;i++) {
      await page.locator('.card-image').nth(i).click();
      assert.equal(await page.locator('#viewer-text').innerText(), await page.evaluate(i => ORBITA_DIARY.cards[i].text, i));
      await page.locator('#viewer-image').evaluate(img => img.decode());
      await page.keyboard.press('Escape');
    }
    assert.equal(await page.evaluate(() => localStorage.getItem('orbita2-wallet-v1')), null);
    for (const [width,height] of [[1440,1000],[768,1024],[390,844],[320,740]]) {
      await page.setViewportSize({width,height});
      await page.evaluate(() => scrollTo(0,0));
      await page.locator('.card-image img').evaluateAll(imgs => Promise.all(imgs.map(img => img.decode())));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Aerivia overflow ${width}`);
      await page.screenshot({path:`output/diario/aerivia-${width}.png`,fullPage:true});
      await page.locator('.card-image').last().click();
      assert(await page.locator('#photo-viewer').evaluate(e => e.scrollWidth <= e.clientWidth));
      await page.screenshot({path:`output/diario/aerivia-popup-${width}.png`});
      await page.keyboard.press('Escape');
    }
    await page.locator('.back-planets').click();
    await page.locator('a[href="diario-planeta.html?planeta=planeta-42"]').click();
    await page.waitForFunction(() => document.body.dataset.planet === 'planeta-42');
    assert.equal(await page.locator('#planet-title').innerText(), 'Planeta 42');
    assert.equal(await page.locator('.is-owned').count(), 12);
    assert.equal(await page.locator('.card-action').count(), 0);
    await page.locator('#read-full-story').click();
    assert.deepEqual(await page.locator('#full-story-content p').allTextContents(), await page.evaluate(() => ORBITA_DIARY.cards.map(c => c.text)));
    assert((await page.locator('#full-story-content').innerText()).includes('Nenhum matemático soube responder.'));
    await page.keyboard.press('Escape');
    for (let i=0;i<12;i++) {
      await page.locator('.card-image').nth(i).click();
      assert.equal(await page.locator('#viewer-text').innerText(), await page.evaluate(i => ORBITA_DIARY.cards[i].text, i));
      await page.locator('#viewer-image').evaluate(img => img.decode());
      await page.keyboard.press('Escape');
    }
    assert.equal(await page.evaluate(() => localStorage.getItem('orbita2-wallet-v1')), null);
    for (const [width,height] of [[1440,1000],[768,1024],[390,844],[320,740]]) {
      await page.setViewportSize({width,height});
      await page.evaluate(() => scrollTo(0,0));
      await page.locator('.card-image img').evaluateAll(imgs => Promise.all(imgs.map(img => img.decode())));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Planet 42 overflow ${width}`);
      await page.screenshot({path:`output/diario/planeta-42-${width}.png`,fullPage:true});
      await page.locator('.card-image').nth(2).click();
      assert(await page.locator('#photo-viewer').evaluate(e => e.scrollWidth <= e.clientWidth));
      await page.screenshot({path:`output/diario/planeta-42-popup-${width}.png`});
      await page.keyboard.press('Escape');
    }
    await page.locator('.back-planets').click();
    await page.locator('a[href="diario-planeta.html?planeta=mecano"]').click();
    await page.waitForFunction(() => document.body.dataset.planet === 'mecano');
    assert.equal(await page.locator('#planet-title').innerText(), 'Mecano');
    assert.equal(await page.locator('.is-owned').count(), 12);
    assert.equal(await page.locator('.card-action').count(), 0);
    await page.locator('#read-full-story').click();
    assert.deepEqual(await page.locator('#full-story-content p').allTextContents(), await page.evaluate(() => ORBITA_DIARY.cards.map(c => c.text)));
    await page.keyboard.press('Escape');
    for (let i=0;i<12;i++) {
      await page.locator('.card-image').nth(i).click();
      assert.equal(await page.locator('#viewer-text').innerText(), await page.evaluate(i => ORBITA_DIARY.cards[i].text, i));
      await page.locator('#viewer-image').evaluate(img => img.decode());
      await page.keyboard.press('Escape');
    }
    assert.equal(await page.evaluate(() => localStorage.getItem('orbita2-wallet-v1')), null);
    for (const [width,height] of [[1440,1000],[768,1024],[390,844],[320,740]]) {
      await page.setViewportSize({width,height});
      await page.evaluate(() => scrollTo(0,0));
      await page.locator('.card-image img').evaluateAll(imgs => Promise.all(imgs.map(img => img.decode())));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Mecano overflow ${width}`);
      await page.screenshot({path:`output/diario/mecano-${width}.png`,fullPage:true});
      await page.locator('.card-image').nth(9).click();
      assert(await page.locator('#photo-viewer').evaluate(e => e.scrollWidth <= e.clientWidth));
      await page.screenshot({path:`output/diario/mecano-popup-${width}.png`});
      await page.keyboard.press('Escape');
    }
    await page.locator('.back-planets').click();
    await page.locator('a[href="diario-planeta.html?planeta=lamalume"]').click();
    await page.waitForFunction(() => document.body.dataset.planet === 'lamalume');
    assert.equal(await page.locator('#planet-title').innerText(), 'Lamalume');
    assert.equal(await page.locator('.card-action').count(), 0);
    await page.locator('#read-full-story').click();
    assert(await page.locator('#full-story').evaluate(e => e.open));
    assert.deepEqual(await page.locator('#full-story-content p').allTextContents(), await page.evaluate(() => ORBITA_DIARY.cards.map(c=>c.text)));
    await page.screenshot({path:'output/diario/texto-integral-mobile.png'});
    await page.keyboard.press('Escape');
    assert(await page.locator('#read-full-story').evaluate(e => e === document.activeElement));
    for (let i=0;i<12;i++) {
      await page.locator('.card-image').nth(i).click();
      assert(await page.locator('#photo-viewer').evaluate(e => e.open));
      assert.equal(await page.locator('#viewer-text').innerText(), await page.evaluate(i => ORBITA_DIARY.cards[i].text, i));
      await page.locator('#viewer-image').evaluate(i => i.decode());
      await page.keyboard.press('Escape');
    }
    fs.mkdirSync('output/diario', {recursive:true});
    for (const [width,height] of [[1440,1000],[390,844],[320,740]]) {
      await page.setViewportSize({width,height});
      await page.evaluate(() => scrollTo(0,0));
      await page.locator('.card-image img').evaluateAll(imgs => Promise.all(imgs.map(i => i.decode())));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Lamalume overflow ${width}`);
      await page.screenshot({path:`output/diario/lamalume-${width}.png`,fullPage:true});
      await page.locator('.card-image').last().click();
      assert(await page.locator('#photo-viewer').evaluate(e => e.scrollWidth <= e.clientWidth));
      await page.screenshot({path:`output/diario/lamalume-popup-${width}.png`});
      await page.keyboard.press('Escape');
    }
    await page.locator('.back-planets').click();
    await page.locator('a[href="diario-planeta.html?planeta=umbralia"]').click();
    await page.reload();
    assert.equal(await page.locator('#planet-title').innerText(), 'Umbrália');
    await page.locator('#read-full-story').click();
    assert.deepEqual(await page.locator('#full-story-content p').allTextContents(), await page.evaluate(() => ORBITA_DIARY.cards.map(c=>c.text)));
    await page.locator('#full-story-close').click();
    assert.equal(await page.locator('.album-card').count(), 12);
    assert.equal(await page.locator('.is-owned').count(), 12);
    await page.locator('.card-image').last().click();
    assert(await page.locator('#photo-viewer').evaluate(e => e.open));
    assert.equal(await page.evaluate(() => localStorage.getItem('orbita2-wallet-v1')), null);
    await page.keyboard.press('Escape');
    // Exercise future paid mode without changing the app's unlocked default.
    await context.route('**/diario-data.js', async route => {
      const response = await route.fetch();
      await route.fulfill({response, body:(await response.text()).replace('previewUnlocked: true', 'previewUnlocked: false')});
    });
    await page.reload();
    await page.locator('.album-card').nth(1).locator('.card-image').click();
    assert(await page.locator('#notice').evaluate(e => e.open));
    await page.keyboard.press('Escape');
    await page.locator('#planet-action').click();
    await page.locator('#purchase-confirm').click();
    await page.waitForFunction(() => document.getElementById('purchase-error').textContent.includes('suficientes'));
    assert.equal(await page.evaluate(() => OrbitaWallet.snapshot().coins), 0);
    await page.locator('#purchase-cancel').click();
    // Seed only this isolated browser context; never give the real student test coins.
    await page.evaluate(() => {localStorage.setItem('orbita2-wallet-v1', JSON.stringify({coins:6150,purchases:[]})); OrbitaWallet.refresh();});
    await page.locator('#planet-action').click();
    await page.locator('#purchase-cancel').click();
    assert.equal(await page.evaluate(() => OrbitaWallet.snapshot().coins), 6150);
    await page.locator('#planet-action').click();
    await page.locator('#purchase-confirm').click();
    await page.waitForFunction(() => document.getElementById('photo-viewer').open);
    assert.equal(await page.evaluate(() => OrbitaWallet.snapshot().coins), 5500);
    assert((await page.locator('#viewer-text').innerText()).includes('bola de carvão'));
    await page.keyboard.press('Escape');
    await page.reload();
    assert.equal(await page.locator('.is-owned').count(), 1);
    await page.locator('.card-image').first().click();
    assert.equal(await page.evaluate(() => OrbitaWallet.snapshot().coins), 5500);
    await page.keyboard.press('Escape');
    for (let i=1;i<12;i++) {
      await page.locator('.card-image').nth(i).click();
      await page.locator('#purchase-confirm').click();
      await page.waitForFunction(() => document.getElementById('photo-viewer').open);
      assert.equal(await page.locator('#viewer-text').innerText(), await page.evaluate(i => ORBITA_DIARY.cards[i].text, i));
      await page.keyboard.press('Escape');
    }
    assert.equal(await page.evaluate(() => OrbitaWallet.snapshot().coins), 0);
    assert.equal(await page.locator('.is-owned').count(), 12);
    await page.locator('.card-image').first().click();
    await page.locator('#next-photo').click();
    assert.equal(await page.locator('#viewer-title').innerText(), 'A morte e a Gadanha');
    await page.keyboard.press('ArrowLeft');
    assert(await page.locator('#previous-photo').isDisabled());
    await page.keyboard.press('Escape');
    fs.mkdirSync('output/diario', {recursive:true});
    for (const [width,height] of [[1440,1000],[768,1024],[390,844],[320,740]]) {
      await page.setViewportSize({width,height});
      await page.evaluate(() => scrollTo(0,0));
      await page.locator('.card-image img').evaluateAll(imgs => Promise.all(imgs.map(i => i.decode())));
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `overflow ${width}`);
      await page.screenshot({path:`output/diario/album-${width}.png`,fullPage:true});
      await page.locator('.card-image').nth(8).click();
      await page.locator('#viewer-image').evaluate(i => i.decode());
      assert(await page.locator('#photo-viewer').evaluate(e => e.scrollWidth <= e.clientWidth), `dialog overflow ${width}`);
      await page.screenshot({path:`output/diario/popup-${width}.png`});
      await page.keyboard.press('Escape');
    }
    // Concurrent purchases in two tabs must only deduct once.
    await page.evaluate(() => {localStorage.setItem('orbita2-wallet-v1', JSON.stringify({coins:1150,purchases:[]})); OrbitaWallet.refresh();});
    const other = await context.newPage(); await other.goto('http://127.0.0.1:4179/diario-planeta.html?planeta=umbralia');
    await Promise.all([page,other].map(p => p.evaluate(() => OrbitaWallet.purchase('diary:umbralia:umbralia',650))));
    assert.equal(await page.evaluate(() => OrbitaWallet.snapshot().coins), 500);
    await other.close();
    // Storage failures must not claim a successful purchase.
    await page.evaluate(() => {Storage.prototype.setItem = () => {throw new Error('quota');};});
    assert.equal(await page.evaluate(async () => (await OrbitaWallet.purchase('diary:umbralia:a-morte',500,'diary:umbralia:umbralia')).ok), false);
    assert.equal(await page.evaluate(() => OrbitaWallet.snapshot().coins), 500);
    await page.reload();
    for(const file of ['index.html','avatar.html','mission.html']) {
      await page.goto(`http://127.0.0.1:4179/${file}`);
      assert.equal(await page.locator('a[href="diario.html"]').count(),1);
    }
    assert.deepEqual(errors, []);
    console.log('OK: 12 assets, prerequisite, insufficient funds, cancel, purchase, no double charge, persistence, full album, popup navigation, four widths, cross-tab locking, storage failure and menu links.');
  } finally {await browser.close();server.kill();}
})().catch(e => {console.error(e); process.exitCode=1;});

