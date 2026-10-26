# Chapter builder instructions (exam kit, Bengali SSC ICT)

You build ONE chapter of a last-minute exam kit for a student whose ICT MCQ exam is tomorrow (~25 MCQs, goal 25/25). Accuracy is the top priority. All output text is in Bengali, using the BOOK'S OWN WORDING. Keep English technical terms exactly as the book prints them (e.g. Compiler, URL, Ctrl+S, print(), =SUM(B1:B4)). Do not paraphrase away book terms.

Base directory: /tmp/claude-0/-home-user-LarynXeon/b4c2cc56-0c4f-5775-aa60-ba8786b426dd/scratchpad

## Inputs
- Book OCR text: `ocr/book/pNNN.txt` (NNN = PDF page, 3 digits). First line gives `printed=` page number. Printed page = PDF page - 5. ALWAYS cite the PRINTED page number in Bengali digits, e.g. (পৃ. ১১২).
- Book page images for verification: `bk/p-NNN.png` (full page) or `bkh/pNNNa.png` / `bkh/pNNNb.png` (top/bottom halves, sharper).
- IMPORTANT: the OCR was made by a weaker model. It is mostly exact but can contain occasional word substitutions (one found: "লক্ষ্য" printed in OCR where the book says "লঙ্ঘন"). Before you finalize any fact, lesson, or answer that depends on a specific word, number, name, year, shortcut, menu name, or code output, confirm it against the page IMAGE. You must view the image of every page you cite at least once.
- Board MCQs for your chapter: `build/ch/mcq_chN.json` (fields: slide, question, options A-D, answer letter, answer_confidence, stars, boards, handwritten, remarks). Slide images: `mq/s-NNN.png` (3-digit slide number). Two slide styles: "REDWAN'S METHOD" (answer = option with red rectangle) and "FINAL SHOT 2.0" (answer = option with a white dot at its right; a yellow rectangle is the teacher's highlight and usually matches). For every MCQ with answer_confidence "low", any remark about conflicting markers, covered text, or unreadable text: open the slide image and decide. Also open the slide image whenever the question/options text looks garbled.

## Your job
1. Read your chapter's OCR pages fully (list given in your task message). View the page images while working.
2. MCQ ANALYSIS. For every board MCQ:
   - Assign `topic` (short Bengali topic name, book heading wording where possible) and `k` (question type key, one of: def = সংজ্ঞা/ধারণা, full = পূর্ণরূপ, multi = বহুপদী সমাপ্তিসূচক (i, ii, iii), odd = ব্যতিক্রম/কোনটি নয়, num = সংখ্যা/সাল/পরিমাণ, who = ব্যক্তি/আবিষ্কারক, code = কোড/আউটপুট, use = কাজ/ব্যবহার/কোন টুল-মেনু-কমান্ড, scen = উদ্দীপক/পরিস্থিতি, fact = একক তথ্য কোনটি সঠিক).
   - Verify the answer key against the book (and for code: trace the code exactly as Python would run it). If the key looks wrong, or the book disagrees, or the book does not cover it at all, set `f` (flag) to a short Bengali explanation, e.g. "উত্তরমালায় খ দেওয়া, কিন্তু বই (পৃ. ১২৩) অনুযায়ী গ সঠিক।" and set `a` to the answer that is correct per the book (explain in the flag which one the key said). If the fact is not in the book at all, keep the key answer, add flag "বইয়ে সরাসরি নেই, গাইডের উত্তর রাখা হলো" and mark the lesson `UNSURE` with reason.
   - Write `l` (শিক্ষা, lesson learned): 1 to 2 short lines, CONTEXT-BASED: "সত্য যখন X. ভুল যখন Y." style where it helps (tell which fact fits which context, and why the main trap distractor is wrong). Book wording.
   - `p`: printed page(s) in Bengali digits, e.g. "১১২" or "১১২-১১৩".
   - `st`: true if the concept repeats in 2+ board MCQs (across the chapter) or the slide shows stars.
   - Clean the question and options text: fix obvious OCR glitches using the slide image, keep the board text in `b` (short form ok). Use `\n` between the stem and the i/ii/iii statements. Options as an array of 4 strings in order ক খ গ ঘ. `a` = 0-3.
   - Remove exact duplicate questions (same stem and same answer) but count them for repetition; keep the one with the clearest text and record `dup` count.
3. PATTERNS. Find repeated concepts, question types, distractor traps. Output top 10 repeated topics with counts.
4. PRE-READ NOTES (most important). Goal: the student reads ALL chapters' notes in 45 to 60 minutes total and knows everything needed for 25/25. Your chapter's word budget is given in the task message (Bengali words; reading speed 150 words/min). Build from two sources: (a) concepts in the book, (b) every concept, fact, and trap that appears in the board MCQs.
   - Organize in sections (book headings). Each item is ONE fact: `f` = short line (book wording, info dense), `c` = context line "সত্য যখন ... ভুল যখন ..." (1 line, only when it adds exam value; skip for plain facts), `p` = printed page, `star` = true if it repeats in MCQs.
   - Add `trap` items: look-alike terms and how to tell them apart (e.g. Compiler বনাম Interpreter). Include page.
   - Every board MCQ answer MUST be supported by some note item. Coverage check: after writing, go through every MCQ and confirm; list any unsupported ones in `coverage.unsupported` and FIX until it is empty.
   - Never invent. If unsure, add `"unsure": true` and say why in `c`.
   - End with `must`: exactly 5 lines, the "must remember" box.
   - No fluff, no intro sentences.
5. NEW MCQs from book facts: write the requested number of new MCQs in the SAME style as board MCQs (mix of types: def, full, multi i/ii/iii, odd, num, use, code for Ch6, scen). Target book facts that board MCQs miss. Every answer must be directly provable from the book page you cite (view the image). Same fields as real MCQs, `r`: 0.
6. SPOT CHECK: pick 10 random facts from your notes, re-open the page image, and confirm each word/number. Record them in `spot_check` with the exact book quote. Fix anything wrong.
7. Word count: count words of all `f` + `c` + trap + must text; report `word_count`.

## Style rules
- NEVER use the em dash (—) or en dash (–) anywhere in your output. Use a comma, colon, or plain hyphen (-) instead. If the book has an em dash in a quote, replace it with a hyphen.
- Bengali digits for page numbers and Bengali numbers in prose; keep code/formula digits as printed.
- Keep it short and dense. Easy reading level.

## Output
Write ONE JSON file `build/chN.json` (UTF-8, ensure_ascii false) with this exact shape, then validate it parses (e.g. `python3 -c "import json;json.load(open('build/chN.json'))"`):
```
{
 "ch": N,
 "title": "অধ্যায়ের নাম (book wording)",
 "pages": "১১০-১৩৫",
 "mcq_total": <number of board MCQ slides>,
 "type_counts": {"def": n, "full": n, ...},
 "top_topics": [{"topic": "...", "count": n, "note": "what is asked / which trap"}],   // 10 items
 "traps_summary": ["distractor trap pattern 1", "..."],
 "notes": {"sections": [{"h": "section heading", "items": [{"f": "...", "c": "...", "p": "১১২", "star": true}, {"trap": "X বনাম Y: ...", "p": "১১২"}]}],
           "must": ["...", "...", "...", "...", "..."]},
 "cards": [{"id": "6r001", "r": 1, "slide": 289, "q": "...", "o": ["...","...","...","..."], "a": 2, "key": "C",
            "b": "boards", "s": stars, "st": true, "t": "topic", "k": "code", "l": "lesson", "p": "১২৩", "f": "", "dup": 1}],
 "new_cards": [{"id": "6n001", "r": 0, "q": "...", "o": [...], "a": 1, "s": 0, "st": false, "t": "...", "k": "...", "l": "...", "p": "...", "f": ""}],
 "flags": [{"slide": 300, "issue": "short Bengali/English explanation"}],
 "coverage": {"checked": <number of MCQs checked>, "unsupported": []},
 "spot_check": [{"fact": "...", "p": "১১২", "book_quote": "...", "ok": true}],
 "word_count": n
}
```
`key` = the answer letter shown on the slide (A-D) so we can audit; `a` = the index you believe is correct per the book.
When finished, reply with a short summary: counts, flags list, word_count, anything UNSURE.
