"""Merge chapter JSON into the quiz app and the two printable HTML files."""
import json, base64, os, re, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(ROOT)
FONTS = os.path.join(KIT, "fonts")
OUT = os.environ.get("OUTDIR", os.path.join(KIT, "dist"))
os.makedirs(OUT, exist_ok=True)

BN = "০১২৩৪৫৬৭৮৯"
def bn(x): return re.sub(r"[0-9]", lambda m: BN[int(m.group())], str(x))
LBL = ["ক", "খ", "গ", "ঘ"]
DIFF = {1: 1.0, 2: 1.5, 3: 1.5, 4: 2.0, 5: 2.0, 6: 3.0}
NOTES_MIN, QUIZ_MIN, WRONG_MIN = 50, 55, 15

PATTERNS = {
    "def": {"n": "সংজ্ঞা/ধারণা", "tip": "বইয়ের সংজ্ঞার মূল শব্দটি খোঁজো। কাছাকাছি শোনায় এমন শব্দের বিকল্পটিই সাধারণ ফাঁদ।"},
    "full": {"n": "পূর্ণরূপ", "tip": "প্রতিটি অক্ষরের শব্দ মিলিয়ে দেখো। একটি শব্দ বদলে দেওয়া বিকল্পই ফাঁদ।"},
    "multi": {"n": "বহুপদী (i, ii, iii)", "tip": "প্রতিটি বাক্য আলাদা করে সত্য না মিথ্যা যাচাই করো। একটি বাক্য নিশ্চিত ভুল হলে সেটি থাকা সব বিকল্প বাদ দাও।"},
    "odd": {"n": "ব্যতিক্রম/কোনটি নয়", "tip": "প্রশ্নে 'নয়' বা 'ব্যতীত' আছে কিনা আবার পড়ো। তিনটি একই দলের, একটি আলাদা।"},
    "num": {"n": "সংখ্যা/সাল", "tip": "সাল ও সংখ্যা হুবহু মনে রাখো। কাছাকাছি সংখ্যাগুলোই ফাঁদ।"},
    "who": {"n": "ব্যক্তি/আবিষ্কারক", "tip": "কে কী করেছেন, জোড়া মিলিয়ে মনে রাখো।"},
    "code": {"n": "কোড/আউটপুট", "tip": "লাইন ধরে ধরে প্রতিটি ভ্যারিয়েবলের মান লিখে ট্রেস করো। লুপ কতবার চলে আর শর্ত কখন মিথ্যা হয়, সেটাই আসল।"},
    "use": {"n": "কাজ/ব্যবহার", "tip": "কোন টুল, মেনু বা কমান্ড কোন কাজে লাগে, জোড়া মেলাও।"},
    "scen": {"n": "উদ্দীপক/পরিস্থিতি", "tip": "উদ্দীপকের মূল তথ্য (সংখ্যা, শর্ত, ঘটনা) চিহ্নিত করে বইয়ের ধারণার সাথে মেলাও।"},
    "fact": {"n": "একক তথ্য", "tip": "বইয়ের বাক্যের সাথে হুবহু মেলে এমন বিকল্পটি বেছে নাও।"},
}

def nodash(s):
    if isinstance(s, str):
        s = s.replace(" — ", ", ").replace("—", "-").replace(" – ", ", ").replace("–", "-")
    return s

def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list): return [clean(v) for v in o]
    return nodash(o)

def load():
    chs = []
    for n in range(1, 7):
        p = os.path.join(os.environ.get("CHDIR", os.path.join(KIT, "build")), f"ch{n}.json")
        if not os.path.exists(p):
            print("missing", p); continue
        chs.append(clean(json.load(open(p, encoding="utf-8"))))
    return chs

def wordcount(N):
    t = []
    for s in N["notes"]["sections"]:
        t.append(s.get("h", ""))
        for it in s["items"]:
            t += [it.get("f", ""), it.get("c", ""), it.get("trap", "")]
    t += N["notes"]["must"]
    return len(" ".join(t).split())

