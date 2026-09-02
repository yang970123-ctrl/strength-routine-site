# -*- coding: utf-8 -*-
"""
오늘의 근력루틴 - 운동 가이드 페이지 빌드 스크립트

사용법:
  1. 아래 EXERCISES 리스트에 운동을 추가/수정한다.
  2. python3 build.py 실행 -> exercises/*.html, bodyweight.html, equipment.html 자동 생성.

주방시간 사이트와 동일한 "데이터 리스트 + 템플릿" 구조입니다.
"""

import os

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
EXERCISES_DIR = os.path.join(SITE_ROOT, "exercises")

CATEGORY_LABEL = {
    "bodyweight": "맨몸운동",
    "equipment": "기구운동",
}
CATEGORY_ICON = {
    "bodyweight": "🤸",
    "equipment": "🏋️",
}

# ---------------------------------------------------------------------------
# 음식별 칼로리 데이터 (1인분 기준) - 이 리스트만 채우면 food-calories.html 자동 생성
# ---------------------------------------------------------------------------
FOODS = [
    {"name": "흰쌀밥 (1공기, 210g)", "kcal": 300},
    {"name": "현미밥 (1공기, 210g)", "kcal": 290},
    {"name": "계란 1개 (완숙)", "kcal": 78},
    {"name": "닭가슴살 100g", "kcal": 165},
    {"name": "삼겹살 100g", "kcal": 331},
    {"name": "두부 100g", "kcal": 84},
    {"name": "바나나 1개", "kcal": 105},
    {"name": "사과 1개", "kcal": 95},
    {"name": "고구마 100g (찐)", "kcal": 118},
    {"name": "김밥 1줄", "kcal": 450},
    {"name": "라면 1개 (조리)", "kcal": 500},
    {"name": "삼각김밥 1개", "kcal": 180},
    {"name": "아메리카노 (톨)", "kcal": 10},
    {"name": "우유 200ml", "kcal": 130},
    {"name": "그릭요거트 100g", "kcal": 97},
    {"name": "고등어 구이 100g", "kcal": 205},
    {"name": "된장찌개 1인분", "kcal": 150},
    {"name": "김치찌개 1인분", "kcal": 200},
    {"name": "샐러드 (드레싱 포함) 1접시", "kcal": 220},
    {"name": "아보카도 1/2개", "kcal": 120},
    {"name": "아몬드 10알", "kcal": 70},
    {"name": "떡볶이 1인분", "kcal": 480},
    {"name": "치킨 (후라이드) 100g", "kcal": 260},
    {"name": "프로틴쉐이크 1스쿱", "kcal": 120},
]

# ---------------------------------------------------------------------------
# 스포츠/운동별 칼로리 소모 데이터 (MET 값 기준) - 체중 x MET x 시간(h) x 1.05
# ---------------------------------------------------------------------------
SPORTS = [
    {"name": "걷기 (보통 속도)", "met": 3.5},
    {"name": "달리기 (8km/h)", "met": 8.3},
    {"name": "달리기 (10km/h)", "met": 9.8},
    {"name": "수영 (자유형, 보통)", "met": 8.3},
    {"name": "수영 (여유롭게)", "met": 5.8},
    {"name": "농구 (경기)", "met": 8.0},
    {"name": "축구 (경기)", "met": 7.0},
    {"name": "자전거 타기 (보통)", "met": 6.8},
    {"name": "등산", "met": 6.0},
    {"name": "줄넘기", "met": 10.0},
    {"name": "배드민턴", "met": 5.5},
    {"name": "테니스 (복식)", "met": 6.0},
    {"name": "요가", "met": 2.5},
    {"name": "계단 오르기", "met": 8.8},
    {"name": "클라이밍 (실내)", "met": 7.5},
    {"name": "복싱 (스파링)", "met": 9.0},
    {"name": "스쿼시", "met": 7.3},
    {"name": "인라인스케이트", "met": 7.0},
    {"name": "골프 (걸어서)", "met": 4.8},
]

