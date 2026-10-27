
import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="STUDY CLUB",
    page_icon="📼",
    layout="wide"
)

# 교육과정 기반 과목 및 단원 선택 목록
CURRICULUM = {
    "중학교": {
        "국어": [
            "읽기와 이해", "문학 감상", "표현과 소통",
            "문법", "듣기와 말하기", "쓰기"
        ],
        "수학": [
            "수와 연산", "문자와 식", "방정식",
            "함수", "기하", "확률과 통계"
        ],
        "영어": [
            "어휘", "문법", "듣기", "읽기",
            "말하기", "쓰기"
        ],
        "사회": [
            "지리", "자연환경과 인간 생활",
            "정치와 법", "경제", "사회문화"
        ],
        "역사": [
            "고대 세계", "동아시아 역사",
            "유럽과 아메리카", "근대 국가 수립",
            "현대 세계"
        ],
        "과학": [
            "물질의 성질", "힘과 운동",
            "생물의 구성", "전기와 자기",
            "파동", "지구와 우주"
        ],
        "정보": [
            "컴퓨팅 시스템", "데이터",
            "알고리즘과 프로그래밍", "인공지능"
        ]
    },
    "고등학교": {
        "공통국어1": [
            "읽기와 쓰기", "문학", "듣기와 말하기",
            "문법", "매체"
        ],
        "공통국어2": [
            "읽기와 쓰기", "문학", "듣기와 말하기",
            "문법", "매체"
        ],
        "문학": [
            "문학의 본질", "시", "소설",
            "극과 수필", "한국 문학의 흐름"
        ],
        "독서와 작문": [
            "독서의 원리", "비판적 읽기",
            "정보 전달 글", "논리적 글쓰기"
        ],
        "공통수학1": [
            "다항식", "방정식과 부등식",
            "경우의 수", "행렬"
        ],
        "공통수학2": [
            "도형의 방정식", "집합과 명제",
            "함수와 그래프"
        ],
        "대수": [
            "지수와 로그", "삼각함수", "수열"
        ],
        "미적분Ⅰ": [
            "함수의 극한과 연속",
            "미분계수와 도함수",
            "도함수의 활용",
            "부정적분과 정적분",
            "정적분의 활용"
        ],
        "미적분Ⅱ": [
            "수열의 극한", "급수",
            "여러 가지 함수의 미분",
            "여러 가지 적분법"
        ],
        "기하": [
            "이차곡선", "평면벡터",
            "공간도형과 공간좌표"
        ],
        "확률과 통계": [
            "경우의 수", "순열과 조합",
            "확률", "조건부확률",
            "확률분포", "통계적 추정"
        ],
        "공통영어1": [
            "어휘", "문법", "읽기",
            "듣기", "말하기와 쓰기"
        ],
        "공통영어2": [
            "어휘", "문법", "읽기",
            "듣기", "말하기와 쓰기"
        ],
        "영어Ⅰ": [
            "어휘와 표현", "글의 요지와 주제",
            "세부 내용", "추론과 빈칸",
            "어법", "영작"
        ],
        "한국사": [
            "고대 국가", "고려", "조선",
            "근대 국가 수립", "일제강점기",
            "대한민국의 발전"
        ],
        "통합사회1": [
            "인간과 사회", "자연환경",
            "문화와 다양성", "생활공간"
        ],
        "통합사회2": [
            "인권과 헌법", "시장경제와 금융",
            "세계화와 평화", "지속가능한 미래"
        ],
        "통합과학1": [
            "과학의 기초", "물질과 규칙성",
            "시스템과 상호작용"
        ],
        "통합과학2": [
            "변화와 다양성", "환경과 에너지",
            "과학과 미래 사회"
        ],
        "물리학": [
            "힘과 에너지", "전기와 자기",
            "빛과 물질", "운동과 상호작용"
        ],
        "화학": [
            "화학의 언어", "물질의 구조",
            "화학 결합", "화학 반응"
        ],
        "생명과학": [
            "생명 시스템", "항상성",
            "유전과 진화", "생태계"
        ],
        "세포와 물질대사": [
            "세포의 구조와 기능",
            "세포막과 물질 이동",
            "효소와 생체 촉매",
            "세포 호흡", "광합성",
            "물질대사와 에너지"
        ],
        "생물의 유전": [
            "유전 물질", "유전자 발현",
            "염색체와 세포 분열",
            "유전 현상", "유전적 다양성"
        ],
        "지구과학": [
            "지구 시스템", "대기와 해양",
            "지구의 역사", "천체와 우주"
        ]
    }
}

