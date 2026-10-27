import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="STUDY FLOW",
    page_icon="✳",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
.stApp {
    background: #F7F8FA;
    color: #202C43;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
.hero {
    background: #202C43;
    color: white;
    padding: 35px;
    border-radius: 20px;
    margin-bottom: 25px;
}
.hero h1 {
    color: white;
    font-size: 36px;
    font-weight: 800;
}
.hero p {
    color: #D5DCEA;
}
div[data-testid="stExpander"] {
    background: white;
    border-radius: 12px;
}
div.stButton > button[kind="primary"] {
    background: #5068E8;
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 45px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <p>YOUR PERSONAL STUDY SYSTEM</p>
    <h1>STUDY FLOW ✳</h1>
    <p>막막한 시험공부를, 오늘 해야 할 명확한 계획으로.</p>
</div>
""", unsafe_allow_html=True)

# 사이드바 설정
with st.sidebar:
    st.title("✳ STUDY FLOW")
    st.caption("SMART EXAM PLANNER")

    subject_count = st.number_input(
        "공부할 과목 수",
        min_value=1,
        max_value=12,
        value=5
    )

    daily_hours = st.slider(
        "하루 공부 가능 시간",
        min_value=1,
        max_value=12,
        value=4
    )

# 과목 정보 입력
st.header("01 / 과목 설정")
st.caption("과목별 단원, 난이도, 이해도, 남은 공부 시간을 입력해 줘.")

subjects = []

for i in range(int(subject_count)):
    defaults = ["국어", "수학", "영어", "과학", "사회"]
    default_name = defaults[i] if i < 5 else f"과목 {i+1}"

    with st.expander(f"📘 과목 {i+1}", expanded=(i < 2)):
        name = st.text_input(
            "과목 이름",
            value=default_name,
            key=f"name_{i}"
        )

        importance = st.slider(
            "과목 중요도",
            1, 5, 3,
            key=f"importance_{i}"
        )

        st.markdown("**단원별 학습 정보**")
        st.caption(
            "한 줄에 한 단원씩 입력해 줘. "
            "형식: 단원명,난이도,이해도,남은시간"
        )

        raw = st.text_area(
            "단원 목록",
            value=(
                "기본 개념,3,3,1.5\n"
                "응용 문제,4,2,2\n"
                "심화 문제,5,2,1.5"
            ),
            key=f"units_{i}",
            height=120
        )

        subjects.append({
            "name": name.strip() or f"과목 {i+1}",
            "importance": importance,
            "raw": raw
        })

# 시험 주간 설정
st.divider()
st.header("02 / 시험 일정")

selected_date = st.date_input(
    "시험 주간에 속하는 날짜를 선택해 줘",
    value=date.today() + timedelta(
        days=(7-date.today().weekday()) % 7
    )
)

monday = selected_date - timedelta(days=selected_date.weekday())
weekdays = [monday + timedelta(days=i) for i in range(5)]

subject_names = list(dict.fromkeys(
    s["name"] for s in subjects
))

exam_schedule = {}
cols = st.columns(5)

for i, col in enumerate(cols):
    day = weekdays[i]

    with col:
        st.markdown(
            f"**{'월화수목금'[i]}요일**"
        )
        st.caption(day.strftime("%m/%d"))

        exam_schedule[day] = st.multiselect(
            "시험 과목",
            subject_names,
            key=f"exam_{day}"
        )

# 공부 계획 계산
st.divider()
st.header("03 / 학습 계획")

if st.button(
    "✳ 학습 계획 계산하기",
    type="primary",
    use_container_width=True
):
    units = []
    exam_dates = {}

    for day, names in exam_schedule.items():
        for name in names:
            if name not in exam_dates:
                exam_dates[name] = day

    for subject in subjects:
        for line in subject["raw"].splitlines():
            parts = [p.strip() for p in line.split(",")]

            if not parts or not parts[0]:
                continue

            try:
                unit_name = parts[0]
                difficulty = max(1, min(5, int(parts[1])))
                mastery = max(1, min(5, int(parts[2])))
                hours = max(0.1, float(parts[3]))

                units.append({
                    "과목": subject["name"],
                    "단원": unit_name,
                    "난이도": difficulty,
                    "이해도": mastery,
                    "남은시간": hours,
                    "중요도": subject["importance"]
                })

            except (ValueError, IndexError):
                st.warning(
                    f"{subject['name']}의 단원 입력을 확인해 줘."
                )

    if not units:
        st.error("단원 정보를 먼저 입력해 줘.")
        st.stop()

    if not exam_dates:
        st.error("월요일부터 금요일 중 시험 과목을 선택해 줘.")
        st.stop()

    # 우선순위 계산
    def score(unit, today):
        exam_day = exam_dates[unit["과목"]]
        days_left = max((exam_day - today).days, 0)

        urgency = 1 + 5 / ((days_left + 1) ** 0.75)
        difficulty = unit["난이도"]
        weakness = 6 - unit["이해도"]
        importance = unit["중요도"]

        return (
            urgency
            * (0.8 + difficulty * 0.28)
            * (0.8 + weakness * 0.22)
            * (0.8 + importance * 0.1)
        )

    today = date.today()
    start_day = max(today, monday)
    study_days = [
        monday + timedelta(days=i)
        for i in range(5)
        if monday + timedelta(days=i) >= start_day
    ]

    # 계획 수립: 시험일 이후에는 해당 과목을 배정하지 않음
    remaining = {
        i: unit["남은시간"] * 60
        for i, unit in enumerate(units)
    }

    plans = []

    for day in study_days:
        available = daily_hours * 60

        while available >= 10:
            candidates = []

            for i, unit in enumerate(units):
                if unit["과목"] not in exam_dates:
                    continue
                if exam_dates[unit["과목"]] < day:
                    continue
                if remaining[i] < 5:
                    continue

                candidates.append((
                    score(unit, day),
                    i
                ))

            if not candidates:
                break

            candidates.sort(reverse=True)
            total_score = sum(s for s, _ in candidates)

            # 우선순위에 따라 학습 시간을 배분
            allocations = []

            for s, i in candidates:
                share = available * s / total_score
                minutes = min(
                    share,
                    remaining[i],
                    45
                )

                if minutes >= 5:
                    allocations.append((i, minutes))

            if not allocations:
                break

            spent = 0

            for i, minutes in allocations:
                minutes = min(minutes, available - spent)

                if minutes < 5:
                    continue

                remaining[i] -= minutes
                spent += minutes

                plans.append({
                    "날짜": day,
                    "요일": "월화수목금"[day.weekday()] + "요일",
                    "과목": units[i]["과목"],
                    "단원": units[i]["단원"],
                    "공부 시간(분)": round(minutes),
                    "우선순위": round(score(units[i], day), 2)
                })

                if spent >= available:
                    break

            available -= spent

            if spent < 5:
                break

    if not plans:
        st.warning("배정할 공부 분량이 없어. 입력 정보를 확인해 줘.")
        st.stop()

    df = pd.DataFrame(plans)

    # 대시보드
    st.success("학습 계획이 완성됐어!")

    c1, c2, c3 = st.columns(3)

    c1.metric("시험 과목", f"{len(exam_dates)}개")
    c2.metric("계획된 학습", f"{round(df['공부 시간(분)'].sum()/60, 1)}시간")
    c3.metric("학습 단원", f"{df['단원'].nunique()}개")

    st.subheader("⚡ 과목별 우선순위")

    ranking = []

    for name, exam_day in exam_dates.items():
        subject_units = [
            u for u in units if u["과목"] == name
        ]

        if not subject_units:
            continue

        avg_difficulty = sum(
            u["난이도"] for u in subject_units
        ) / len(subject_units)

        avg_mastery = sum(
            u["이해도"] for u in subject_units
        ) / len(subject_units)

        days_left = max((exam_day - today).days, 0)

        ranking.append({
            "과목": name,
            "시험일": exam_day.strftime("%m/%d"),
            "남은 날짜": f"D-{days_left}",
            "평균 난이도": round(avg_difficulty, 1),
            "평균 이해도": round(avg_mastery, 1),
            "우선순위": round(
                (1 + 5/(days_left+1)**0.75)
                * (0.8 + avg_difficulty*0.28)
                * (0.8 + (6-avg_mastery)*0.22),
                2
            )
        })

    ranking.sort(
        key=lambda x: x["우선순위"],
        reverse=True
    )

    st.dataframe(
        pd.DataFrame(ranking),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🗓️ 요일별 학습 일정")

    for day in study_days:
        day_df = df[df["날짜"] == day]

        with st.expander(
            f"{'월화수목금'[day.weekday()]}요일 "
            f"· {day.strftime('%m/%d')} "
            f"· {int(day_df['공부 시간(분)'].sum())}분",
            expanded=(day == study_days[0])
        ):
            if day_df.empty:
                st.write("배정된 학습이 없어.")
            else:
                for _, row in day_df.iterrows():
                    st.markdown(
                        f"**{row['과목']} — {row['단원']}**  \n"
                        f"⏱️ {int(row['공부 시간(분)'])}분"
                    )

    st.subheader("📋 전체 학습 계획")
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
        "⬇️ 계획표 CSV 다운로드",
        data=display_df.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="study_flow_plan.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.caption(
        "STUDY FLOW · 난이도, 이해도, 중요도와 시험 날짜를 "
        "기반으로 계산한 학습 추천이야."
    )

else:
    st.info(
        "과목과 시험 일정을 입력한 뒤 "
        "'학습 계획 계산하기'를 눌러 줘."
    )