# ---------------------------------------------------------------------------
# 분할법 루틴 데이터 - exercise_id는 EXERCISES 리스트의 id와 매칭되어 자동 링크됨
# 문자열만 넣으면 (매칭되는 운동이 없으면) 링크 없이 텍스트로만 표시됨
# ---------------------------------------------------------------------------
SPLITS = {
    "none": {
        "label": "무분할",
        "intro": "매 훈련일마다 전신을 자극합니다. 주 2~3회, 훈련 간 최소 하루는 휴식하는 것을 권장합니다.",
        "days": [
            {
                "name": "전신 A",
                "items": [
                    ("squat", "5세트 x 5회"),
                    ("bench-press", "5세트 x 5회"),
                    ("lat-pulldown", "4세트 x 10회"),
                    ("plank", "3세트 x 40초"),
                ],
            },
            {
                "name": "전신 B",
                "items": [
                    ("deadlift", "5세트 x 5회"),
                    ("overhead-press", "4세트 x 8회"),
                    ("pullup", "4세트 x 최대반복"),
                    ("bodyweight-squat", "3세트 x 15회"),
                ],
            },
        ],
    },
    "2way": {
        "label": "2분할",
        "intro": "상체/하체로 나누어 훈련합니다. 주 4회(상-하-상-하) 진행 시 부위별로 주 2회씩 자극할 수 있습니다.",
        "days": [
            {
                "name": "상체",
                "items": [
                    ("bench-press", "4세트 x 8회"),
                    ("lat-pulldown", "4세트 x 10회"),
                    ("overhead-press", "3세트 x 10회"),
                    ("pullup", "3세트 x 최대반복"),
                ],
            },
            {
                "name": "하체",
                "items": [
                    ("squat", "5세트 x 5회"),
                    ("deadlift", "3세트 x 6회"),
                    ("bodyweight-squat", "3세트 x 20회"),
                    ("plank", "3세트 x 40초"),
                ],
            },
        ],
    },
    "3way": {
        "label": "3분할",
        "intro": "밀기(Push)·당기기(Pull)·하체(Legs)로 나누는 대표적인 3분할입니다. 주 3~6회 (PPL 반복) 진행 가능합니다.",
        "days": [
            {
                "name": "Push (가슴·어깨·삼두)",
                "items": [
                    ("bench-press", "4세트 x 8회"),
                    ("overhead-press", "4세트 x 8회"),
                    ("pushup", "3세트 x 최대반복"),
                ],
            },
            {
                "name": "Pull (등·이두)",
                "items": [
                    ("deadlift", "4세트 x 6회"),
                    ("lat-pulldown", "4세트 x 10회"),
                    ("pullup", "3세트 x 최대반복"),
                ],
            },
            {
                "name": "Legs (하체·코어)",
                "items": [
                    ("squat", "5세트 x 5회"),
                    ("bodyweight-squat", "3세트 x 20회"),
                    ("plank", "3세트 x 40초"),
                ],
            },
        ],
    },
    "4way": {
        "label": "4분할",
        "intro": "부위를 세분화해 회복 시간을 늘리는 방식입니다. 중~고급자에게 적합하며 주 4회 진행합니다.",
        "days": [
            {
                "name": "가슴 · 삼두",
                "items": [
                    ("bench-press", "5세트 x 6회"),
                    ("pushup", "3세트 x 최대반복"),
                ],
            },
            {
                "name": "등 · 이두",
                "items": [
                    ("deadlift", "4세트 x 6회"),
                    ("lat-pulldown", "4세트 x 10회"),
                    ("pullup", "3세트 x 최대반복"),
                ],
            },
            {
                "name": "하체",
                "items": [
                    ("squat", "5세트 x 5회"),
                    ("bodyweight-squat", "3세트 x 20회"),
                ],
            },
            {
                "name": "어깨 · 코어",
                "items": [
                    ("overhead-press", "4세트 x 8회"),
                    ("plank", "3세트 x 40초"),
                    ("burpee", "3세트 x 15회"),
                ],
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# 운동 데이터 : 이 리스트만 채우면 상세 페이지 + 카테고리 목록이 자동 생성됨
# ---------------------------------------------------------------------------
EXERCISES = [
    # ---- 맨몸운동 ----
    {
        "id": "pushup",
        "name": "푸시업",
        "category": "bodyweight",
        "target": "가슴, 삼두, 어깨",
        "difficulty": "초급",
        "desc": "장비 없이 가슴과 삼두를 자극하는 대표적인 맨몸운동입니다.",
        "steps": [
            "손을 어깨너비보다 약간 넓게 벌리고 플랭크 자세를 잡는다.",
            "몸을 일직선으로 유지한 채 팔꿈치를 굽혀 가슴이 바닥에 가까워질 때까지 내려간다.",
            "가슴과 삼두의 힘으로 밀어 올려 시작 자세로 돌아온다.",
        ],
        "tips": [
            "허리가 꺾이지 않도록 복부에 힘을 유지한다.",
            "팔꿈치는 몸통에서 약 45도 각도를 유지한다.",
        ],
    },
    {
        "id": "pullup",
        "name": "풀업",
        "category": "bodyweight",
        "target": "광배근, 이두, 전완",
        "difficulty": "중급",
        "desc": "철봉에 매달려 등 전체를 발달시키는 상체 대표 운동입니다.",
        "steps": [
            "철봉을 어깨너비보다 약간 넓게 오버그립으로 잡는다.",
            "어깨를 아래로 당기며 몸을 끌어올려 턱이 봉을 넘게 한다.",
            "천천히 팔을 펴며 시작 자세로 내려온다.",
        ],
        "tips": [
            "몸이 흔들리지 않도록 코어에 힘을 준다.",
            "처음에는 밴드나 어시스트 머신으로 보조해도 좋다.",
        ],
    },
    {
        "id": "bodyweight-squat",
        "name": "맨몸 스쿼트",
        "category": "bodyweight",
        "target": "대퇴사두, 둔근",
        "difficulty": "초급",
        "desc": "하체 기본기를 다지는 맨몸 스쿼트입니다. 웨이트 스쿼트 전 필수 학습 동작입니다.",
        "steps": [
            "발을 어깨너비로 벌리고 발끝을 살짝 바깥으로 향한다.",
            "무릎과 엉덩이를 동시에 굽히며 앉듯이 내려간다.",
            "허벅지가 바닥과 평행해지면 발바닥 전체로 밀며 일어난다.",
        ],
        "tips": [
            "무릎이 발끝 방향과 같은 선을 유지하도록 한다.",
            "시선은 정면을 유지해 상체 숙임을 방지한다.",
        ],
    },
    {
        "id": "plank",
        "name": "플랭크",
        "category": "bodyweight",
        "target": "코어 전체",
        "difficulty": "초급",
        "desc": "코어 안정성을 기르는 등척성(isometric) 운동입니다.",
        "steps": [
            "팔꿈치를 어깨 아래에 두고 엎드린다.",
            "발끝으로 지지하며 머리부터 발끝까지 일직선을 만든다.",
            "정해진 시간 동안 자세를 유지한다.",
        ],
        "tips": [
            "엉덩이가 위로 뜨거나 아래로 처지지 않도록 한다.",
            "호흡을 멈추지 말고 자연스럽게 유지한다.",
        ],
    },
    {
        "id": "burpee",
        "name": "버피",
        "category": "bodyweight",
        "target": "전신, 심폐지구력",
        "difficulty": "중급",
        "desc": "전신 근력과 심폐지구력을 동시에 단련하는 고강도 맨몸운동입니다.",
        "steps": [
            "선 자세에서 스쿼트로 앉아 손을 바닥에 짚는다.",
            "다리를 뒤로 뻗어 플랭크 자세를 만든다.",
            "다시 다리를 당겨오고 점프하며 일어선다.",
        ],
        "tips": [
            "속도보다 정확한 자세를 우선한다.",
            "심박수가 많이 오르므로 초심자는 세트 사이 충분히 휴식한다.",
        ],
    },
    # ---- 기구운동 ----
    {
        "id": "bench-press",
        "name": "벤치프레스",
        "category": "equipment",
        "target": "가슴, 삼두, 어깨",
        "difficulty": "중급",
        "desc": "바벨을 이용해 가슴 근력을 발달시키는 3대 운동 중 하나입니다.",
        "steps": [
            "벤치에 누워 견갑골을 모으고 가슴을 살짝 든다.",
            "바를 가슴 중앙 위로 내려 살짝 터치한 뒤 밀어 올린다.",
            "팔이 완전히 펴지기 직전까지 밀어 올려 반복한다.",
        ],
        "tips": [
            "손목이 꺾이지 않도록 바를 손바닥 위에 수직으로 둔다.",
            "고중량 시 반드시 보조자를 두거나 세이프티바를 사용한다.",
        ],
    },
    {
        "id": "squat",
        "name": "바벨 스쿼트",
        "category": "equipment",
        "target": "대퇴사두, 둔근, 코어",
        "difficulty": "중급",
        "desc": "바벨을 이용해 하체 전체를 강화하는 3대 운동 중 하나입니다.",
        "steps": [
            "바를 승모근 위에 얹고 랙에서 들어 올려 스쿼트 랙을 빠져나온다.",
            "발을 어깨너비로 벌리고 무릎과 엉덩이를 굽혀 앉는다.",
            "허벅지가 바닥과 평행해지면 발바닥으로 밀며 일어난다.",
        ],
        "tips": [
            "가슴을 펴고 허리 중립을 유지한다.",
            "무릎이 안으로 모이지 않도록 주의한다.",
        ],
    },
    {
        "id": "deadlift",
        "name": "데드리프트",
        "category": "equipment",
        "target": "등, 둔근, 햄스트링",
        "difficulty": "고급",
        "desc": "바닥의 바벨을 들어올려 후면 사슬 전체를 강화하는 3대 운동 중 하나입니다.",
        "steps": [
            "바 앞에 서서 정강이가 바에 거의 닿을 정도로 다가선다.",
            "허리를 중립으로 유지하며 엉덩이를 뒤로 빼고 바를 잡는다.",
            "바닥을 밀어내듯 다리와 엉덩이 힘으로 일어선다.",
        ],
        "tips": [
            "바가 몸에서 멀어지지 않도록 최대한 몸에 붙여 든다.",
            "허리가 둥글게 말리지 않도록 각별히 주의한다.",
        ],
    },
    {
        "id": "overhead-press",
        "name": "오버헤드프레스",
        "category": "equipment",
        "target": "어깨, 삼두, 코어",
        "difficulty": "중급",
        "desc": "바벨을 머리 위로 밀어 올려 어깨 근력을 키우는 운동입니다.",
        "steps": [
            "바를 쇄골 앞에 걸치듯 잡고 선다.",
            "코어에 힘을 준 채 바를 머리 위로 곧게 밀어 올린다.",
            "팔이 완전히 펴지면 천천히 시작 위치로 내린다.",
        ],
        "tips": [
            "허리가 과도하게 꺾이지 않도록 둔근과 복부에 힘을 준다.",
            "바가 얼굴을 스치듯 최단 경로로 밀어 올린다.",
        ],
    },
    {
        "id": "lat-pulldown",
        "name": "랫풀다운",
        "category": "equipment",
        "target": "광배근, 이두",
        "difficulty": "초급",
        "desc": "머신을 이용해 풀업 동작을 보조된 중량으로 연습할 수 있는 운동입니다.",
        "steps": [
            "패드에 허벅지를 고정하고 바를 어깨너비보다 넓게 잡는다.",
            "가슴을 펴고 견갑골을 내리며 바를 쇄골까지 당긴다.",
            "천천히 팔을 펴며 시작 위치로 돌아온다.",
        ],
        "tips": [
            "몸을 뒤로 젖히기보다 등 힘으로 당기는 느낌에 집중한다.",
            "반동을 최소화하고 광배근 수축을 느끼며 진행한다.",
        ],
    },
    {
        "id": "leg-press",
        "name": "레그프레스",
        "category": "equipment",
        "target": "대퇴사두, 둔근, 햄스트링",
        "difficulty": "초급",
        "desc": "머신에 앉아 안전하게 하체 전체를 강화할 수 있는 운동입니다.",
        "steps": [
            "시트에 앉아 발판에 발을 어깨너비로 올린다.",
            "무릎을 굽혀 발판을 몸쪽으로 당겨온다.",
            "발바닥 전체로 밀어내며 다리를 편다 (무릎은 완전히 펴지 않는다).",
        ],
        "tips": [
            "무릎이 안쪽으로 모이지 않도록 주의한다.",
            "허리가 시트에서 뜨지 않는 범위까지만 내린다.",
        ],
    },
    {
        "id": "barbell-row",
        "name": "바벨로우",
        "category": "equipment",
        "target": "광배근, 승모근, 이두",
        "difficulty": "중급",
        "desc": "상체를 숙인 자세로 바벨을 당겨 등 두께를 키우는 운동입니다.",
        "steps": [
            "무릎을 살짝 굽히고 상체를 45도 정도 숙인다.",
            "바벨을 어깨너비로 잡고 배꼽 방향으로 당긴다.",
            "등 근육의 수축을 느끼며 천천히 내린다.",
        ],
        "tips": [
            "허리가 둥글게 말리지 않도록 중립을 유지한다.",
            "반동을 최소화하고 등 힘으로 당긴다.",
        ],
    },
    {
        "id": "dumbbell-curl",
        "name": "덤벨컬",
        "category": "equipment",
        "target": "이두근",
        "difficulty": "초급",
        "desc": "덤벨을 이용해 이두근을 고립시켜 발달시키는 운동입니다.",
        "steps": [
            "덤벨을 양손에 들고 팔을 자연스럽게 내린다.",
            "팔꿈치를 고정한 채 덤벨을 어깨 방향으로 감아올린다.",
            "천천히 시작 자세로 내린다.",
        ],
        "tips": [
            "몸의 반동을 이용하지 않고 이두근 힘으로만 든다.",
            "팔꿈치 위치가 훈련 중 앞뒤로 흔들리지 않게 고정한다.",
        ],
    },
    {
        "id": "lunge",
        "name": "런지",
        "category": "bodyweight",
        "target": "대퇴사두, 둔근, 균형감각",
        "difficulty": "초급",
        "desc": "한 다리씩 번갈아 딛으며 하체와 균형 감각을 함께 훈련하는 운동입니다.",
        "steps": [
            "선 자세에서 한쪽 발을 크게 앞으로 내딛는다.",
            "양 무릎이 90도가 될 때까지 몸을 낮춘다.",
            "앞발로 밀어 시작 자세로 돌아온 뒤 반대쪽을 반복한다.",
        ],
        "tips": [
            "앞 무릎이 발끝을 넘지 않도록 주의한다.",
            "상체는 곧게 세운 상태를 유지한다.",
        ],
    },
    {
        "id": "mountain-climber",
        "name": "마운틴클라이머",
        "category": "bodyweight",
        "target": "코어, 심폐지구력",
        "difficulty": "초급",
        "desc": "플랭크 자세에서 무릎을 빠르게 당겨 코어와 심폐지구력을 함께 단련합니다.",
        "steps": [
            "플랭크 자세로 시작한다.",
            "한쪽 무릎을 가슴 쪽으로 빠르게 당긴다.",
            "발을 원위치하며 반대쪽 무릎을 당기는 동작을 반복한다.",
        ],
        "tips": [
            "엉덩이가 위로 솟구치지 않도록 코어에 힘을 유지한다.",
            "속도보다 정확한 자세를 우선한다.",
        ],
    },
    {
        "id": "crunch",
        "name": "크런치",
        "category": "bodyweight",
        "target": "복직근",
        "difficulty": "초급",
        "desc": "복부 상부를 집중적으로 자극하는 기본 코어 운동입니다.",
        "steps": [
            "바닥에 누워 무릎을 세우고 손을 귀 옆이나 가슴에 둔다.",
            "복부 힘으로 상체를 말아 올린다.",
            "천천히 시작 자세로 내려온다.",
        ],
        "tips": [
            "목을 손으로 당기지 않고 복부 힘으로만 들어올린다.",
            "허리는 바닥에서 크게 뜨지 않게 유지한다.",
        ],
    },
]

# ---------------------------------------------------------------------------
# 랜덤 루틴 생성기용 메타데이터
# muscle_group: 하체 / 가슴 / 등 / 어깨 / 팔 / 코어 / 전신
# sets/reps: 생성 시 무작위로 뽑힐 범위
# bw_mult: {난이도: 체중 대비 권장 중량 배수} - 기구운동에만 존재 (참고용 추정치)
# ---------------------------------------------------------------------------
GENERATOR_META = {
    "pushup":            {"muscle_group": "가슴", "sets": [3, 4], "reps": [10, 20]},
    "pullup":            {"muscle_group": "등",   "sets": [3, 4], "reps": [5, 12]},
    "bodyweight-squat":  {"muscle_group": "하체", "sets": [3, 4], "reps": [15, 25]},
    "plank":             {"muscle_group": "코어", "sets": [3, 4], "reps": [30, 60], "unit": "초"},
    "burpee":            {"muscle_group": "전신", "sets": [3, 4], "reps": [10, 20]},
    "lunge":             {"muscle_group": "하체", "sets": [3, 4], "reps": [10, 16]},
    "mountain-climber":  {"muscle_group": "코어", "sets": [3, 4], "reps": [20, 40]},
    "crunch":            {"muscle_group": "코어", "sets": [3, 4], "reps": [15, 25]},
    "bench-press":       {"muscle_group": "가슴", "sets": [3, 5], "reps": [6, 10],
                           "bw_mult": {"초급": 0.4, "중급": 0.65, "고급": 0.9}},
    "squat":             {"muscle_group": "하체", "sets": [3, 5], "reps": [5, 8],
                           "bw_mult": {"초급": 0.6, "중급": 0.95, "고급": 1.35}},
    "deadlift":          {"muscle_group": "하체", "sets": [3, 5], "reps": [4, 6],
                           "bw_mult": {"초급": 0.7, "중급": 1.05, "고급": 1.5}},
    "overhead-press":    {"muscle_group": "어깨", "sets": [3, 4], "reps": [6, 10],
                           "bw_mult": {"초급": 0.25, "중급": 0.4, "고급": 0.55}},
    "lat-pulldown":      {"muscle_group": "등",   "sets": [3, 4], "reps": [8, 12],
                           "bw_mult": {"초급": 0.35, "중급": 0.55, "고급": 0.75}},
    "leg-press":         {"muscle_group": "하체", "sets": [3, 4], "reps": [10, 15],
                           "bw_mult": {"초급": 0.8, "중급": 1.3, "고급": 1.8}},
    "barbell-row":       {"muscle_group": "등",   "sets": [3, 4], "reps": [8, 12],
                           "bw_mult": {"초급": 0.35, "중급": 0.55, "고급": 0.75}},
    "dumbbell-curl":     {"muscle_group": "팔",   "sets": [3, 4], "reps": [10, 15],
                           "bw_mult": {"초급": 0.08, "중급": 0.12, "고급": 0.18}},
}
MUSCLE_GROUPS = ["하체", "가슴", "등", "어깨", "팔", "코어", "전신"]


def page_shell(title, description, active_nav, body_html, extra_head="", base_path="../"):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="manifest" href="{base_path}manifest.json">
<link rel="stylesheet" href="{base_path}css/style.css">
{extra_head}
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8486360926248718" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
{body_html}
<div class="ad-slot">
  <ins class="adsbygoogle"
    style="display:block; width:100%;"
    data-ad-client="ca-pub-8486360926248718"
    data-ad-slot="0000000000"
    data-ad-format="auto"
    data-full-width-responsive="true"></ins>
</div>
</div>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<script src="{base_path}js/common.js"></script>
<script>renderChrome('{active_nav}', '{base_path}');</script>
</body>
</html>
"""


def build_exercise_page(ex):
    steps_html = "".join(f"<li>{s}</li>" for s in ex["steps"])
    tips_html = "".join(f"<li>{t}</li>" for t in ex["tips"])
    body = f"""
  <p style="font-size:13px; color:var(--text-dim); margin-bottom:4px;">
    <a href="../{ex['category']}.html">{CATEGORY_LABEL[ex['category']]}</a> &gt; {ex['name']}
  </p>
  <h1 style="margin-top:0;">{ex['name']}</h1>
  <p style="color:var(--text-dim); margin-top:-8px; font-size:14px;">{ex['desc']}</p>

  <div class="card">
    <div class="grid-2">
      <div>
        <label>타겟 부위</label>
        <p style="margin-top:-4px;">{ex['target']}</p>
      </div>
      <div>
        <label>난이도</label>
        <p style="margin-top:-4px;">{ex['difficulty']}</p>
      </div>
    </div>
  </div>

  <div class="card">
    <h3 style="margin-top:0;">동작 방법</h3>
    <ol style="color:var(--text-dim); font-size:14px; line-height:1.8; padding-left:20px;">
      {steps_html}
    </ol>
  </div>

  <div class="card">
    <h3 style="margin-top:0;">주의사항 & 팁</h3>
    <ul style="color:var(--text-dim); font-size:14px; line-height:1.8; padding-left:20px;">
      {tips_html}
    </ul>
  </div>
"""
    html = page_shell(
        title=f"{ex['name']} 방법과 자세 - 오늘의 근력루틴",
        description=f"{ex['name']} 동작 방법, 타겟 부위, 주의사항을 확인하세요.",
        active_nav="",
        body_html=body,
        base_path="../",
    )
    with open(os.path.join(EXERCISES_DIR, f"{ex['id']}.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_category_page(category):
    label = CATEGORY_LABEL[category]
    items = [e for e in EXERCISES if e["category"] == category]
    tiles = "".join(f"""
    <a class="home-tile" href="exercises/{e['id']}.html">
      <div class="icon">{CATEGORY_ICON[category]}</div>
      <div class="title">{e['name']}</div>
      <div class="desc">{e['target']} · {e['difficulty']}</div>
    </a>""" for e in items)

    body = f"""
  <h1 style="margin-top:0;">{label}</h1>
  <p style="color:var(--text-dim); margin-top:-8px; font-size:14px;">
    {"장비 없이 어디서나 할 수 있는 운동 모음" if category == "bodyweight" else "바벨·머신 등 기구를 활용하는 운동 모음"}
  </p>
  <div class="home-grid">
    {tiles}
  </div>
"""
    html = page_shell(
        title=f"{label} 가이드 - 오늘의 근력루틴",
        description=f"{label} 종류별 동작 방법과 주의사항을 확인하세요.",
        active_nav=category,
        body_html=body,
        base_path="",
    )
    with open(os.path.join(SITE_ROOT, f"{category}.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_food_page():
    rows = "".join(
        f"<tr><td style='text-align:left;'>{f['name']}</td><td>{f['kcal']} kcal</td></tr>"
        for f in FOODS
    )
    body = f"""
  <h1 style="margin-top:0;">음식 칼로리 사전</h1>
  <p style="color:var(--text-dim); margin-top:-8px; font-size:14px;">1인분 기준 대략적인 칼로리입니다.</p>
  <div class="card">
    <table class="std-table">
      <tr><th style="text-align:left;">음식</th><th>칼로리</th></tr>
      {rows}
    </table>
  </div>
"""
    html = page_shell(
        title="음식 칼로리 사전 - 오늘의 근력루틴",
        description="밥, 계란, 닭가슴살 등 음식별 대략적인 칼로리를 확인하세요.",
        active_nav="",
        body_html=body,
        base_path="",
    )
    with open(os.path.join(SITE_ROOT, "food-calories.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_sports_page():
    options = "".join(f"<option value='{s['met']}'>{s['name']}</option>" for s in SPORTS)
    body = f"""
  <h1 style="margin-top:0;">운동별 칼로리 소모 계산기</h1>
  <p style="color:var(--text-dim); margin-top:-8px; font-size:14px;">수영, 농구 등 스포츠 활동 기준 (MET 방식)</p>

  <div class="card">
    <label for="sport">운동 종류</label>
    <select id="sport">
      {options}
    </select>
    <div class="grid-2">
      <div>
        <label for="sw">체중 (kg)</label>
        <input type="number" id="sw" inputmode="decimal" placeholder="예: 70">
      </div>
      <div>
        <label for="sm">운동 시간 (분)</label>
        <input type="number" id="sm" inputmode="numeric" placeholder="예: 30">
      </div>
    </div>
    <button class="btn" onclick="calcSportsCalorie()">계산하기</button>

    <div class="result-box" id="sportsResult" style="display:none;">
      <div class="stat-value" id="sportsKcal">-</div>
      <div class="stat-label">예상 소모 칼로리 (kcal)</div>
    </div>
  </div>

  <script>
  function calcSportsCalorie() {{
    const met = parseFloat(document.getElementById('sport').value);
    const w = parseFloat(document.getElementById('sw').value);
    const min = parseFloat(document.getElementById('sm').value);
    if (!w || !min) {{ alert('체중과 운동 시간을 입력해주세요.'); return; }}
    const kcal = met * w * (min / 60) * 1.05;
    document.getElementById('sportsKcal').textContent = kcal.toFixed(0);
    document.getElementById('sportsResult').style.display = 'block';
  }}
  </script>
"""
    html = page_shell(
        title="운동별 칼로리 소모 계산기 - 오늘의 근력루틴",
        description="수영, 농구, 달리기 등 스포츠 활동별 칼로리 소모량을 체중과 시간으로 계산합니다.",
        active_nav="",
        body_html=body,
        base_path="",
    )
    with open(os.path.join(SITE_ROOT, "sports-calories.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_generator_page():
    import json

    pool = []
    for ex in EXERCISES:
        meta = GENERATOR_META.get(ex["id"])
        if not meta:
            continue
        pool.append({
            "id": ex["id"],
            "name": ex["name"],
            "category": ex["category"],
            "muscle_group": meta["muscle_group"],
            "sets": meta["sets"],
            "reps": meta["reps"],
            "unit": meta.get("unit", "회"),
            "bw_mult": meta.get("bw_mult"),
        })
    pool_json = json.dumps(pool, ensure_ascii=False)
    groups_json = json.dumps(MUSCLE_GROUPS, ensure_ascii=False)

    group_buttons = "".join(
        f'<button type="button" class="group-btn" data-group="{g}">{g}</button>'
        for g in MUSCLE_GROUPS
    )

    body = f"""
  <h1 style="margin-top:8px;">오늘 뭐하지? 랜덤 루틴</h1>
  <p style="color:var(--text-dim); margin-top:-8px; font-size:14px;">부위와 체중만 넣으면 오늘 할 운동을 바로 만들어드려요.</p>

  <div class="card">
    <label>부위 선택 (중복 가능)</label>
    <div id="groupButtons" style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
      {group_buttons}
    </div>

    <div class="grid-2">
      <div>
        <label for="genWeight">체중 (kg)</label>
        <input type="number" id="genWeight" inputmode="decimal" placeholder="예: 70">
      </div>
      <div>
        <label for="genLevel">난이도</label>
        <select id="genLevel">
          <option value="초급">초급</option>
          <option value="중급" selected>중급</option>
          <option value="고급">고급</option>
        </select>
      </div>
    </div>

    <label for="genCount">운동 개수</label>
    <select id="genCount">
      <option value="3">3개</option>
      <option value="4" selected>4개</option>
      <option value="5">5개</option>
    </select>

    <button class="btn" onclick="generateRoutine()">루틴 생성하기</button>
  </div>

  <div id="genResultWrap" style="display:none;">
    <div class="card" id="genResult"></div>
    <button class="btn secondary" onclick="generateRoutine(true)">다시 뽑기 (같은 조건)</button>
  </div>

  <script>
  const EXERCISE_POOL = {pool_json};

  function pickRandom(arr, n) {{
    const copy = [...arr];
    const picked = [];
    while (picked.length < n && copy.length > 0) {{
      const idx = Math.floor(Math.random() * copy.length);
      picked.push(copy.splice(idx, 1)[0]);
    }}
    return picked;
  }}

  function randInRange([min, max]) {{
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }}

  document.addEventListener('DOMContentLoaded', () => {{
    document.querySelectorAll('.group-btn').forEach(btn => {{
      btn.addEventListener('click', () => btn.classList.toggle('active'));
    }});
  }});

  function generateRoutine() {{
    const selected = [...document.querySelectorAll('.group-btn.active')].map(b => b.dataset.group);
    const weight = parseFloat(document.getElementById('genWeight').value);
    const level = document.getElementById('genLevel').value;
    const count = parseInt(document.getElementById('genCount').value);

    if (selected.length === 0) {{ alert('부위를 최소 1개 이상 선택해주세요.'); return; }}
    if (!weight) {{ alert('체중을 입력해주세요.'); return; }}

    let candidates = EXERCISE_POOL.filter(e => selected.includes(e.muscle_group));
    if (candidates.length === 0) {{ alert('선택한 부위에 해당하는 운동이 아직 없어요.'); return; }}

    const picked = pickRandom(candidates, Math.min(count, candidates.length));

    let html = '<h3 style="margin-top:0;">오늘의 루틴</h3>';
    picked.forEach(ex => {{
      const sets = randInRange(ex.sets);
      const reps = randInRange(ex.reps);
      let weightLine = '';
      if (ex.bw_mult) {{
        const mult = ex.bw_mult[level];
        let suggested = weight * mult;
        suggested = Math.round(suggested / 2.5) * 2.5;
        weightLine = `<div style="color:var(--accent-2); font-size:14px; margin-top:2px;">추천 중량 약 ${{suggested}}kg (체중 대비 추정치)</div>`;
      }}
      html += `
        <div class="log-entry" style="display:block;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <a href="exercises/${{ex.id}}.html" style="font-weight:700; font-size:15px;">${{ex.name}}</a>
            <span style="font-size:12px; color:var(--text-dim);">${{ex.muscle_group}}</span>
          </div>
          <div style="color:var(--text-dim); font-size:14px; margin-top:4px;">${{sets}}세트 x ${{reps}}${{ex.unit}}</div>
          ${{weightLine}}
        </div>`;
    }});

    document.getElementById('genResult').innerHTML = html;
    document.getElementById('genResultWrap').style.display = 'block';
  }}
  </script>

  <style>
  .group-btn {{
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-dim);
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 13px;
    cursor: pointer;
  }}
  .group-btn.active {{
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
  }}
  </style>
"""
    html = page_shell(
        title="랜덤 루틴 생성기 - 오늘의 근력루틴",
        description="부위와 체중만 입력하면 오늘 할 운동과 추천 중량을 랜덤으로 만들어줍니다.",
        active_nav="home",
        body_html=body,
        base_path="",
    )
    with open(os.path.join(SITE_ROOT, "generator.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_split_page(split_id, split):
    exercise_ids = {e["id"] for e in EXERCISES}
    exercise_names = {e["id"]: e["name"] for e in EXERCISES}

    day_cards = ""
    for day in split["days"]:
        rows = ""
        for item_id, volume in day["items"]:
            if item_id in exercise_ids:
                name_html = f'<a href="../exercises/{item_id}.html" style="color:var(--text);">{exercise_names[item_id]}</a>'
            else:
                name_html = item_id
            rows += f"<tr><td style='text-align:left;'>{name_html}</td><td>{volume}</td></tr>"
        day_cards += f"""
  <div class="card">
    <h3 style="margin-top:0;">{day['name']}</h3>
    <table class="std-table">
      <tr><th style="text-align:left;">운동</th><th>세트 x 반복</th></tr>
      {rows}
    </table>
  </div>"""

    body = f"""
  <p style="font-size:13px; color:var(--text-dim); margin-bottom:4px;">
    <a href="../splits.html">분할법</a> &gt; {split['label']}
  </p>
  <h1 style="margin-top:0;">{split['label']}</h1>
  <p style="color:var(--text-dim); margin-top:-8px; font-size:14px;">{split['intro']}</p>
  {day_cards}
"""
    html = page_shell(
        title=f"{split['label']} 루틴 - 오늘의 근력루틴",
        description=f"{split['label']} 루틴 구성과 운동별 세트·반복수를 확인하세요.",
        active_nav="",
        body_html=body,
        base_path="../",
    )
    with open(os.path.join(SITE_ROOT, "splits", f"{split_id}.html"), "w", encoding="utf-8") as f:
        f.write(html)


def main():
    os.makedirs(EXERCISES_DIR, exist_ok=True)
    os.makedirs(os.path.join(SITE_ROOT, "splits"), exist_ok=True)
    for ex in EXERCISES:
        build_exercise_page(ex)
    for cat in CATEGORY_LABEL:
        build_category_page(cat)
    build_food_page()
    build_sports_page()
    build_generator_page()
    for split_id, split in SPLITS.items():
        build_split_page(split_id, split)
    print(f"생성 완료: 운동 {len(EXERCISES)}개, 카테고리 {len(CATEGORY_LABEL)}개, "
          f"음식 {len(FOODS)}개, 스포츠 {len(SPORTS)}개, 분할법 {len(SPLITS)}개")


if __name__ == "__main__":
    main()