def build_data(chs):
    tot = sum(c["mcq_total"] * DIFF[c["ch"]] for c in chs)
    chapters, cards, notes = [], [], {}
    for c in chs:
        n = c["ch"]; w = c["mcq_total"] * DIFF[n] / tot
        words = wordcount(c)
        chapters.append({"n": n, "title": c["title"], "pages": c["pages"], "w": round(w, 4),
                         "mcq": c["mcq_total"], "diff": DIFF[n],
                         "quizMin": max(2, round(w * QUIZ_MIN)), "notesMin": max(2, round(w * NOTES_MIN)),
                         "readMin": max(1, round(words / 150)), "words": words})
        for k in c["cards"] + c["new_cards"]:
            o = k["o"]
            assert len(o) == 4, (k["id"], o)
            assert 0 <= int(k["a"]) <= 3, k["id"]
            cards.append({"id": k["id"], "c": n, "q": k["q"].strip(), "o": [x.strip() for x in o], "a": int(k["a"]),
                          "r": 1 if k.get("r") else 0, "s": int(k.get("s") or 0), "st": bool(k.get("st")),
                          "b": (k.get("b") or "").strip(), "t": k.get("t") or "", "k": k.get("k") or "fact",
                          "l": k.get("l") or "", "p": k.get("p") or "", "f": k.get("f") or ""})
        notes[n] = {"sections": c["notes"]["sections"], "must": c["notes"]["must"]}
    order = sorted(chapters, key=lambda x: -x["w"])
    plan = []
    plan.append(["ধাপ ১: সব নোট পড়া (ওজন অনুযায়ী)", f"{bn(NOTES_MIN)} মিনিট"])
    for ch in order:
        plan.append([f"   অধ্যায় {bn(ch['n'])}: নোট {bn(ch['notesMin'])} মিনিট, কুইজ {bn(ch['quizMin'])} মিনিট", f"ওজন {bn(round(ch['w']*100))}%"])
    plan.append(["ধাপ ২: অনুশীলন, মিশ্র মোড", f"{bn(QUIZ_MIN)} মিনিট"])
    plan.append(["ধাপ ৩: শুধু ভুল মোড", f"{bn(WRONG_MIN)} মিনিট"])
    plan.append(["পরীক্ষার সকালে: সকালের ১৫ মিনিট মোড", "১৫ মিনিট"])
    return {"chapters": chapters, "cards": cards, "notes": notes, "patterns": PATTERNS, "plan": plan}

def b64(path): return base64.b64encode(open(path, "rb").read()).decode()

def font_css(embed=True):
    hs = FONTS
    ns = FONTS
    BEN = "U+0951-0952,U+0964-0965,U+0980-09FE,U+1CD0,U+1CD2,U+1CD5-1CD6,U+1CD8,U+1CE1,U+1CEA,U+1CED,U+1CF2,U+1CF5-1CF7,U+200C-200D,U+20B9,U+25CC,U+A8F1"
    LAT = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
    out = []
    def face(fam, w, path, rng):
        src = f"data:font/woff2;base64,{b64(path)}" if embed else "file://" + path
        out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url({src}) format('woff2');unicode-range:{rng}}}")
    for w in (400, 600, 700):
        face("Hind Siliguri", w, os.path.join(hs, f"hind-siliguri-bengali-{w}-normal.woff2"), BEN)
        face("Hind Siliguri", w, os.path.join(hs, f"hind-siliguri-latin-{w}-normal.woff2"), LAT)
    face("Noto Serif Bengali", 700, os.path.join(ns, "noto-serif-bengali-bengali-700-normal.woff2"), BEN)
    face("Kit Code Bn", 400, os.path.join(hs, "hind-siliguri-bengali-400-normal.woff2"), BEN)
    face("Kit Code Bn", 700, os.path.join(hs, "hind-siliguri-bengali-700-normal.woff2"), BEN)
    return "\n".join(out)

def build_app(data):
    tpl = open(os.path.join(ROOT, "app_template.html"), encoding="utf-8").read()
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    out = tpl.replace("/*__FONTS__*/", font_css(True)).replace("/*__DATA__*/null", js)
    p = os.path.join(OUT, "artifact.html")
    open(p, "w", encoding="utf-8").write(out)
    sa = os.path.join(OUT, "ict-exam-kit.html")
    open(sa, "w", encoding="utf-8").write('<!doctype html><html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>' + out + '</body></html>')
    return sa

E = html.escape

