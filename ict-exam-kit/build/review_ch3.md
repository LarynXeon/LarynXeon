# Review log: Chapter 3 (ইন্টারনেট ও ওয়েব পরিচিতি), build/ch3.json

Sources viewed: book images PDF 48-56 (printed ৪৩-৫১, halves for 48-55, full page 56); slides 122-142 (via montages ch3_mont0-3, cross-checked against mq/s-124.png and mq/s-142.png; crops ch3_s124D.png, ch3_s125C.png).
Cards checked: 21 board + 15 new = 36. All 21 slide keys match `a`. No answer changed.

## Fixes

### A. Digital content classification (extra check 1)
Book p. ৪৩ (image): "তবে, ডিজিটাল কনটেন্টকে প্রধান চারটি ভাগে ভাগ করা যায়।" Bullets: টেক্সট বা লিখিত কনটেন্ট / ছবি / শব্দ বা অডিয়ো এবং / ভিডিয়ো ও অ্যানিমেশন। So it is 4 parts, and "ভিডিয়ো ও অ্যানিমেশন" is ONE part.
1. must[0]: said "৪ প্রকার: টেক্সট, ছবি, অডিয়ো, ভিডিয়ো ও অ্যানিমেশন" (read as 5 items). Rewrote as "প্রধান চারটি ভাগ: (১) টেক্সট বা লিখিত (২) ছবি (৩) শব্দ বা অডিয়ো (৪) ভিডিয়ো ও অ্যানিমেশন".
2. Notes item (ডিজিটাল কনটেন্ট, "প্রধান চারটি ভাগ"): same comma list; renumbered with book wording; `c` now says ভিডিয়ো ও অ্যানিমেশন মিলে একটি ভাগ.
3. Card 3r003 `l`: same 5-looking list; rewrote as "চারটি ভাগ: টেক্সট, ছবি, শব্দ বা অডিয়ো, এবং ভিডিয়ো ও অ্যানিমেশন".
4. Card 3r002 `l`: added "(ভিডিয়ো ও অ্যানিমেশন মিলে একটি)".
5. traps_summary[0]: "৪ প্রকার" changed to "প্রধান চারটি ভাগ (ভিডিয়ো ও অ্যানিমেশন একটি ভাগ)" vs ই-বুক পাঁচটি ভাগ.
(top_topics note "কত প্রকার (৪)" and 3n004 lesson "চারটি ভাগ" were already right.)

### B. New cards answer balance (extra check 2)
Before: ক3 খ8 গ3 ঘ1. After: ক4 খ4 গ4 ঘ3. Options reordered, `a` updated, same option text:
- 3n007 (ওয়েবসাইটের দুটি অংশ): খ to ঘ.
- 3n009 (forms.gov.bd): খ to ঘ.
- 3n010 (TCP/IP পূর্ণরূপ): খ to গ.
- 3n011 (টিম বার্নার্স লি): খ to ক.
I did not reorder the multi cards (3n003, 3n006) or the number card (3n004), so the i/ii/iii options and the ascending numbers stay in their usual order.

### C. Text and lesson accuracy
- 3r003 option ঘ: "মডেম (হাতে লেখা)" changed to "মডেম"; the handwriting note moved into `f` (still marked not fully certain).
- 3r001 `l`: removed the claim "সবসময় ডিজিটাল", which is not in the book. It now cites the book list ('ব্লগ পোস্ট') (p. ৪৩).
- 3r010 `l`: "CMYK, RGB ফরম্যাট নয়" (not a book statement) changed to "CMYK, RGB, CSB বইয়ের ই-বুক ফরম্যাটে নেই".
- 3r019 `l`: reworded. It is still UNSURE, now with the ই-বুক analogy page (পৃ. ৪৪).
- Notes, লিখিত কনটেন্ট item: "পণ্যের তালিকা ও মূল্যায়ন" changed to book wording "পণ্য বা সেবার তালিকা ও বর্ণনা, পণ্যের মূল্যায়ন" (p. ৪৩).
- Notes, ছবি item: added "হাতে আঁকা ছবি" from the book list (p. ৪৩).
- Notes, URL item `c`: now covers both board forms: 'URL কী' (trap: প্রটোকল) and 'অংশ নয়' = Bookmark (p. ৫০).
- Notes, ই-মেইল UNSURE item `c`: names the page of the analogy (ই-বুক = ইলেকট্রনিক বুক, পৃ. ৪৪). It still says the full form is not in the book.

### D. Style and format
- No em or en dash found before or after the fixes. JSON parses. Every card has 4 distinct options.
- word_count: 526 to 568 (+42, mostly the numbered list markers and the restored book wording). Still near budget.

## Spot check (reviewer, against page images)
1. p. ৪৩: "ডিজিটাল কনটেন্টকে প্রধান চারটি ভাগে ভাগ করা যায়।" OK
2. p. ৪৩: "ভিডিয়ো ও অ্যানিমেশন" is a single bullet. OK
3. p. ৪৩: "...ঘটনার ভিডিয়ো সরাসরি প্রচারিত হয়ে থাকে। এটিকে বলা হয় ভিডিয়ো স্ট্রিমিং।" OK
4. p. ৪৪: "অ্যামাজন ডটকমের (amazon.com) কিন্ডল (kindle) সবচেয়ে জনপ্রিয়।" OK
5. p. ৪৪: "পিডিএফ (পোর্টেবল ডকুমেন্ট ফরম্যাট)" for হুবহু প্রতিলিপি. OK
6. p. ৪৪: EPUB for "নোট লেখা, শব্দের অর্থ জানা". OK
7. p. ৪৫: "দ্রুত গতির বেশি ব্যান্ডউইথের (bandwidth) ইন্টারনেট" (no definition of bandwidth). OK
8. p. ৪৭: "'বাংলাদেশ জাতীয় তথ্য বাতায়ন' পোর্টালটির (www.bangladesh.gov.bd)". OK
9. p. ৪৮: "TCP/IP (Transmission Control Protocol/Internet Protocol)"; "forms.gov.bd অ্যাড্রেসে". OK
10. p. ৪৯: "১৯৯০ সালে টিম বার্নার্স লি WorldWideWeb নামে সর্বপ্রথম ওয়েব ব্রাউজার তৈরি করেন।" OK
11. p. ৫০: URL parts "(১) প্রোটোকলের নাম, (২) হোস্টনেইম ও (৩) ফাইলের অবস্থানসহ নাম"; "ডাইনামিক ওয়েব পেজের জন্য Reload / Refresh কমান্ড খুব গুরুত্বপূর্ণ". OK
12. p. ৫১: the sample questions have no printed answers. ICT প্রধান উপকরণ = কম্পিউটার stays UNSURE. OK

## Coverage
All 21 board MCQs are backed by a note item (checked one by one; 142 Bookmark is now explicit in the URL `c`). coverage.unsupported = [].

## Remaining UNSURE (kept flagged honestly)
- 3r013 / notes: ব্যান্ডউইথ = ডেটা প্রবাহের হার. The book only mentions bandwidth (p. ৪৫) and gives no definition. The guide key B is kept.
- 3r019 / notes: ই-মেইল = ইলেকট্রনিক মেইল. The full form is not in the book. The guide key B is kept, by analogy with ই-বুক = ইলেকট্রনিক বুক (p. ৪৪).
- Notes: ICT এর প্রধান উপকরণ = কম্পিউটার. This is a book sample question (p. ৫১) with no printed answer.
- 3r003 option ঘ is handwritten on the slide and read as 'মডেম'. The answer ঘ is certain either way.
