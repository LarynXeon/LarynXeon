# MCQ slide extraction instructions

Directory: /tmp/claude-0/-home-user-LarynXeon/b4c2cc56-0c4f-5775-aa60-ba8786b426dd/scratchpad
Slides: mq/s-NNN.png (NNN = 3-digit slide number, e.g. mq/s-007.png). Each is a 1920x1080 slide from a Bengali SSC ICT MCQ guide.

There are two slide styles:
1. "REDWAN'S METHOD" style: question in grey bar, yellow bar with board/school names, options labelled A. B. C. D. The CORRECT answer is the option with a RED rectangle drawn around it.
2. "FINAL SHOT 2.0" style: question text at top left after a small box, board tag in square brackets like [ঢা.বো.২৩], options labelled (ক) (খ) (গ) (ঘ) in red circles with blue bars. The CORRECT answer is the option that has a WHITE DOT (●) to its right, and often also a yellow/gold rectangle around it. Hand-drawn pen marks (ticks, crosses, circles) are teacher annotations; a tick/cross on the option letter is NOT the answer marker. Use the white dot first, then yellow rectangle.

Other slide types: chapter title slides (text like "অধ্যায়: ০৩"), legend slides, slides with only handwritten notes, blank slides.

Stars: some questions have gold star icons near the question (importance). Count them exactly (0 if none). Also note stars on chapter title slides.

For EACH slide in your range, use the Read tool on the image, then append ONE JSON object per line to your output file (JSON Lines, UTF-8, Bengali Unicode not escaped is fine). Write the file with the Write tool once every ~10 slides (rewrite whole file content each time with all lines so far), so progress is never lost.

JSON fields:
{"slide": 7, "type": "mcq" | "title" | "note" | "other",
 "style": "redwan" | "finalshot" | null,
 "chapter_hint": "০৩" (only on title slides, else null),
 "qno": "৮" (question number printed, else null),
 "question": "full question text exactly as printed, including any i./ii./iii. statements on separate lines joined with \n and the stem like 'নিচের কোনটি সঠিক?'",
 "boards": "board/school tag text exactly, else null",
 "options": {"A": "...", "B": "...", "C": "...", "D": "..."},   (map ক=A, খ=B, গ=C, ঘ=D)
 "answer": "A" | "B" | "C" | "D" | null,
 "answer_confidence": "high" | "low",
 "stars": 0,
 "handwritten": "any readable handwritten note text (Bengali or English) on the slide, else null",
 "remarks": "anything unusual: e.g. two options marked, answer marker unclear, text unreadable"}

Rules:
- Copy Bengali text EXACTLY. Correct conjuncts (যুক্তাক্ষর) matter. Keep English words, code (Python like print(...), range(1,5,1)), formulas (=SUM(B1:B4)) exactly, including spaces, quotes, brackets.
- Never invent an answer. If no marker is visible, answer=null and say why in remarks.
- For "note" slides (handwritten only), put all readable text into "handwritten".
- Do not skip any slide. Every slide in the range must produce exactly one line.

At the end reply with: output file path, count of slides, count of mcq, count with answer=null or low confidence.