PRINT_CSS = """
@page{size:A4;margin:16mm 15mm 18mm 15mm;
  @bottom-center{content:"পৃষ্ঠা " counter(page, bengali);font-family:'Hind Siliguri';font-size:9pt;color:#555}}
html{font-family:'Hind Siliguri',sans-serif;font-size:10.5pt;line-height:1.5;color:#111}
body{margin:0}
h1{font-family:'Noto Serif Bengali','Hind Siliguri',serif;font-size:20pt;margin:0 0 4pt}
h2{font-family:'Noto Serif Bengali','Hind Siliguri',serif;font-size:15pt;margin:0 0 2pt;color:#004d39;break-after:avoid}
h3{font-size:11.5pt;margin:10pt 0 3pt;color:#006a4e;break-after:avoid}
.meta{color:#555;font-size:9pt;margin-bottom:6pt}
.ch{break-before:page}
.ch.first{break-before:auto}
.fact{padding:2pt 0;border-bottom:.4pt solid #ddd;break-inside:avoid}
.ft{font-weight:600}
.fc{color:#444;font-size:9.5pt}
.st{color:#b07800}
.pg{font-weight:700;white-space:nowrap;color:#004d39}
.trap{background:#fbf1d9;border-left:3pt solid #c58a00;padding:3pt 7pt;margin:4pt 0;break-inside:avoid;font-size:10pt}
.must{border:1.5pt solid #006a4e;border-radius:6pt;padding:5pt 10pt;margin:10pt 0;break-inside:avoid}
.must ol{margin:3pt 0 0;padding-left:18pt;list-style-type:bengali}
.unsure{color:#b05000;font-weight:700}
table{border-collapse:collapse;width:100%;font-size:9.5pt;margin:6pt 0}
td,th{border:.5pt solid #bbb;padding:3pt 5pt;text-align:left;vertical-align:top}
th{background:#eef3f0}
.q{break-inside:avoid;padding:4pt 0 5pt;border-bottom:.4pt solid #ddd}
.qt{font-weight:600;white-space:pre-wrap}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:1pt 14pt;margin-top:2pt}
.code{font-family:'Kit Code Bn',ui-monospace,Menlo,Consolas,'DejaVu Sans Mono',monospace}
.src{font-size:8.5pt;color:#666}
.les{break-inside:avoid;padding:3pt 0;border-bottom:.4pt solid #e2e2e2;font-size:9.8pt}
.cols{columns:2;column-gap:14pt}
.key{display:grid;grid-template-columns:repeat(8,1fr);gap:2pt 6pt;font-size:10pt;margin:4pt 0 10pt}
.key span{white-space:nowrap}
.flag{color:#8a4b00;font-size:9pt}
"""

def notes_html(data):
    chs = sorted(data["chapters"], key=lambda x: -x["w"])
    tw = sum(c["words"] for c in chs)
    h = [f"<!doctype html><html lang='bn'><head><meta charset='utf-8'><title>আইসিটি প্রি-রিড নোট</title><style>{font_css(False)}{PRINT_CSS}</style></head><body>"]
    h.append("<h1>আইসিটি প্রি-রিড নোট</h1>")
    h.append(f"<div class='meta'>নবম-দশম শ্রেণি, তথ্য ও যোগাযোগ প্রযুক্তি। ক্রম: পরীক্ষার ওজন অনুযায়ী (বেশি থেকে কম)। মোট প্রায় {bn(tw)} শব্দ, পড়তে প্রায় {bn(round(tw/150))} মিনিট (১৫০ শব্দ/মিনিট)। ★ = বোর্ড প্রশ্নে বারবার এসেছে। (পৃ. X) = পাঠ্যবইয়ের পৃষ্ঠা।</div>")
    h.append("<table><tr><th>অধ্যায়</th><th>বোর্ড MCQ</th><th>কাঠিন্য</th><th>ওজন</th><th>নোট পড়া</th><th>কুইজ</th></tr>")
    for c in chs:
        h.append(f"<tr><td>{bn(c['n'])}. {E(c['title'])}</td><td>{bn(c['mcq'])}</td><td>{bn(c['diff'])}</td><td>{bn(round(c['w']*100))}%</td><td>~{bn(c['readMin'])} মিনিট</td><td>{bn(c['quizMin'])} মিনিট</td></tr>")
    h.append("</table>")
    for i, c in enumerate(chs):
        N = data["notes"][c["n"]]
        h.append(f"<section class='ch{' first' if i == 0 else ''}'><h2>অধ্যায় {bn(c['n'])}: {E(c['title'])}</h2><div class='meta'>বইয়ের পৃষ্ঠা {E(c['pages'])} · ওজন {bn(round(c['w']*100))}% · পড়ার সময় ~{bn(c['readMin'])} মিনিট</div>")
        for s in N["sections"]:
            h.append(f"<h3>{E(s['h'])}</h3>")
            for it in s["items"]:
                if it.get("trap"):
                    h.append(f"<div class='trap'><b>ফাঁদ:</b> {E(it['trap'])}{' <span class=pg>(পৃ. '+E(it['p'])+')</span>' if it.get('p') else ''}</div>")
                else:
                    star = "<span class='st'>★ </span>" if it.get("star") else ""
                    uns = " <span class='unsure'>UNSURE</span>" if it.get("unsure") else ""
                    pg = f" <span class='pg'>(পৃ. {E(it['p'])})</span>" if it.get("p") else ""
                    ctx = f"<div class='fc'>{E(it['c'])}</div>" if it.get("c") else ""
                    h.append(f"<div class='fact'><div class='ft'>{star}{E(it['f'])}{pg}{uns}</div>{ctx}</div>")
        h.append("<div class='must'><b>অবশ্যই মনে রাখো</b><ol>" + "".join(f"<li>{E(m)}</li>" for m in N["must"]) + "</ol></div></section>")
    h.append("</body></html>")
    p = os.path.join(OUT, "notes.html"); open(p, "w", encoding="utf-8").write("".join(h)); return p

