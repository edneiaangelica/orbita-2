const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try {
  const page=await browser.newPage({isMobile:true,hasTouch:true});
  fs.mkdirSync('output/mobile',{recursive:true});
  for(const [width,height] of [[320,568],[390,844],[430,932]]){
   await page.setViewportSize({width,height});await page.goto('http://127.0.0.1:4173/index.html');
   await page.emulateMedia({reducedMotion:'reduce'});
   const scene=await page.locator('.scene').boundingBox(),intro=await page.locator('.intro').boundingBox(),actions=await page.locator('.actions').boundingBox();
   assert(scene.y+scene.height<=intro.y+1,'Scene before intro');assert(intro.y+intro.height<=actions.y+1,'Intro before actions');
   assert(actions.y+actions.height<=Math.max(height,660),'Buttons fit viewport or short-screen scroll area');
   const title=await page.locator('h1').boundingBox();assert(title.y<100,'Title near top');assert(scene.height>=220,'Animation has room');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   await page.screenshot({path:`output/mobile/opening-${width}.png`,fullPage:true});
  }
  await page.goto('http://127.0.0.1:4173/mission.html');await page.locator('#trail-challenges [data-challenge]').first().click();
  for(const [width,height] of [[568,320],[667,375],[844,390],[932,430]]){
   await page.setViewportSize({width,height});
   const video=await page.locator('#lesson').boundingBox(),nav=await page.locator('.header-nav').boundingBox();
   assert(video.height>=height-60,'Video uses screen height');assert(video.x+video.width<=nav.x+1,'Video clear of sidebar');
   const controls=page.locator('.header-nav .menu-icon, .toolbar .icon-button, #start-questions');
   const boxes=await Promise.all((await controls.all()).map(e=>e.boundingBox()));
   for(const box of boxes)assert(box.x>=nav.x&&box.y>=0&&box.x+box.width<=width+1&&box.y+box.height<=height+1,'Control within sidebar');
   for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const a=boxes[i],b=boxes[j];assert(a.x+a.width<=b.x+1||b.x+b.width<=a.x+1||a.y+a.height<=b.y+1||b.y+b.height<=a.y+1,'Controls do not overlap');}
   await page.screenshot({path:`output/mobile/lesson-${width}.png`});
  }
  await page.locator('#start-questions').click();assert(await page.locator('#learning-view').isVisible());
  await page.locator('#review-lesson').click();await page.setViewportSize({width:390,height:844});
  const nav=await page.locator('.header-nav').boundingBox();assert(Math.abs(nav.y+nav.height-844)<2,'Portrait restores bottom navigation');
  console.log('OK: opening order and visible buttons; landscape video, accessible nonoverlapping sidebar; questions and portrait return.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
