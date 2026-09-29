# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PATH = r"C:\Users\hardw\maistudy\gwihwa1000\qa_1000.json"
data = json.load(open(PATH, encoding="utf-8"))
byn = {c["n"]: c for c in data}

def set_qa(n, q=None, a=None):
    c = byn[n]
    if q is not None:
        c["q"] = q
    if a is not None:
        c["a"] = a

# ---------- A. 신규 문항 오류 (수정 필수) ----------
set_qa(57, a="3대 2입니다.")
set_qa(71,
    q="2008년에 공휴일에서 제외되었다가 2026년에 다시 공휴일로 지정된 국경일은 무엇입니까?",
    a="제헌절(7월 17일)입니다.")
set_qa(73, a="1935년입니다.")
set_qa(607, a="지식재산처(옛 특허청)입니다.")
set_qa(770, a="형님입니다.")
set_qa(916, a="전라남도, 전북특별자치도, 경상남도에 걸쳐 있습니다.")
set_qa(933, a="강원도 대관령, 경상북도 울릉도 등이 있습니다.")
set_qa(1028, q="아동에게 매달 지급되는 정부의 대표적인 현금성 지원을 무엇이라 합니까?")

# ---------- B. 신규 문항 보완 권장 ----------
set_qa(59, a="양(陽)의 기운을 상징합니다.")
set_qa(172, q="조선 건국 초, 한양으로 옮기기 전의 도읍은 어디였습니까?")
set_qa(173, q="조선의 정궁인 경복궁을 세운 왕은 누구입니까?")
set_qa(267, a="시천주 사상입니다(이후 3대 교주 손병희 때 인내천 사상으로 발전했습니다).")
set_qa(414, a="북한이탈주민(탈북민)입니다.")
set_qa(416, a="도라전망대, 오두산 통일전망대 등이 있습니다.")
set_qa(533, a="주민조례발안제(주민발안제)입니다.")
set_qa(599, q="국가안보 관련 정책을 대통령에게 자문하는 헌법상 기구는 어디입니까?")
set_qa(689, a="징역형(자유형)입니다.")
set_qa(693, q="법원의 영장에 따라 피의자나 피고인을 일정 기간 가두는 것을 무엇이라 합니까?")
set_qa(700, a="직계비속(자녀 등)이며, 배우자는 공동으로 상속받습니다.")
set_qa(774, a="남자는 제수(계수), 여자는 올케라고 부릅니다.")
set_qa(776, a="여자는 제부, 남자는 매부(매제)라고 부릅니다.")
set_qa(1022, q="만 65세 이상에게 지하철(도시철도) 요금을 면제해주는 제도를 무엇이라 합니까?")
set_qa(1027, a="가족센터(옛 다문화가족지원센터)입니다.")

# ---------- C. 346(→671) 추정 답변 수정 ----------
set_qa(671, a="가족관계등록부입니다.")
byn[671]["guess"] = True

# ---------- E. 기존 543문항 중 시점이 지났거나 틀린 항목 ----------
set_qa(553, a="이재명 대통령입니다.")
set_qa(555, a="청와대입니다.")
set_qa(569, a="성평등가족부입니다.")
set_qa(570, q="환경·기후·에너지 관련 업무를 담당하는 행정부의 부처는 어디입니까?", a="기후에너지환경부입니다.")
set_qa(574, q="산업, 통상, 무역 등에 관련된 업무를 하는 행정부의 부처는 어디입니까?", a="산업통상부입니다.")
set_qa(577, a="예산은 기획예산처, 경제정책·세제는 재정경제부가 담당합니다.")
set_qa(587, a="국가데이터처(옛 통계청)입니다.")
set_qa(598, a="방송미디어통신위원회입니다.")
set_qa(656, a="1억원입니다.")
set_qa(983, q="원금과 이자를 합쳐 1인당 최고 1억원까지 보호받는 제도는 무엇입니까?")
set_qa(904,
    q="대한민국에는 6개의 도가 있습니다. 모두 말해보세요.",
    a="경기도, 충청북도, 충청남도, 전라남도, 경상북도, 경상남도입니다.")
set_qa(903, a="제주특별자치도, 강원특별자치도, 전북특별자치도입니다.")
set_qa(235, q="1940년 김구가 중국에서 독립전쟁을 벌이는 독립군을 바탕으로 조직한 단체의 이름은 무엇입니까?")
set_qa(135, a="혼천의입니다.")
set_qa(638, a="삼심제도입니다.")
set_qa(515, a="대통령 직선제입니다.")

# 국무총리(현직자, 변동 잦음) - 삭제 권장
DELETE_VOLATILE = {557}

# ---------- D. 중복 제거 (16쌍, "삭제" 권장 대상) ----------
DELETE_DUPES = {
    2, 77, 914, 535, 74, 83, 382, 427, 922, 716, 79, 86, 444, 76, 449,
    426,  # (14행: 표현조정 대신 삭제로 단순화)
}

TO_DELETE = DELETE_VOLATILE | DELETE_DUPES
print("deleting", len(TO_DELETE), "items:", sorted(TO_DELETE))

kept = [c for c in data if c["n"] not in TO_DELETE]
for i, c in enumerate(kept, start=1):
    c["n"] = i

print("final total:", len(kept))

empties = [c["n"] for c in kept if not c["q"].strip() or not c["a"].strip()]
print("empty q/a:", empties)

seen = {}
dupes = []
for c in kept:
    key = c["q"].replace(" ", "")
    if key in seen:
        dupes.append((seen[key], c["n"], c["q"]))
    seen[key] = c["n"]
print("remaining exact-duplicate questions:", len(dupes))
for a, b, q in dupes:
    print(" ", a, b, q)

json.dump(kept, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", PATH)