# 레트로 스타일
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

.stApp {
    background: #F4EBD8;
    color: #28291F;
    font-family: 'Noto Sans KR', sans-serif;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}
.hero {
    background: #28291F;
    color: #F4EBD8;
    padding: 32px;
    border: 2px solid #28291F;
    border-radius: 4px;
    box-shadow: 7px 7px 0 #D95D39;
    margin-bottom: 30px;
}
.hero h1 {
    color: #F4EBD8;
    font-size: 40px;
    font-weight: 900;
}
.hero p {
    color: #D6C9AE;
}
div[data-testid="stExpander"] {
    background: #FBF6EA;
    border: 1px solid #D6C9AE;
    border-radius: 4px;
}
div[data-testid="stMetric"] {
    background: #FBF6EA;
    border: 1px solid #D6C9AE;
    padding: 14px;
    border-radius: 4px;
}
div.stButton > button[kind="primary"] {
    background: #D95D39;
    color: white;
    border: 2px solid #28291F;
    border-radius: 3px;
    min-height: 46px;
    font-weight: 800;
    box-shadow: 4px 4px 0 #28291F;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <p>EST. 2026 / YOUR STUDY ARCHIVE</p>
    <h1>STUDY CLUB. 📼</h1>
    <p>시험공부를 오늘의 계획으로 바꾸는 레트로 플래너.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📼 STUDY CLUB")
    school_level = st.selectbox(
        "학교급",
        list(CURRICULUM.keys())
    )
    subject_count = st.number_input(
        "시험 과목 수", 1, 12, 5
    )
    daily_hours = st.slider(
        "하루 공부 가능 시간", 1, 12, 4
    )


st.markdown("## 01 / 과목 선택")

available_subjects = list(CURRICULUM[school_level].keys())

selected_subjects = st.multiselect(
    "시험 과목을 선택해 줘",
    options=available_subjects,
    max_selections=int(subject_count),
    placeholder="과목 이름을 검색하거나 선택해 줘"
)

unit_settings = {}

st.markdown("## 02 / 단원 선택")

for subject in selected_subjects:
    with st.expander(subject, expanded=True):
        chapters = CURRICULUM[school_level][subject]

        selected_chapters = st.multiselect(
            f"{subject} 시험 범위",
            chapters,
            key=f"chapters_{school_level}_{subject}"
        )

        for chapter in selected_chapters:
            st.markdown(f"**{chapter}**")

            c1, c2, c3 = st.columns(3)

            difficulty = c1.select_slider(
                "난이도",
                options=[1, 2, 3, 4, 5],
                value=3,
                key=f"d_{subject}_{chapter}"
            )

            mastery = c2.select_slider(
                "이해도",
                options=[1, 2, 3, 4, 5],
                value=3,
                key=f"m_{subject}_{chapter}"
            )

            hours = c3.number_input(
                "예상 공부 시간",
                min_value=0.5,
                max_value=20.0,
                value=1.0,
                step=0.5,
                key=f"h_{subject}_{chapter}"
            )

            unit_settings[(subject, chapter)] = {
                "subject": subject,
                "chapter": chapter,
                "difficulty": difficulty,
                "mastery": mastery,
                "hours": hours
            }

st.markdown("## 03 / 시험 시간표")

selected_date = st.date_input(
    "시험 주간에 속한 날짜",
    value=date.today() + timedelta(
        days=(7 - date.today().weekday()) % 7
    )
)

monday = selected_date - timedelta(
    days=selected_date.weekday()
)

weekdays = [monday + timedelta(days=i) for i in range(5)]
weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일"]

exam_schedule = {}
cols = st.columns(5)

for i, col in enumerate(cols):
    day = weekdays[i]

    with col:
        st.markdown(f"**{weekday_names[i]}**")
        st.caption(day.strftime("%m/%d"))

        exam_schedule[day] = st.multiselect(
            "시험 과목",
            selected_subjects,
            key=f"exam_{day.isoformat()}",
            label_visibility="collapsed"
        )


st.markdown("## 04 / 공부 계획")

def priority(unit, exam_day, current_day):
    days_left = max((exam_day - current_day).days, 0)

    urgency = 1 + 5 / ((days_left + 1) ** 0.75)
    difficulty_factor = 0.8 + unit["difficulty"] * 0.28
    weakness_factor = 0.8 + (6 - unit["mastery"]) * 0.22

    return urgency * difficulty_factor * weakness_factor


if st.button(
    "✳ 공부 계획 만들기",
    type="primary",
    use_container_width=True
):
    exam_dates = {}

    for day, subjects_on_day in exam_schedule.items():
        for subject in subjects_on_day:
            if subject not in exam_dates:
                exam_dates[subject] = day

    units = [
        dict(unit)
        for unit in unit_settings.values()
        if unit["subject"] in exam_dates
    ]

    if not units:
        st.error("과목, 단원, 시험 일정을 모두 선택해 줘.")
        st.stop()

    today = date.today()
    last_day = weekdays[-1]

    if last_day < today:
        st.error("시험 주간 날짜를 다시 선택해 줘.")
        st.stop()

    study_days = [
        day for day in weekdays
        if day >= max(today, monday)
    ]

    remaining = {
        i: unit["hours"] * 60
        for i, unit in enumerate(units)
    }

    plans = []
    daily_limit = int(daily_hours * 60)

    for day in study_days:
        available = daily_limit

        while available >= 5:
            candidates = []

            for i, unit in enumerate(units):
                if remaining[i] < 5:
                    continue

                exam_day = exam_dates[unit["subject"]]

                if exam_day < day:
                    continue

                candidates.append((
                    priority(unit, exam_day, day), i
                ))

            if not candidates:
                break

            candidates.sort(reverse=True)
            total_score = sum(s for s, _ in candidates)
            spent = 0

            for score, i in candidates:
                if available - spent < 5:
                    break

                share = available * score / total_score
                minutes = int(min(
                    share,
                    remaining[i],
                    45,
                    available - spent
                ))

                if minutes < 5:
                    continue

                remaining[i] -= minutes
                spent += minutes

                plans.append({
                    "날짜": day,
                    "요일": weekday_names[day.weekday()],
                    "과목": units[i]["subject"],
                    "단원": units[i]["chapter"],
                    "공부 시간(분)": minutes
                })

            if spent == 0:
                break

            available -= spent

    st.session_state["plans"] = plans
    st.session_state["remaining"] = remaining
    st.session_state["units"] = units
    st.session_state["exam_dates"] = exam_dates
    st.session_state["study_days"] = study_days


if "plans" in st.session_state:
    plans = st.session_state["plans"]
    remaining = st.session_state["remaining"]
    units = st.session_state["units"]
    exam_dates = st.session_state["exam_dates"]
    study_days = st.session_state["study_days"]

    if plans:
        df = pd.DataFrame(plans)
        total = int(df["공부 시간(분)"].sum())

        st.success("공부 계획이 완성됐어!")

        c1, c2, c3 = st.columns(3)
        c1.metric("시험 과목", f"{len(exam_dates)}개")
        c2.metric("총 공부 시간", f"{total // 60}시간 {total % 60}분")
        c3.metric(
            "미배정 분량",
            f"{sum(remaining.values()) / 60:.1f}시간"
        )

        st.markdown("### 요일별 체크리스트")

        for day in study_days:
            day_df = df[df["날짜"] == day]

            with st.expander(
                f"{weekday_names[day.weekday()]} · {day:%m/%d}",
                expanded=(day == study_days[0])
            ):
                if day_df.empty:
                    st.write("오늘 배정된 공부가 없어.")
                else:
                    for idx, row in day_df.iterrows():
                        st.checkbox(
                            f"{row['과목']} — {row['단원']} "
                            f"({row['공부 시간(분)']}분)",
                            key=f"done_{day}_{idx}"
                        )

        st.markdown("### 전체 공부 계획")

        display_df = df.copy()
        display_df["날짜"] = display_df["날짜"].apply(
            lambda d: d.strftime("%m/%d")
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ 공부 계획 다운로드",
            data=display_df.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="study_club_plan.csv",
            mime="text/csv"
        )

        if sum(remaining.values()) > 5:
            st.warning(
                "모든 단원을 배정하지 못했어. "
                "공부 시간을 늘리거나 예상 분량을 조정해 줘."
            )
    else:
        st.warning("배정된 공부가 없어. 입력한 일정을 확인해 줘.")

st.caption("STUDY CLUB © 2026 — MADE FOR BETTER DAYS.")
