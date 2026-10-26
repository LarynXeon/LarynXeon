# Independent review instructions (exam kit chapter)

You are the independent reviewer for ONE chapter of a Bengali SSC ICT exam kit. Another model built `build/chN.json`. Your job is to find and FIX errors. Accuracy is the top priority; the student wants 25/25 tomorrow.

Base directory: /tmp/claude-0/-home-user-LarynXeon/b4c2cc56-0c4f-5775-aa60-ba8786b426dd/scratchpad
Read `CHAPTER_INSTRUCTIONS.md` first to learn the data format and rules.

Sources of truth:
- Book page images `bk/p-NNN.png` / `bkh/pNNNa.png`, `bkh/pNNNb.png` (PDF page = printed page + 5). OCR text `ocr/book/pNNN.txt` is a helper only; it can contain word substitutions.
- Slide images `mq/s-NNN.png` for board MCQs (REDWAN style: red rectangle = key; FINAL SHOT style: white dot right of option = key).

Check, for EVERY card in `cards` and `new_cards`:
1. `a` is correct per the book (and for code, per exact Python 3 execution; run the code with `python3 -I -c` in a scratch dir if useful). If `a` differs from the slide key (`key`), there must be a clear flag `f` saying what the key says and why the book says otherwise.
2. The lesson `l` is true, in book wording, context-based, 1 to 2 lines, and its page `p` is the right printed page (open the image to confirm).
3. Question/options text is clean (no OCR garbage), 4 options, no duplicate options, exactly one correct answer. For i/ii/iii questions, check every statement.
4. New cards: answer provable from the cited page; no ambiguity; style like board MCQs.
Check the notes:
5. Every fact `f`/`c`/trap: true per the book, page right. Spot check at least 10 random facts against images (record them).
6. Coverage: every board MCQ's answer is supported by a note item. Add missing items briefly.
7. Style: NO em dash (—) or en dash (–) anywhere. Bengali digits for pages. Book terms kept.
8. In `new_cards`, spread correct answers across ক/খ/গ/ঘ roughly evenly (reorder options and update `a`; keep "i, ii ও iii" style option sets in their natural order). Do not reorder board cards.
9. Every number/count stated in notes must match the items listed (e.g. "৪ প্রকার" must list exactly 4).
10. Word count of notes stays near the builder's (do not bloat; tighten if far over budget).

Fix problems directly in `build/chN.json` (keep the same schema; validate it parses). Write a short log `build/review_chN.md` listing each fix (card id or note item, what was wrong, what you changed, page). If something cannot be decided, mark it UNSURE in the lesson/flag with the reason rather than guessing.

Reply with: number of cards checked, number of fixes by type, list of remaining UNSURE items.
