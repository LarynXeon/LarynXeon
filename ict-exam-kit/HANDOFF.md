# ICT exam kit: handoff (read this first)

Goal: SSC ICT MCQ exam, 25 MCQs, 6 chapters, 2 hours. Build a Bengali notes PDF, quiz PDF, and quiz app. Accuracy first. All text Bengali in book wording, English terms kept, page numbers (পৃ. X), no em dashes.

## What is DONE (all in this folder)
- `ocr/book/pNNN.txt`: OCR of all 140 book pages (PDF page N, printed page = N - 5). Made by Haiku. Mostly exact, some word slips. Verify against `images/book/p-NNN.jpg` when a fact matters. Already fixed: p040 "লঙ্ঘন", p008 "কৃত্রিম", ঙ্গে artifacts.
- `ocr/all_slides.json`: all 385 MCQ slides extracted (question, options A-D, answer letter, confidence, stars, remarks). Slide images: `images/slides/s-NNN.jpg`. Style REDWAN = red box is the key; FINAL SHOT = white dot at right of option is the key.
- 375 board MCQs. Chapter split by slide: Ch1 3-40 (37), Ch2 41-120 (80), Ch3 122-142 (21), Ch4 144-211 (68), Ch5 213-286 (72), Ch6 288-385 (97). Per chapter files: `build/ch/mcq_chN.json`.
- Weights = MCQ count x difficulty (1,1.5,1.5,2,2,3): Ch6 38%, Ch5 19%, Ch4 18%, Ch2 16%, Ch1 5%, Ch3 4%.
- `build/ch1.json` to `ch4.json`: finished chapter data (notes, board cards with lessons, new cards, flags). Ch3 is independently reviewed (`build/review_ch3.md`). Ch1, Ch2, Ch4 are built but NOT reviewed.
- `scripts/app_template.html` + `scripts/build.py`: quiz app (tested with a headless browser: auto spaced repetition, themes, settings, modes, Bengali fonts) and the notes/quiz HTML for PDFs.
- `dist/`: partial build from Ch1-4 only (notes.pdf, quiz.pdf, ict-exam-kit.html). Weights/times in it are wrong until Ch5 and Ch6 are added (weights are computed from loaded chapters only).

## What is NOT done
1. `build/ch5.json` and `build/ch6.json` (Ch6 is the heaviest, 38%). Build them with `scripts/CHAPTER_INSTRUCTIONS.md` (full spec of the JSON format and rules). `scripts/gen_ch6.py` is a partial, unfinished draft of the Ch6 cards (traced code answers); reuse it if useful, do not trust it blindly.
   - Book pages: Ch5 PDF 69-114 (printed ৬৪-১০৯), Ch6 PDF 115-140 (printed ১১০-১৩৫).
2. Review Ch1, Ch2, Ch4 with `scripts/REVIEW_INSTRUCTIONS.md`. Known items to resolve:
   - Ch1 slide 15 (Maxwell): key says তড়িৎ, builder changed to তড়িৎচৌম্বক (book পৃ. ৪). Slide 13: stem 1842, book says 1840.
   - Ch2 slide 54 (ডিস্ক ক্লিনআপ): key গ "কম্পিউটারের গতি বাড়ানো", builder changed to খ. Real board key may be গ. Decide and flag both.
   - Ch4: formula questions 189, 193, 195, 204-207, 210, 211 (book teaches =A3*B3% style; SUM not in book). Many UNSURE lessons are facts the book does not cover.
   - Ch6 known conflicts (answer marker disagree): slides 341, 343, 357, 358, 380, 381, 318, 328 (trace the Python code exactly). Book p.১৩৩ continue example output looks wrong in print (omits 6, same-line text).
3. Rebuild: `python3 scripts/build.py` then `node scripts/make_pdf.js dist/notes.html dist/notes.pdf dist/quiz.html dist/quiz.pdf` (needs playwright). Test app: `node scripts/test_app.js <abs path to dist/ict-exam-kit.html> <shots dir>`.
4. Final checks asked by the user: 10 random OCR pages vs images (done for ~8, fine), spot check 10 facts per chapter, coverage (every MCQ answer supported by notes), total notes reading time 45-60 min (150 words/min; Ch1-4 notes are about 3,900 words, so Ch5+Ch6 notes should total about 3,400 words or less).

## Rules the user set
- Haiku for OCR/tagging/low-level work. Heavy thinking by a strong model, but BUDGET IS TIGHT: use Sonnet, few agents, no Opus swarm.
- Never invent facts. Unsure = mark UNSURE with reason. Flag wrong answer keys.
- Bengali only, book wording; English terms as in book. No em dash. Easy words. Brief.
- Deliver: notes PDF, quiz PDF (answer key and lessons separate), single-file quiz app (artifact), with dark/light mode.

## Source files
Original uploads were a split zip (book PDF 140 pages, MCQ deck PDF 385 slides) and are not in git (too big). Page/slide JPEGs are in `images/`.