def quiz_html(data):
    chs = sorted(data["chapters"], key=lambda x: -x["w"])
    h = [f"<!doctype html><html lang='bn'><head><meta charset='utf-8'><title>আইসিটি কুইজ</title><style>{font_css(False)}{PRINT_CSS}</style></head><body>"]
    h.append("<h1>আইসিটি কুইজ: বোর্ড প্রশ্ন ও বই থেকে নতুন প্রশ্ন</h1>")
    h.append(f"<div class='meta'>মোট {bn(len(data['cards']))}টি প্রশ্ন। প্রতিটি অধ্যায়ে আগে বোর্ড প্রশ্ন, পরে বই থেকে নতুন প্রশ্ন। উত্তরমালা ও শিক্ষা আলাদা অংশে, শেষে।</div>")
    num = {}; i = 0
    for ci, c in enumerate(chs):
        cards = [k for k in data["cards"] if k["c"] == c["n"]]
        cards.sort(key=lambda k: (0 if k["r"] else 1))
        h.append(f"<section class='ch{' first' if ci == 0 else ''}'><h2>অধ্যায় {bn(c['n'])}: {E(c['title'])}</h2>")
        for k in cards:
            i += 1; num[k["id"]] = i
            code = " code" if k["k"] == "code" else ""
            src = ("বোর্ড: " + E(k["b"])) if k["r"] and k["b"] else ("বোর্ড প্রশ্ন" if k["r"] else "বই থেকে নতুন")
            star = " <span class='st'>★</span>" if k["st"] else ""
            h.append(f"<div class='q'><div class='qt{code}'>{bn(i)}. {E(k['q'])}{star}</div><div class='opts{code}'>" +
                     "".join(f"<span>{LBL[j]}. {E(o)}</span>" for j, o in enumerate(k["o"])) + f"</div><div class='src'>{src}</div></div>")
        h.append("</section>")
    h.append("<section class='ch'><h2>উত্তরমালা</h2>")
    for c in chs:
        cards = sorted([k for k in data["cards"] if k["c"] == c["n"]], key=lambda k: num[k["id"]])
        h.append(f"<h3>অধ্যায় {bn(c['n'])}</h3><div class='key'>" + "".join(f"<span>{bn(num[k['id']])}. {LBL[k['a']]}</span>" for k in cards) + "</div>")
    h.append("</section><section class='ch'><h2>শিক্ষা ও পৃষ্ঠা</h2>")
    for c in chs:
        cards = sorted([k for k in data["cards"] if k["c"] == c["n"]], key=lambda k: num[k["id"]])
        h.append(f"<h3>অধ্যায় {bn(c['n'])}</h3><div class='cols'>")
        for k in cards:
            fl = f"<div class='flag'>সতর্কতা: {E(k['f'])}</div>" if k["f"] else ""
            h.append(f"<div class='les'><b>{bn(num[k['id']])}. {LBL[k['a']]}. {E(k['o'][k['a']])}</b><br>{E(k['l'])} <span class='pg'>(পৃ. {E(k['p'])})</span> <span class='src'>[{E(PATTERNS.get(k['k'],{}).get('n',''))}]</span>{fl}</div>")
        h.append("</div>")
    h.append("</section></body></html>")
    p = os.path.join(OUT, "quiz.html"); open(p, "w", encoding="utf-8").write("".join(h)); return p

if __name__ == "__main__":
    chs = load()
    data = build_data(chs)
    json.dump(data, open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(build_app(data)); print(notes_html(data)); print(quiz_html(data))
    print("cards", len(data["cards"]), "real", sum(c["r"] for c in data["cards"]))
    for c in sorted(data["chapters"], key=lambda x: -x["w"]):
        print(c["n"], c["mcq"], c["w"], "words", c["words"], "read", c["readMin"], "quiz", c["quizMin"])
