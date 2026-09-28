# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = r"C:\Users\hardw\maistudy\gwihwa1000"

existing = json.load(open(BASE + r"\existing_543.json", encoding="utf-8"))

# category definitions: (title, old_n_lo, old_n_hi, new_file)
CATS = [
    ("대한민국 개관",              1,  57,  "01_대한민국개관_new.json"),
    ("한국사1 (고조선~조선전기)",   58, 113, "02_한국사1_new.json"),
    ("한국사2 (조선후기~일제강점기)", 114, 144, "03_한국사2_new.json"),
    ("현대사·남북관계",            145, 169, "04_현대사남북관계_new.json"),
    ("헌법·기본권·정치제도",        170, 235, "05_헌법정치제도_new.json"),
    ("정부조직·행정기관",           236, 293, "06_정부행정기관_new.json"),
    ("사법제도·생활법률",           294, 363, "07_사법생활법률_new.json"),
    ("가족·호칭·명절·세시풍속",     364, 410, "08_가족명절세시풍속_new.json"),
    ("전통문화·유산·예술",          411, 444, "09_전통문화유산예술_new.json"),
    ("국토·지리·계절",             445, 466, "10_국토지리계절_new.json"),
    ("의료·복지·교육·생활정보",     467, 547, "11_의료복지교육생활정보_new.json"),
]

final = []
n = 1
seen_q = {}
dupe_report = []

for title, lo, hi, fname in CATS:
    old_items = [c for c in existing if lo <= c["n"] <= hi]
    new_items = json.load(open(BASE + "\\categories\\" + fname, encoding="utf-8"))

    for c in old_items:
        q, a = c["q"].strip(), c["a"].strip()
        final.append({"n": n, "category": title, "q": q, "a": a, "source": "existing"})
        key = q.replace(" ", "")
        if key in seen_q:
            dupe_report.append((n, seen_q[key], q))
        seen_q[key] = n
        n += 1

    for c in new_items:
        q, a = c["q"].strip(), c["a"].strip()
        final.append({"n": n, "category": title, "q": q, "a": a, "source": "new"})
        key = q.replace(" ", "")
        if key in seen_q:
            dupe_report.append((n, seen_q[key], q))
        seen_q[key] = n
        n += 1

    print(f"{title}: existing={len(old_items)} new={len(new_items)} total={len(old_items)+len(new_items)}")

print(f"\nTOTAL: {len(final)}")

empties = [c["n"] for c in final if not c["q"] or not c["a"]]
print("empty q/a:", empties)

print(f"\nexact-duplicate question text pairs: {len(dupe_report)}")
for a, b, q in dupe_report:
    print(f"  #{b} == #{a}: {q}")

out = BASE + r"\qa_1000.json"
json.dump(final, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nwrote", out)
