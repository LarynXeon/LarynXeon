const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const pg=await (await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2})).newPage();
 const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
 await pg.goto('file://'+process.argv[2]); await pg.waitForTimeout(400);
 await pg.click('#tab-set');
 for (const v of [10,25,50,100,200,500]) {
   await pg.evaluate(v=>{const r=document.querySelector('#sCount'); r.value=v; r.dispatchEvent(new Event('input',{bubbles:true})); r.dispatchEvent(new Event('change',{bubbles:true}));}, v);
   const t=await pg.evaluate(()=>{const k=window.__kit; const sel=k.selected? k.selected():null; return [document.querySelector('#cntVal').textContent, document.querySelector('#cntEst').textContent]});
   console.log(v, t.join(' | '));
 }
 await pg.evaluate(()=>{const r=document.querySelector('#sCount'); r.value=50; r.dispatchEvent(new Event('input',{bubbles:true})); r.dispatchEvent(new Event('change',{bubbles:true}));});
 await pg.screenshot({path:process.argv[3]+'/count.png'});
 await pg.click('#tab-quiz'); await pg.waitForTimeout(200);
 console.log(await pg.textContent('#stLeft'), '|', await pg.textContent('#brandSub'));
 // play through whole 50-set answering correctly, count distinct cards
 const seen=new Set(); 
 for(let i=0;i<80;i++){
   const st=await pg.evaluate(()=>{const k=window.__kit.cur(); return k&&!k.answered?{id:k.c.id,pos:k.order.indexOf(k.c.a)}:null});
   if(!st) break; seen.add(st.id); await pg.click('#opt'+st.pos); await pg.click('#nextBtn');
 }
 console.log('distinct cards served', seen.size, 'mastered', await pg.textContent('#stLeft'));
 console.log('errors', errs.join(';')||'none'); await b.close();
})();
