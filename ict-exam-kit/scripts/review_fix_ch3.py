import json, sys

P = sys.argv[1]
d = json.load(open(P, encoding='utf-8'))

def item(sec_h, start):
    for s in d['notes']['sections']:
        if s['h'] == sec_h:
            for it in s['items']:
                t = it.get('f') or it.get('trap')
                if t.startswith(start):
                    return it
    raise KeyError(start)

# ---- Notes ----
it = item('ডিজিটাল কনটেন্ট', 'প্রধান চারটি ভাগ')
it['f'] = 'প্রধান চারটি ভাগ: (১) টেক্সট বা লিখিত কনটেন্ট (২) ছবি (৩) শব্দ বা অডিয়ো এবং (৪) ভিডিয়ো ও অ্যানিমেশন।'
it['c'] = "সত্য যখন 'কত প্রকার' = ৪ (ভিডিয়ো ও অ্যানিমেশন মিলে একটি ভাগ)। ভুল যখন ৫ (ই-বুকের ভাগ)।"

it = item('ডিজিটাল কনটেন্ট', 'লিখিত (পরিমাণে বেশি)')
it['f'] = 'লিখিত (পরিমাণে বেশি): নিবন্ধ, ব্লগ পোস্ট, পণ্য বা সেবার তালিকা ও বর্ণনা, পণ্যের মূল্যায়ন, ই-বুক, সংবাদপত্র, শ্বেতপত্র।'

it = item('ডিজিটাল কনটেন্ট', 'ছবি: ফটো')
it['f'] = 'ছবি: ফটো, হাতে আঁকা ছবি, কার্টুন, ইনফো-গ্রাফিক্স, অ্যানিমেটেড ছবি। শব্দ = অডিয়ো কনটেন্ট।'

it = item('বইয়ে সরাসরি নেই (বোর্ড MCQ)', 'ই-মেইল = ইলেকট্রনিক মেইল')
it['c'] = "ভুল যখন ইলেকট্রিক্যাল। পূর্ণরূপ বইয়ে নেই; তুলনা: ই-বুক = ইলেকট্রনিক বুক (পৃ. ৪৪)।"

it = item('ওয়েব ব্রাউজার ও শব্দাবলি', 'URL (Uniform Resource Locator)')
it['c'] = "'URL কী' প্রশ্নে ভুল যখন প্রটোকল (একটি অংশ মাত্র)। 'অংশ নয়' = Bookmark।"

d['notes']['must'][0] = 'ডিজিটাল কনটেন্ট প্রধান চারটি ভাগ: (১) টেক্সট বা লিখিত (২) ছবি (৩) শব্দ বা অডিয়ো (৪) ভিডিয়ো ও অ্যানিমেশন; ব্লগ/শ্বেতপত্র = লিখিত; সরাসরি প্রচার = ভিডিয়ো স্ট্রিমিং।'

d['traps_summary'][0] = 'সংখ্যা গুলানো: ডিজিটাল কনটেন্ট প্রধান চারটি ভাগ (ভিডিয়ো ও অ্যানিমেশন একটি ভাগ) বনাম ই-বুক পাঁচটি ভাগ।'

# ---- Board cards ----
C = {c['id']: c for c in d['cards']}
c = C['3r001']
c['l'] = "সত্য যখন ব্লগ (বইয়ের লিখিত কনটেন্টের তালিকায় 'ব্লগ পোস্ট')। ভুল যখন শুধু বই/পত্রিকা (মুদ্রিত রূপ) বা ব্রডব্যান্ড (সংযোগ, কনটেন্ট নয়)।"
c = C['3r002']
c['l'] = 'সত্য যখন ডিজিটাল কনটেন্ট = প্রধান চারটি ভাগ (ভিডিয়ো ও অ্যানিমেশন মিলে একটি)। ভুল যখন ৫ (৫ হলো ই-বুকের ভাগ)।'
c = C['3r003']
c['o'][3] = 'মডেম'
c['l'] = 'চারটি ভাগ: টেক্সট, ছবি, শব্দ বা অডিয়ো, এবং ভিডিয়ো ও অ্যানিমেশন; ক-গ সবই কনটেন্ট। যন্ত্র বা সংযোগ (মডেম) কনটেন্ট নয়।'
c['f'] = "ঘ অপশনটি স্লাইডে হাতে লেখা; 'মডেম' পড়া হয়েছে (পুরো নিশ্চিত নয়)। ক-গ তিনটিই বইয়ের কনটেন্ট প্রকার, তাই উত্তর ঘ অপরিবর্তিত।"
c = C['3r010']
c['l'] = "সত্য যখন 'কেবল অনলাইনে তথা ইন্টারনেটে পড়া যায়' = এইচটিএমএল (HTML), এদের বলে 'বই-এর ওয়েবসাইট'। CMYK, RGB, CSB বইয়ের ই-বুক ফরম্যাটে নেই।"
c = C['3r019']
c['l'] = 'UNSURE (পূর্ণরূপ বইয়ে নেই): ই-মেইল = ইলেকট্রনিক মেইল, যেমন ই-বুক = ইলেকট্রনিক বুক (পৃ. ৪৪)। ভুল যখন ইলেকট্রিক্যাল।'

# ---- New cards: rebalance answer positions ----
N = {c['id']: c for c in d['new_cards']}
def reorder(cid, new_opts):
    c = N[cid]
    right = c['o'][c['a']]
    assert sorted(new_opts) == sorted(c['o']), cid
    c['o'] = new_opts
    c['a'] = new_opts.index(right)

reorder('3n007', ['ওয়েব পেইজ ও হোম পেইজ', 'ব্রাউজার ও সার্চ ইঞ্জিন', 'URL ও Bookmark', 'ওয়েব সার্ভার ও ওয়েব ক্লায়েন্ট'])
reorder('3n009', ['www.bangladesh.gov.bd', 'www.shikkha.com', 'www.google.com/maps', 'forms.gov.bd'])
reorder('3n010', ['Transfer Control Protocol/Internet Protocol', 'Text Control Protocol/Internet Protocol', 'Transmission Control Protocol/Internet Protocol', 'Transmission Control Program/Internet Program'])
reorder('3n011', ['টিম বার্নার্স লি', 'রেমন্ড স্যামুয়েল টমলিনসন', 'গুগলিয়েলমো মার্কনি', 'জেমস ক্লার্ক ম্যাক্সওয়েল'])

# ---- word count ----
wc = 0
for s in d['notes']['sections']:
    for it in s['items']:
        for k in ('f', 'c', 'trap'):
            wc += len(it.get(k, '').split())
for m in d['notes']['must']:
    wc += len(m.split())
d['word_count'] = wc

s = json.dumps(d, ensure_ascii=False, indent=1)
assert '—' not in s and '–' not in s
open(P, 'w', encoding='utf-8').write(s)
json.load(open(P, encoding='utf-8'))
from collections import Counter
print('new_card a dist', Counter('কখগঘ'[c['a']] for c in d['new_cards']))
print('word_count', wc)
