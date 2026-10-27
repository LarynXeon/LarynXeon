const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const pg=await (await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2})).newPage();
 const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
 await pg.goto('file://'+process.argv[2]); await pg.waitForTimeout(400);
 const cur=()=>pg.evaluate(()=>{const k=window.__kit.cur(); return {id:k.c.id,pos:k.order.indexOf(k.c.a),wrong:k.order.findIndex(o=>o!==k.c.a)}});
 const st=id=>pg.evaluate(id=>{const s=window.__kit.S.cs[id];return s?{m:s.m,w:s.w,d:s.d,last:s.last}:null},id);
 const log=[];
 // card1: correct first time
 let c1=await cur(); await pg.click('#opt'+c1.pos); log.push(['c1 right',c1.id,JSON.stringify(await st(c1.id))]); await pg.click('#nextBtn');
 // card2: wrong
 let c2=await cur(); await pg.click('#opt'+c2.wrong); log.push(['c2 wrong',c2.id,JSON.stringify(await st(c2.id))]); await pg.click('#nextBtn');
 const seq=[]; let back=null;
 for(let i=0;i<6;i++){ const c=await cur(); seq.push(c.id); if(c.id===c2.id){ back=i+1; await pg.click('#opt'+c.pos); await pg.click('#nextBtn'); break;} await pg.click('#opt'+c.pos); await pg.click('#nextBtn'); }
 log.push(['c2 returned after cards',back,JSON.stringify(await st(c2.id))]);
 // run 60 more, ensure c1 and c2 never reappear
 let again=0; for(let i=0;i<60;i++){ const c=await cur(); if(c.id===c1.id||c.id===c2.id) again++; await pg.click('#opt'+c.pos); await pg.click('#nextBtn'); }
 log.push(['repeat of mastered in next 60',again]);
 log.forEach(l=>console.log(l.join(' | ')));
 await pg.click('#tab-set'); console.log('swatches', await pg.locator('#sAccent button').count());
 await pg.screenshot({path:process.argv[3]+'/sw.png'});
 console.log('errors',errs.join(';')||'none'); await b.close();
})();
